from typing import Dict

from ...api.entity.model_pb2 import Model
from .flavor import (
    KerasModelFlavor,
    LightGBMModelFlavor,
    ModelFlavor,
    PyTorchModelFlavor,
    ScikitLearnModelFlavor,
    SparkMLModelFlavor,
    TensorFlowModelFlavor,
    XGBoostModelFlavor,
)


PROTO_TO_PYTHON_FLAVORS: Dict["Model.ModelFlavor", ModelFlavor] = {
    Model.ModelFlavor.Value("MODEL_FLAVOR_SPARK"): SparkMLModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_SKLEARN"): ScikitLearnModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_PYTORCH"): PyTorchModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_XGBOOST"): XGBoostModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_LIGHTGBM"): LightGBMModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_KERAS"): KerasModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_TENSORFLOW"): TensorFlowModelFlavor(),
}
