from fastapi import Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest


async def health_check_handler(request: Request) -> JSONResponse:
    if request.app.state.ready:
        return JSONResponse({"status": "OK"})
    else:
        return JSONResponse(
            {"status": "Starting"},
            status_code=503,
        )


async def metrics_handler(request: Request) -> Response:
    return Response(content=generate_latest(), media_type="text/plain")
