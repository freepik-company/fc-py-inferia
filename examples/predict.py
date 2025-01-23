import time
from typing import Any

from pydantic import BaseModel

from cogito import BasePredictor


class PredictResponse(BaseModel):
    image: str
    text: str

class GoodPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> PredictResponse:
        return PredictResponse(
                image="https://example.com/image.jpg",
                text="Hello world"
        )

    def setup(self):
        pass


class DelayPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> PredictResponse:
        time.sleep(5)
        return PredictResponse(
                image="https://example.com/image.jpg",
                text="Hello world"
        )

    def setup(self):
        pass


class BadPredictor(BasePredictor):
    def predict(self, *args, **kwargs) -> Any:
        raise Exception("No doy permisos de root")

    def setup(self):
        pass
