import time
from typing import Any

from fastapi import Request
from starlette.responses import JSONResponse

from inferia.api.responses import ErrorResponse, ResultResponse
from inferia.core.models import BasePredictor


async def health_check_handler(request: Request) -> JSONResponse:
    if request.app.state.ready:
        return JSONResponse({"status": "OK"})
    else:
        return JSONResponse(
            {"status": "Starting"},
            status_code=503,
        )


def create_predictor_handler(predictor: BasePredictor, response_model: ResultResponse):
    async def handler(request: Request) -> Any:
        # Fixme convert request arguments to kwargs and pass them to the model
        try:
            start_time = time.time()
            result = predictor.predict(request)
            end_time = time.time() - start_time

            response = response_model(
                inference_time_seconds=end_time,
                input=request.query_params,
                result=result,
            )
            return response.model_dump()
        except Exception as e:
            error = ErrorResponse(message=str(e))
            return error.to_json_response()

    return handler
