import logging

from pydantic import BaseModel

from inferia import BasePredictor


class PredictResponse(BaseModel):
    image: str
    text: str


class Predictor(BasePredictor):
    def predict(self, *args, **kwargs) -> PredictResponse:
        return PredictResponse(
            image="https://example.com/image.jpg", text="Hello world"
        )

    def setup(self):
        logging.info("I'm ready")
