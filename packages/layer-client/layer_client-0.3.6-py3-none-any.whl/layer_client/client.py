import abc
import json
import time
import uuid
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, field, replace
from logging import Logger
from typing import Any, Iterator, List, Mapping, Optional, Union

import grpc
from pandas import DataFrame as PDataFrame
from pyspark.sql import DataFrame as SDataFrame, SparkSession

from .api.entity.dataset_build_pb2 import DatasetBuild as PBDatasetBuild
from .api.entity.dataset_pb2 import Dataset as PBDataset
from .api.entity.dataset_version_pb2 import DatasetVersion as PBDatasetVersion
from .api.entity.feature_set_pb2 import FeatureSet as PBFeatureSet
from .api.entity.sql_feature_pb2 import SqlFeature as PBSqlFeature
from .api.ids_pb2 import (
    AppId,
    DatasetBuildId,
    DatasetId,
    DatasetVersionId,
    FeatureSetId,
    OrganizationId,
    UserId,
)
from .api.service.datacatalog.data_catalog_api_pb2 import (
    AddFeatureSetRequest,
    CompleteBuildRequest,
    GetBuildRequest,
    GetDatasetRequest,
    GetFeatureSetRequest,
    GetLatestBuildRequest,
    GetVersionRequest,
    InitiateBuildRequest,
)
from .api.service.datacatalog.data_catalog_api_pb2_grpc import DataCatalogAPIStub
from .api.service.modelcatalog.model_catalog_api_pb2 import (
    CompleteModelTrainRequest,
    GetModelTrainIdRequest,
    StartModelTrainRequest,
)
from .api.service.modelcatalog.model_catalog_api_pb2_grpc import ModelCatalogAPIStub
from .api.value.metadata_pb2 import Metadata
from .api.value.storage_location_pb2 import StorageLocation
from .config import LayerClientConfig
from .exceptions import LayerClientException
from .mlmodels.service import MLModelService, ModelDefinition


_MAX_FAILURE_INFO_LENGTH = 200


@dataclass(frozen=True)
class Dataset:
    name: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    version: str = ""
    schema: str = "{}"
    uri: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Feature(abc.ABC):
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class SQLFeature(Feature):
    query: str = ""


@dataclass(frozen=True)
class Featureset:
    name: str
    features: List[Feature]
    id: uuid.UUID = field(default_factory=uuid.uuid4)


