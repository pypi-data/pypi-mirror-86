from typing import Dict

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


MODEL_FLAVORS: Dict[str, ModelFlavor] = {
    "SparkMLModelFlavor": SparkMLModelFlavor(),
    "ScikitLearnModelFlavor": ScikitLearnModelFlavor(),
    "PyTorchModelFlavor": PyTorchModelFlavor(),
    "XGBoostModelFlavor": XGBoostModelFlavor(),
    "LightGBMModelFlavor": LightGBMModelFlavor(),
    "KerasModelFlavor": KerasModelFlavor(),
    "TensorFlowModelFlavor": TensorFlowModelFlavor(),
}
