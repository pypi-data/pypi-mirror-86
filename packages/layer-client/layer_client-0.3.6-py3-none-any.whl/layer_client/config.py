import os
import uuid
from dataclasses import dataclass, replace
from typing import Mapping, Optional


@dataclass(frozen=True)
class DataCatalogConfig:
    host: str
    port: int
    s3_bucket_name: str

    @classmethod
    def disabled(cls) -> "DataCatalogConfig":
        return cls(host="", port=0, s3_bucket_name="")

    @property
    def is_enabled(self) -> bool:
        return bool(self.host)

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

    def with_address(self, address: str) -> "DataCatalogConfig":
        host, port = address.split(":", 1)
        return replace(self, host=host, port=int(port))


@dataclass(frozen=True)
class ModelCatalogConfig:
    host: str
    port: int

    @classmethod
    def disabled(cls) -> "ModelCatalogConfig":
        return cls(host="", port=0)

    @property
    def is_enabled(self) -> bool:
        return bool(self.host)

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"


@dataclass(frozen=True)
class LayerClientConfig:
    organization_id: uuid.UUID
    user_id: uuid.UUID
    client_id: uuid.UUID
    data_catalog: DataCatalogConfig
    model_catalog: ModelCatalogConfig


class EnvironLayerClientConfigFactory:
    def __init__(
        self,
        require_data_catalog_address: bool = True,
        environ: Optional[Mapping[str, str]] = None,
    ) -> None:
        self._require_data_catalog_address = require_data_catalog_address
        self._environ = environ or os.environ

    def create(self) -> LayerClientConfig:
        host, port = "", "0"
        address = self._environ.get("LAYER_DATA_CATALOG_ADDRESS")
        if self._require_data_catalog_address and not address:
            raise ValueError("Data Catalog address is required")
        if address:
            host, port = address.split(":", 1)
        s3_bucket_name = self._environ.get("LAYER_S3_BUCKET_NAME") or ""
        return LayerClientConfig(
            organization_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            client_id=uuid.uuid4(),
            data_catalog=DataCatalogConfig(
                host=host, port=int(port), s3_bucket_name=s3_bucket_name
            ),
            model_catalog=ModelCatalogConfig.disabled(),
        )