class DataCatalogClient:
    _service: DataCatalogAPIStub

    def __init__(
        self, config: LayerClientConfig, logger: Logger, session: SparkSession
    ):
        self._user_id = config.user_id
        self._client_id = config.client_id
        self._config = config.data_catalog
        self._session = session
        self._logger = logger

    @contextmanager
    def init(self) -> Iterator["DataCatalogClient"]:
        with grpc.insecure_channel(self._config.address) as channel:
            self._service = DataCatalogAPIStub(channel)  # type: ignore
            yield self

    def add_featureset(self, featureset: Featureset) -> Featureset:
        sql_features = []
        for feature in featureset.features:
            if not isinstance(feature, SQLFeature):
                raise TypeError(f"Unsupported type: {feature.__class__!r}")
            sql_features.append(
                PBSqlFeature(
                    name=feature.name,
                    query_text=feature.query,
                )
            )
        resp = self._service.AddFeatureSet(
            AddFeatureSetRequest(
                feature_set=PBFeatureSet(
                    name=featureset.name,
                    sql_features=sql_features,
                )
            )
        )
        return self.get_featureset_by_id(uuid.UUID(resp.feature_set_id.value))

    def get_featureset_by_id(self, id_: uuid.UUID) -> Featureset:
        resp = self._service.GetFeatureSet(
            GetFeatureSetRequest(feature_set_id=FeatureSetId(value=str(id_)))
        )
        features: List[Feature] = []
        for feature in resp.feature_set.sql_features:
            features.append(
                SQLFeature(
                    id=uuid.UUID(feature.id.value),
                    name=feature.name,
                    query=feature.query_text,
                )
            )
        return Featureset(
            id=uuid.UUID(resp.feature_set.id.value),
            name=resp.feature_set.name,
            features=features,
        )

    def add_dataset(self, dataset: Dataset) -> Dataset:
        self._logger.debug(
            "Adding a new dataset with name %r and version %r",
            dataset.name,
            dataset.version,
        )
        timestamp = int(time.time())
        init_resp = self._service.InitiateBuild(
            InitiateBuildRequest(
                dataset_name=dataset.name,
                dataset_version=dataset.version or "",
                build_description="",
                format="unused",
                user=UserId(value=str(self._user_id)),
                schema=dataset.schema,
                current_timestamp=timestamp,
            )
        )
        comp_resp = self._service.CompleteBuild(
            CompleteBuildRequest(
                id=init_resp.id,
                current_timestamp=timestamp,
                status=PBDatasetBuild.BuildStatus.BUILD_STATUS_COMPLETED,  # type: ignore
                success=CompleteBuildRequest.BuildSuccess(  # type: ignore
                    location=StorageLocation(
                        uri=dataset.uri, metadata=Metadata(value=dataset.metadata)
                    )
                ),
            )
        )
        return replace(
            dataset,
            id=uuid.UUID(comp_resp.version.dataset_id.value),
            version=comp_resp.version.name,
        )

    def get_dataset_by_id(self, id_: uuid.UUID) -> Dataset:
        dataset = self._get_dataset_by_id(str(id_))
        build = self._get_build_by_id(dataset.default_build.value)  # type: ignore
        version = self._get_version_by_id(build.dataset_version_id.value)  # type: ignore
        return Dataset(
            id=id_,
            name=dataset.name,  # type: ignore
            version=version.name,  # type: ignore
            schema=version.schema,  # type: ignore
            uri=build.location.uri,  # type: ignore
            metadata=dict(build.location.metadata.value),  # type: ignore
        )

    def get_dataset_by_name(self, name: str, version: Optional[str] = None) -> Dataset:
        build = self._get_build_by_name(name, version)
        version = self._get_version_by_id(build.dataset_version_id.value)  # type: ignore
        dataset = self._get_dataset_by_id(version.dataset_id.value)
        return Dataset(
            id=uuid.UUID(dataset.id.value),  # type: ignore
            name=dataset.name,  # type: ignore
            version=version.name,
            schema=version.schema,
            uri=build.location.uri,  # type: ignore
            metadata=dict(build.location.metadata.value),  # type: ignore
        )

    def _get_dataset_by_id(self, id_: str) -> PBDataset:  # type: ignore
        return self._service.GetDataset(
            GetDatasetRequest(dataset_id=DatasetId(value=id_))
        ).dataset

    def _get_version_by_id(self, id_: str) -> PBDatasetVersion:  # type: ignore
        return self._service.GetVersion(
            GetVersionRequest(version_id=DatasetVersionId(value=id_))
        ).version

    def _get_build_by_id(self, id_: str) -> PBDatasetBuild:  # type: ignore
        return self._service.GetBuild(
            GetBuildRequest(build_id=DatasetBuildId(value=id_))
        ).build

    def _get_build_by_name(
        self, name: str, version: Optional[str] = None
    ) -> PBDatasetBuild:  # type: ignore
        return self._service.GetLatestBuild(
            GetLatestBuildRequest(
                dataset_name=name,
                dataset_version=version,
            )
        ).build

    def load(self, name: str, version: Optional[str] = None) -> SDataFrame:
        self._logger.debug(
            "Loading data object with name %r and version %r", name, version
        )
        build = self._get_build_by_name(name, version)
        return self._session.read.parquet(build.location.uri)  # type: ignore

    def save(
        self,
        name: str,
        obj: Union[PDataFrame, SDataFrame],
        version: Optional[str] = None,
    ) -> PBDatasetBuild:  # type: ignore
        self._logger.debug(
            "Saving data object with name %r and version %r", name, version
        )
        df: SDataFrame
        if isinstance(obj, PDataFrame):
            df = self._session.createDataFrame(obj)
        else:
            df = obj

        schema = json.dumps(df.schema.jsonValue())
        init_resp = self._service.InitiateBuild(
            InitiateBuildRequest(
                dataset_name=name,
                dataset_version=version or "",
                build_description="",
                format="parquet",
                user=UserId(value=str(self._user_id)),
                schema=schema,
                current_timestamp=int(time.time()),
            )
        )

        uri = f"s3a://{self._config.s3_bucket_name}/{init_resp.suggested_path}"
        exception: Optional[Exception] = None
        try:
            df.write.mode("overwrite").parquet(uri)
        except Exception as exc:
            exception = exc
            comp_req = CompleteBuildRequest(
                id=init_resp.id,
                current_timestamp=int(time.time()),
                status=PBDatasetBuild.BuildStatus.BUILD_STATUS_FAILED,  # type: ignore
                failure=CompleteBuildRequest.BuildFailed(  # type: ignore
                    info=str(exc)[:_MAX_FAILURE_INFO_LENGTH]
                ),
            )
        else:
            comp_req = CompleteBuildRequest(
                id=init_resp.id,
                current_timestamp=int(time.time()),
                status=PBDatasetBuild.BuildStatus.BUILD_STATUS_COMPLETED,  # type: ignore
                success=CompleteBuildRequest.BuildSuccess(  # type: ignore
                    location=StorageLocation(uri=uri)
                ),
            )

        comp_resp = self._service.CompleteBuild(comp_req)

        if exception:
            raise exception

        return comp_resp.build


