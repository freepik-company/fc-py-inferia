from fastapi import Request

from cogito.core.utils import load_predictor


async def health_check_handler(request: Request) -> dict:
    return {"status": "OK"}

def create_model_handler(model):
    async def handler(request: Request) -> dict:
        predictor = load_predictor(model)
        predictor.setup()
        return {"model": model}

    return handler