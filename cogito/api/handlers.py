from typing import Any

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

    return handler

