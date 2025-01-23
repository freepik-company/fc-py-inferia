from typing import Any, Optional

from pydantic import BaseModel, Field

from cogito import BasePredictor

"""
This is a pythonic way to import the Application class from the cogito package from examples folder without being
a package itself. This is a common pattern in the Python world. 
"""

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

############################################################################################################

class Image2Text(BasePredictor):
    async def predict(self, a, b) -> int:
        return 23

    def setup(self):
        pass

############################################################################################################

class STejon(BasePredictor):
    def predict(self, prompt: str, elasticity: float):
        return "No doy permisos de root"

    def setup(self):
        pass