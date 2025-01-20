from fastapi import Request

async def health_check_handler(request: Request) -> dict:
    return {"status": "OK"}

def create_model_handler(model):
    async def handler(request: Request) -> dict:
        return {"model": model}

    return handler