from typing import Any, Optional

from pydantic import BaseModel, Field

from cogito import BasePredictor


class Text2ImageResponse(BaseModel):
    image: str
    text: str

class Text2ImageRequest(BaseModel):
    image: str = Field(..., description="Image URL")
    scale: float = Field(... , description="Scale factor")

class Text2Image(BasePredictor):
    def predict(self,
        text2image_request: Text2ImageRequest,
    ) -> Text2ImageResponse:
        return Text2ImageResponse(
            image="https://example.com/image.jpg",
            text="Hello world"
        )

    def setup(self):
        pass


class Image2TextResponse(BaseModel):
    text: str

class Image2Text(BasePredictor):
    def predict(self, instruction: Image2TextResponse) -> Any:
        pass

    def setup(self):
        pass


class StejonRequest(BaseModel):
    command: str


class STejon(BasePredictor):
    def predict(self, command: StejonRequest) -> Any:
        return "No doy permisos de root"

    def setup(self):
        pass