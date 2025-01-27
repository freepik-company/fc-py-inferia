import logging
import asyncio
from typing import Any

from pydantic import BaseModel

from cogito import BasePredictor


class PredictResponse(BaseModel):
    image: str
    text: str


class GoodPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> PredictResponse:
        return PredictResponse(
            image="https://example.com/image.jpg", text="Hello world"
        )

    async def setup(self):
        await asyncio.sleep(10)
        logging.info("I'm ready")


class DelayPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> PredictResponse:
        asyncio.sleep(5)
        return PredictResponse(
            image="https://example.com/image.jpg", text="Hello world"
        )

    async def setup(self):
        await asyncio.sleep(10)
        logging.info("I'm ready")


class BadPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> Any:
        raise Exception("No doy permisos de root")

    async def setup(self):
        await asyncio.sleep(10)
        logging.info("I'm ready")
