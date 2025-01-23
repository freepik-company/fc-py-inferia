import importlib
from typing import Any

from cogito.api.responses import ResultResponse
from cogito.core.models import BasePredictor


def load_predictor(class_path) -> Any:
    predictor_path, predictor_class = class_path.split(":")
    module = importlib.import_module(f"{predictor_path}")

    if not hasattr(module, predictor_class):
        raise AttributeError(f"Class {predictor_class} not found in module {predictor_path}")

    predict_class = getattr(module, predictor_class)

    # Build an instance of the class
    predict_instance = predict_class()

    # Instantiate and return the class
    return predict_instance


def get_predictor_handler_return_type(predictor: BasePredictor):
    """This method returns the type of the output of the predictor.predict method"""
    # Get the return type of the predictor.predict method
    return_type = predictor.predict.__annotations__.get("return", None)

    # Create a new dynamic type based on ResultResponse, with the correct module and annotated field
    return type(
            f"{predictor.__class__.__name__}Response",
            (ResultResponse,),
            {
                "__annotations__": {"result": return_type},  # Annotate the result field with the return type
                "__module__": ResultResponse.__module__,  # Ensure the module is set correctly for Pydantic
            },
    )
