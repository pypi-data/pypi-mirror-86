import importlib
from logging import Logger
from typing import Any, Optional, Tuple

from mlflow.models.signature import infer_signature

from layer_client.exceptions import LayerClientException
from layer_client.mlmodels import ModelObject, flavors
from layer_client.mlmodels.flavors.model_definition import ModelDefinition

from ..api.entity.model_pb2 import Model
from .flavors import ModelFlavor


class MLModelService:
    """
    Handles ML model lifecycle within the application. Users of this service can
    store/load/delete ML models.
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    def log_metric(self, notebook_id: str, key: str, value: float) -> None:
        pass

    # pytype: disable=annotation-type-mismatch # https://github.com/google/pytype/issues/640
    def store(
        self,
        model_definition: ModelDefinition,
        model_object: ModelObject,
        model_input: Any,
        model_output: Any,
        flavor: ModelFlavor,
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
        """
        self.logger.debug(
            f"Saving user model {model_definition.model_name}({model_object})"
        )
        if model_output is not None and model_input is None:
            raise LayerClientException(
                "Model input not found! Model output can be assigned only if model input is assigned"
            )
        try:
            self.logger.debug(f"Writing model {model_definition}")
            flavor.save(model_definition, model_object)
            self.logger.debug(
                f"User model {model_definition.model_name} saved successfully"
            )
        except Exception as ex:
            raise LayerClientException(f"Error while storing model, {ex}")

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
        flavor: ModelFlavor = self.get_model_flavor_from_proto(
            model_definition.proto_flavor
        )

        self.logger.debug(f"Loading model {model_definition.model_name}")
        module = importlib.import_module(flavor.metadata.module_name)
        model_flavor_class = getattr(module, flavor.metadata.class_name)
        return model_flavor_class().load(model_definition=model_definition)

    def delete(self, model_definition: ModelDefinition) -> None:
        """
        Deletes the model along with its metadata from the storage

        Args:
            model_definition: Model metadata object which describes the model instance
        """
        self.logger.debug(
            f"User requested to delete model {model_definition.model_name}"
        )
        pass

    @staticmethod
    def get_model_flavor(
        model_object: ModelObject,
    ) -> Tuple["Model.ModelFlavor", ModelFlavor]:
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
    def get_model_flavor_from_proto(proto_flavor: "Model.ModelFlavor") -> ModelFlavor:
        if proto_flavor not in flavors.PROTO_TO_PYTHON_FLAVORS:
            raise LayerClientException(f"Unexpected model flavor {type(proto_flavor)}")
        return flavors.PROTO_TO_PYTHON_FLAVORS[proto_flavor]

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
    ) -> Optional[Tuple["Model.ModelFlavor", ModelFlavor]]:
        for proto_flavor, model_flavor in flavors.PROTO_TO_PYTHON_FLAVORS.items():
            if model_flavor.can_interpret_object(model_object):
                return proto_flavor, model_flavor
        return None
