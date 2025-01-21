from typing import Any

from fastapi import Request

from cogito.core.models import BasePredictor

async def health_check_handler(request: Request) -> dict:
    return {"status": "OK"}

def create_predictor_handler(predictor: BasePredictor):
    async def handler(request: Request) -> Any:
        # Fixme convert request arguments to kwargs and pass them to the model
        return predictor.predict(request)

    return handler