class ModelCatalogClient:
    _service: ModelCatalogAPIStub

    def __init__(
        self,
        config: LayerClientConfig,
        ml_model_service: MLModelService,
        logger: Logger,
    ):
        self._client_id = config.client_id
        self._config = config.model_catalog
        self._org_id: uuid.UUID = config.organization_id
        self._logger = logger
        self._ml_model_service = ml_model_service

    @contextmanager
    def init(self) -> Iterator["ModelCatalogClient"]:
        with grpc.insecure_channel(self._config.address) as channel:
            self._service = ModelCatalogAPIStub(channel=channel)  # type: ignore
            yield self

    def load(
        self,
        organization_id: str,
        name: str,
        version: Optional[int] = None,
        build: Optional[int] = None,
    ) -> Any:
        """
        Loads a model from the model catalog

        :param organization_id: org id
        :param name: the name of the model
        :param version: the version of the model
        :param build: the build number of the model
        :return: a model definition
        """
        self._logger.debug(f"Loading model object with name {name}")
        response = self._service.GetModelTrainId(
            GetModelTrainIdRequest(
                organization_id=OrganizationId(value=str(organization_id)),
                model_name=name,
                model_version=None if version is None else str(version),
                model_train=build,
            )
        )
        location = response.id.value
        flavor_key = response.flavor
        mlflow_model_name = location
        model_definition = ModelDefinition(
            self._org_id,
            model_name=name,
            mlflow_model_name=mlflow_model_name,
            flavor_key=flavor_key,
        )
        return self._ml_model_service.retrieve(model_definition)

    def save(
        self,
        name: str,
        obj: Any,
        owner: uuid.UUID,
        version: Optional[int] = None,
        model_input: Any = None,
        model_output: Any = None,
        notebook_id: Optional[str] = None,
    ) -> Any:
        organization_id = self._org_id
        flavor_key, flavor = self._ml_model_service.get_model_flavor(obj)
        if not flavor:
            raise LayerClientException("Model flavor not found")
        location = self._service.StartModelTrain(
            StartModelTrainRequest(
                organization_id=OrganizationId(value=str(organization_id)),
                app_id=AppId(value=str(self._client_id)),
                user_id=UserId(value=str(owner)),
                model_name=name,
                model_version=None if version is None else str(version),
                flavor=flavor_key,
                start_timestamp=int(time.time()),
            )
        ).id.value

        mlflow_model_name = location
        self._logger.debug(
            f"Storing given model {obj} with mlflow model name {mlflow_model_name}"
        )
        model_definition = ModelDefinition(
            organization_id=organization_id,
            model_name=name,
            mlflow_model_name=mlflow_model_name,
        )
        self._ml_model_service.store(
            model_definition,
            obj,
            model_input,
            model_output,
            flavor,
            owner,
            notebook_id,
        )
        signature = self._ml_model_service.get_model_signature(
            model_input, model_output
        )
        self._service.CompleteModelTrain(
            CompleteModelTrainRequest(
                location=location,
                complete_timestamp=int(time.time()),
                signature=str(signature) if signature is not None else None,
            )
        )
        return obj

    def log_parameter(self, key: str, value: str) -> None:
        """
        Logs given parameter to the model storage service

        :param key: name of the parameter
        :param value: value of the parameter
        """
        self._ml_model_service.log_parameter(str(self._client_id), key, value)

    def log_metric(self, key: str, value: float) -> None:
        """
        Logs given metric to the model storage service

        :param key: name of the metric
        :param value: value of the metric
        """
        self._ml_model_service.log_metric(str(self._client_id), key, value)


class LayerClient:
    def __init__(
        self, config: LayerClientConfig, logger: Logger, session: SparkSession
    ):
        self._config = config
        self._data_catalog = DataCatalogClient(config, logger, session)
        ml_model_service = MLModelService(logger)
        self._model_catalog = ModelCatalogClient(config, ml_model_service, logger)

    @contextmanager
    def init(self) -> Iterator["LayerClient"]:
        with ExitStack() as exit_stack:
            if self._config.data_catalog.is_enabled:
                exit_stack.enter_context(self._data_catalog.init())
            if self._config.model_catalog.is_enabled:
                exit_stack.enter_context(self._model_catalog.init())
            yield self

    @property
    def data_catalog(self) -> DataCatalogClient:
        return self._data_catalog

    @property
    def model_catalog(self) -> ModelCatalogClient:
        return self._model_catalog
