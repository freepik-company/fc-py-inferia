import importlib
import inspect
import logging
from inspect import signature, Parameter
from typing import Any, Callable, get_type_hints

from pydantic import Field, create_model

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


def validate_and_wrap_handler(class_name: str, original_handler: Callable) -> Callable:
    sig = signature(original_handler)
    type_hints = get_type_hints(original_handler)

    input_fields = {}
    for name, param in sig.parameters.items():
        param_type = type_hints.get(name, Any)
        default_value = param.default if param.default != Parameter.empty else ...
        input_fields[name] = (param_type, Field(default=default_value))
    InputModel = create_model(f"{class_name}.Input", **input_fields)

    # Check if the original handler is an async function
    if inspect.iscoroutinefunction(original_handler):
        async def handler(input: InputModel):
            result = await original_handler(**input.model_dump())
            return result
    else:
        def handler(input: InputModel):
            return original_handler(**input.model_dump())

    handler.__annotations__ = {
        "input": InputModel,
        'return': type_hints.get("return", Any)
    }
    logging.debug(f"Handler of {original_handler.__name__} annotated with {handler.__annotations__}")
    return handler
