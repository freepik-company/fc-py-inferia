import sys
import os
from typing import Any

from cogito import BasePredictor

"""
This is a pythonic way to import the Application class from the cogito package from examples folder without being
a package itself. This is a common pattern in the Python world. 
"""
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

class Text2Image(BasePredictor):
    def predict(self, **kwargs) -> Any:
        pass

    def setup(self):
        pass

class Image2Text(BasePredictor):
    def predict(self, **kwargs) -> Any:
        pass

    def setup(self):
        pass

class STejon(BasePredictor):
    def predict(self, **kwargs) -> Any:
        pass

    def setup(self):
        raise NotImplementedError("No doy permisos de root")