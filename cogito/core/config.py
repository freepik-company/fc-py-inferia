from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from pydantic import BaseModel
from pydantic.v1 import BaseSettings


class ConfigRoute(BaseModel):
    name: str
    description: Optional[str] = None
    path: str
    predictor: str
    tags: List[str] = List


class ConfigFile(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[str] = '1.0.0'
    routes: List[ConfigRoute] = List

    @classmethod
    def load_from_file(cls, file_path: str) -> "ConfigFile":
        try:
            with open(file_path, "r") as file:
                yaml_data = yaml.safe_load(file)
            return cls(**yaml_data)
        except Exception:
            return cls(
                    name="Cogito ergo sum",
                    description="An API for inference and reasoning with an amazing user interface",
                    routes=[],
                    version="1.0.0",
            )
        
    def save_to_file(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            yaml.dump(self.model_dump(), file)


