import importlib
import inspect
from typing import Any, Callable

from cogito.core.models import BasePredictor
from cogito.core.exceptions import InvalidHandlerSignature


def load_predictor(class_path) -> Any:
    predictor_path, predictor_class = class_path.split(":")
    module = importlib.import_module(f"{predictor_path}")

    if not hasattr(module, predictor_class):
        raise AttributeError(
            f"Class {predictor_class} not found in module {predictor_path}"
        )

    predict_class = getattr(module, predictor_class)

    # Build an instance of the class
    predict_instance = predict_class()

    # Instantiate and return the class
    return predict_instance
