import logging
import inspect

from fastapi import Request
from fastapi.responses import JSONResponse
from inspect import signature, Parameter
from typing import Callable, Any, get_type_hints

from pydantic import Field, create_model, ValidationError


async def health_check_handler(request: Request) -> JSONResponse:
    return JSONResponse(
        content={"status": "ok"},
    )


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

    # Añadir anotaciones al nuevo handler
    handler.__annotations__ = {
        "input": InputModel,
        'return': type_hints.get("return", Any)
    }
    logging.debug(f"Handler of {original_handler.__name__} annotated with {handler.__annotations__}")
    return handler
