from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel

from inferia.core.exceptions import ConfigFileNotFoundError


class ArgConfig(BaseModel):
    name: str
    type: str
    description: Optional[str] = None


class ResponseConfig(BaseModel):
    type: str
    description: Optional[str] = None


class RouteConfig(BaseModel):
    """
    Route configuration.
    """

    name: str
    description: Optional[str] = None
    path: str
    predictor: str
    args: Optional[List["ArgConfig"]] = None
    response: Optional["ResponseConfig"] = None
    tags: List[str] = List

    @classmethod
    def default(cls):
        return cls(
                name="Predict",
                description="Make a single prediction",
                path="/v1/predict",
                predictor="predict:Predictor",
                args=[
                    ArgConfig(
                            name="prompt",
                            type="str",
                            description="The prompt to generate text from",
                    )
                ],
                response=ResponseConfig(
                        type="PredictResponse", description="The generated text"
                ),
                tags=["predict"],
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
    version: Optional[str] = "1.0.0"
    fastapi: FastAPIConfig
    route: RouteConfig
    cache_dir: str = None
    threads: int

    @classmethod
    def default(cls):
        return cls(
                name="Sapientia per Inferentiam",
                description="Inference server",
                version="0.1.0",
                fastapi=FastAPIConfig.default(),
                route=RouteConfig.default(),
                cache_dir="/tmp/inferia",
                threads=1,
        )


class TrainingConfig(BaseModel):
    """
    Training configuration.
    """

    pass

    @classmethod
    def default(cls):
        return cls()


class InferiaConfig(BaseModel):
    """
    Inferia configuration.
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

    inferia: InferiaConfig

    @classmethod
    def default(cls):
        return cls(inferia=InferiaConfig.default())

    @classmethod
    def exists(cls, file_path: str) -> bool:
        return Path(file_path).exists()

    @classmethod
    def load_from_file(cls, file_path: str) -> "ConfigFile":
        try:
            with open(file_path, "r") as file:
                yaml_data = yaml.safe_load(file)
            return cls(**yaml_data)
        except FileNotFoundError:
            raise ConfigFileNotFoundError(file_path)
        except Exception:
            raise ValueError(f"Error loading configuration file {file_path}")

    def save_to_file(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            yaml.dump(self.model_dump(), file)
