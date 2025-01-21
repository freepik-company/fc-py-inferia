import logging
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
        except FileNotFoundError as e:
            logging.info(f"Config file not found: {file_path}. Empty config will be used. {e}")
        except Exception as e:
            logging.error(f"Error loading config file: {file_path}. Empty config will be used. {e}")
        finally:
            logging.debug(f"Starting up with empty config.")
            return cls(
                    name="Cogito ergo sum",
                    description="An API for inference and reasoning with an amazing user interface",
                    routes=[],
                    version="1.0.0",
            )
        
    def save_to_file(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            yaml.dump(self.model_dump(), file)


