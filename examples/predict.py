import logging
import os
import sys
import asyncio
from typing import Any

from pydantic import BaseModel

from cogito import BasePredictor

"""
This is a pythonic way to import the Application class from the cogito package from examples folder without being
a package itself. This is a common pattern in the Python world. 
"""
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)


class PredictResponse(BaseModel):
    image: str
    text: str


class GoodPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> PredictResponse:
        return PredictResponse(
                image="https://example.com/image.jpg",
                text="Hello world"
        )

    async def setup(self):
        await asyncio.sleep(10)
        logging.info("I'm ready")


class DelayPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> PredictResponse:
        asyncio.sleep(5)
        return PredictResponse(
                image="https://example.com/image.jpg",
                text="Hello world"
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

