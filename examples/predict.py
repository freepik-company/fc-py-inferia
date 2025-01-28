import asyncio
import logging
import time
from typing import Any

from pydantic import BaseModel

from inferia import BasePredictor


class PredictResponse(BaseModel):
    image: str
    text: str


class GoodPredictor(BasePredictor):
    def predict(self, prompt: str) -> PredictResponse:
        return PredictResponse(
                image="https://example.com/image.jpg", text="Hello world"
        )

    async def setup(self):
        await asyncio.sleep(2)
        logging.info("I'm ready")


class DelayPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> PredictResponse:
        time.sleep(5)
        return PredictResponse(
                image="https://example.com/image.jpg", text="Hello world"
        )

    async def setup(self):
        await asyncio.sleep(2)
        logging.info("I'm ready")


class BadPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> Any:
        raise Exception("No doy permisos de root")

    async def setup(self):
        await asyncio.sleep(2)
        logging.info("I'm ready")
