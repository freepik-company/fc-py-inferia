from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel

from cogito.core.exceptions import ConfigFileNotFoundError


class RouteConfig(BaseModel):
    """
    Route configuration.
    """
    name: str
    description: Optional[str] = None
    path: str
    predictor: str
    tags: List[str] = List

    @classmethod
    def default(cls):
        return cls(
                name='Predict',
                description='Make a single prediction',
                path='/v1/predict',
                predictor='predict:Predictor',
                tags=['predict']
        )


class FastAPIConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    access_log: bool = True

    @classmethod
    def default(cls):
        return cls()


class ServerConfig(BaseModel):
    """
    Server configuration.
    """
    name: str
    description: Optional[str] = None
    version: Optional[str] = '1.0.0'
    fastapi: FastAPIConfig
    routes: List[RouteConfig] = List

    @classmethod
    def default(cls):
        return cls(
                name='Cogito ergo infero',
                description='Inference server',
                version='0.1.0',
                fastapi=FastAPIConfig.default(),
                routes=[RouteConfig.default()]
        )


class TrainingConfig(BaseModel):
    """
    Training configuration.
    """
    pass

    @classmethod
    def default(cls):
        return cls()


class CogitoConfig(BaseModel):
    """
    Cogito configuration.
    """
    server: ServerConfig
    training: TrainingConfig

    @classmethod
    def default(cls):
        return cls(server=ServerConfig.default(), training=TrainingConfig.default())


class ConfigFile(BaseModel):
    """
    Configuration file.
    """
    cogito: CogitoConfig

    @classmethod
    def default(cls):
        return cls(cogito=CogitoConfig.default())

    @classmethod
    def exists(cls, file_path: str) -> bool:
        return Path(file_path).exists()

    @classmethod
    def load_from_file(cls, file_path: str) -> "ConfigFile":
        try:
            with open(file_path, "r") as file:
                yaml_data = yaml.safe_load(file)
            return cls(**yaml_data)
        except Exception:
            raise ConfigFileNotFoundError(file_path)

    def save_to_file(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            yaml.dump(self.model_dump(), file)
