import logging

from pydantic import BaseModel, Field

from inferia import BasePredictor


class PredictResponse(BaseModel):
    image: str
    text: str


class Predictor(BasePredictor):
    def predict(
            self, prompt: str, temperature: float = Field(0.5,
                                                          description="Temperature is the most important attribute for an inference",
                                                          gt=0.0, lt=1.0)
            ) -> PredictResponse:
        return PredictResponse(
                image="https://example.com/image.jpg", text="Hello world"
        )

    async def setup(self):
        logging.info("I'm ready")
