import inspect

from fastapi import Request, Response, Depends
from pydantic import BaseModel

from cogito.core.models import BasePredictor
from cogito.core.utils import get_predictor_handler_params_type
from cogito.core.exceptions import InvalidHandlerSignature

async def health_check_handler(request: Request) -> Response:
    return Response(
        content={"status": "ok"},
        media_type="application/json",
    )

def create_predictor_handler(predictor: BasePredictor):

    param_type = get_predictor_handler_params_type(predictor)
    if not issubclass(param_type, BaseModel):
        raise InvalidHandlerSignature(f"Predict {predictor.__class__.__name__}")

    async def handler(
        request: param_type = Depends(),
    ):
        # Fixme convert request arguments to kwargs and pass them to the model
        return predictor.predict(request)
    handler.__annotations__ = {"return": Any}
    return handler

from inspect import signature, Parameter
from functools import wraps
from typing import Callable, Any, get_type_hints
from pydantic import Field, create_model

# Wrapper que crea un nuevo handler con anotaciones mejoradas
def wrapper(original_handler: Callable):
    sig = signature(original_handler)
    type_hints = get_type_hints(original_handler)

    # Crear un modelo Pydantic para los parámetros de entrada
    input_fields = {}
    for name, param in sig.parameters.items():
        param_type = type_hints.get(name, Any)
        default_value = param.default if param.default != Parameter.empty else ...
        input_fields[name] = (param_type, Field(default=default_value))
    InputModel = create_model(f"{original_handler.__name__}Input", **input_fields)

    # Tipo de salida
    output_type = type_hints.get('return', Any)

    # Check if the original handler is an async function
    if inspect.iscoroutinefunction(original_handler):
        async def handler(*args, **kwargs):
            # Validar entrada usando el modelo Pydantic
            input_data = InputModel(**kwargs)
            kwargs.update(input_data.model_dump())  # Actualizar con los datos validados
            result = await original_handler(*args, **kwargs)
            return result
    else:
        def handler(*args, **kwargs):
            # Validar entrada usando el modelo Pydantic
            input_data = InputModel(**kwargs)
            kwargs.update(input_data.model_dump())  # Actualizar con los datos validados
            result = original_handler(*args, **kwargs)
            return result

    # Añadir anotaciones al nuevo handler
    handler.__annotations__ = {
        **{name: type_hints.get(name, Any) for name in sig.parameters},
        'return': output_type,
    }
    return handler
