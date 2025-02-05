from abc import ABC, abstractmethod
from typing import Any


class BasePredictor(ABC):
    @abstractmethod
    def predict(self, **kwargs) -> Any:
        pass

    @abstractmethod
    async def setup(self):
        pass
