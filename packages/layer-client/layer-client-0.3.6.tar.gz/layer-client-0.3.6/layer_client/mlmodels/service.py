import importlib
from logging import Logger
from typing import Any, Dict, Optional, Tuple
from uuid import UUID

import mlflow
from mlflow.entities import Experiment, Run
from mlflow.exceptions import RestException
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
from mlflow.tracking.fluent import ActiveRun
from mlflow.utils.mlflow_tags import MLFLOW_SOURCE_TYPE

from layer_client.exceptions import LayerClientException
from layer_client.mlmodels import ModelObject, flavors

from .flavors import ModelFlavor
from .flavors.flavor import ModelDefinition


class MLModelService:
    """
    Handles ML model lifecycle within the application. Users of this service can
    store/load/delete ML models.
    """

    def __init__(self, logger: Logger):
        self.logger = logger
        self.client = MlflowClient()
        self.active_runs: Dict[str, Run] = {}

    def start_run(self, notebook_id: str) -> None:
        """
        Starts an MLFlow run for specified notebook

        Args:
            notebook_id: notebook id to be associated with the run
        """
        experiment = self.__get_or_create_experiment(notebook_id)
        active_run: Run = self.__create_run(experiment_id=experiment.experiment_id)
        self.active_runs[notebook_id] = active_run

    def end_run(self, notebook_id: str) -> None:
        """
        Marks the active MLFlow run as finished for specified notebook

        Args:
            notebook_id: notebook id which corresponding run would be marked as finished
        """
        active_run = self.active_runs[notebook_id]
        run_id = active_run.info.run_id
        self.client.set_terminated(run_id=run_id)
        del self.active_runs[notebook_id]

    def log_parameter(self, notebook_id: str, key: str, value: str) -> None:
        active_run = self.active_runs[notebook_id]
        self.client.log_param(active_run.info.run_id, key, value)

    def log_metric(self, notebook_id: str, key: str, value: float) -> None:
        active_run = self.active_runs[notebook_id]
        self.client.log_metric(active_run.info.run_id, key, value)

    # pytype: disable=annotation-type-mismatch # https://github.com/google/pytype/issues/640
    def store(
        self,
        model_definition: ModelDefinition,
        model_object: ModelObject,
        model_input: Any,
        model_output: Any,
        flavor: ModelFlavor,
        owner: UUID,
        notebook_id: Optional[str],
    ) -> None:  # pytype: enable=annotation-type-mismatch
        """
        Stores given model object along with its definition to the backing storage.
        The metadata written to db and used later on whilst loading the ML model.

        Args:
            model_definition: Model metadata object which describes the model instance
            model_object: Model object to be stored
            model_input: Model input (training) data
            model_output: Model output (prediction) data
            flavor: Corresponding flavor information of the model object
            owner: the owner of the model. Currently considered to be the user who first saved it.
            notebook_id: ID of the notebook which model originated from
        """
        if notebook_id not in self.active_runs:
            self.start_run(notebook_id)
        active_run = self.active_runs[notebook_id]
        mlflow.tracking.fluent._active_run_stack.append(  # pylint: disable=protected-access
            ActiveRun(active_run)
        )
        path = model_definition.model_organization_id
        self.logger.debug(
            f"Saving user model {model_definition.mlflow_model_name}({model_object}) on path {path}"
        )
        if model_output is not None and model_input is None:
            raise LayerClientException(
                "Model input not found! Model output can be assigned only if model input is assigned"
            )
        active_run_id = active_run.info.run_id
        self.end_run(notebook_id)
        self.start_run(notebook_id)
        try:
            flavor.save(
                model_definition,
                model_object,
                active_run_id,
                tags={},
            )
            self.logger.debug(f"Writing model {model_definition} metadata")
        except Exception as ex:
            raise LayerClientException(f"Error while storing model, {ex}")
        else:
            self.logger.debug(
                f"User model {model_definition.mlflow_model_name} saved successfully on path {path}"
            )

    def get_model_signature(self, model_input, model_output) -> Any:
        return (
            infer_signature(model_input, model_output).to_dict()
            if model_input is not None
            else None
        )

    def retrieve(self, model_definition: ModelDefinition) -> ModelObject:
        """
        Retrieves the given model definition from the storage and returns the actual
        model object

        Args:
            model_definition: Model metadata object which describes the model instance
        Returns:
            Loaded model object

        """
        self.logger.debug(
            f"User requested to load model {model_definition.model_name} "
        )
        path = model_definition.mlflow_model_name
        flavor: ModelFlavor = self.get_model_flavor_by_key(model_definition.flavor_key)
        try:
            self.client.get_model_version(model_definition.mlflow_model_name, 1)
        except RestException:
            raise LayerClientException(
                f"Model named {model_definition.model_name} not found"
            )
        self.logger.debug(
            f"Loading model {model_definition.model_name} from path {path}"
        )
        module = importlib.import_module(flavor.metadata.module_name)
        model_flavor_class = getattr(module, flavor.metadata.class_name)
        return model_flavor_class().load(model_name=model_definition.mlflow_model_name)

    def delete(self, model_definition: ModelDefinition) -> None:
        """
        Deletes the model along with its metadata from the storage

        Args:
            model_definition: Model metadata object which describes the model instance
        """
        self.logger.debug(
            f"User requested to delete model {model_definition.model_name}"
        )
        self.client.delete_registered_model(name=model_definition.model_name)
        self.logger.debug(f"Deleted model {model_definition.model_name}")

    @staticmethod
    def get_model_flavor(
        model_object: ModelObject,
    ) -> Tuple[str, ModelFlavor]:
        """
        Checks if given model objects has a known model flavor and returns
        the flavor if there is a match.

        Args:
            model_object: User supplied model object

        Returns:
            The corresponding model flavor if there is match

        Raises:
            LayerException if user provided object does not have a known flavor.

        """
        flavor = MLModelService.__check_and_get_flavor(model_object)
        if flavor is None:
            raise LayerClientException(f"Unexpected model type {type(model_object)}")
        return flavor

    @staticmethod
    def get_model_flavor_by_key(flavor_key: str) -> ModelFlavor:
        if flavor_key not in flavors.MODEL_FLAVORS:
            raise LayerClientException(f"Unexpected model flavor {type(flavor_key)}")
        return flavors.MODEL_FLAVORS[flavor_key]

    @staticmethod
    def check_object_has_known_flavor(model_object: ModelObject) -> bool:
        """
        Checks whether given model has a known flavor which we can work with

        Args:
            model_object: A machine learning model which could be originated
            from any framework

        Returns:
            bool result
        """
        return MLModelService.__check_and_get_flavor(model_object) is not None

    @staticmethod
    def __check_and_get_flavor(
        model_object: ModelObject,
    ) -> Optional[Tuple[str, ModelFlavor]]:
        for key, model_flavor in flavors.MODEL_FLAVORS.items():
            if model_flavor.can_interpret_object(model_object):
                return key, model_flavor
        return None

    def __get_or_create_experiment(self, experiment_name: str) -> Experiment:
        should_create = False
        experiment = None
        try:
            experiment = self.client.get_experiment_by_name(experiment_name)
            if experiment is None:
                should_create = True
        except RestException:
            should_create = True
        if should_create:
            experiment_id = self.client.create_experiment(experiment_name)
            experiment = self.client.get_experiment(experiment_id)
        return experiment

    def __create_run(self, experiment_id: str) -> Run:
        tags = {
            MLFLOW_SOURCE_TYPE: "NOTEBOOK",
        }
        run = self.client.create_run(experiment_id=experiment_id, tags=tags)
        return run

    def __get_model_metrics(self, run_id: str) -> Dict[str, str]:
        return self.client.get_run(run_id).data.metrics

    def __get_model_parameters(self, run_id: str) -> Dict[str, Any]:
        return self.client.get_run(run_id).data.params
