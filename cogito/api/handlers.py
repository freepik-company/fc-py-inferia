from fastapi import Request
from fastapi.responses import JSONResponse


async def health_check_handler(request: Request) -> JSONResponse:
    return JSONResponse(
        content={"status": "ok"},
    )


