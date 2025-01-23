import logging
import os
from typing import Any, Dict, Union

import uvicorn
from fastapi import FastAPI

from cogito.api.handlers import (
    create_predictor_handler,
    health_check_handler,
)
from cogito.api.responses import ErrorResponse
from cogito.core.config import ConfigFile
from cogito.core.exceptions import ConfigFileNotFoundError
from cogito.core.logging import get_logger
from cogito.core.models import BasePredictor
from cogito.core.utils import get_predictor_handler_return_type, load_predictor


class Application:
    _logger: logging.Logger

    def __init__(
            self,
            config_file_path: str = ".",
            logger: Union[Any, logging.Logger] = None,
    ):

        self._logger = logger or Application._get_default_logger()

        try:
            self.config = ConfigFile.load_from_file(
                    os.path.join(
                            f"{config_file_path}/cogito.yaml"
                    )
            )
        except ConfigFileNotFoundError as e:
            self._logger.warning("config file does not exist. Using default configuration.", extra={
                'error': str(e),
                'config_file_path': config_file_path
            })
            self.config = ConfigFile.default()

        map_route_to_model: Dict[str, str] = {}
        map_model_to_instance: Dict[str, BasePredictor] = {}

        self.app = FastAPI(
                title=self.config.cogito.server.name,
                version=self.config.cogito.server.version,
                description=self.config.cogito.server.description,
                access_log=self.config.cogito.server.fastapi.access_log,
                debug=self.config.cogito.server.fastapi.debug,
        )

        self.app.logger = self._logger

        """ Include default routes """
        self.app.add_api_route(
                "/health-check",
                health_check_handler,
                methods=["GET"],
                name="health_check",
                description="Health check endpoint",
                tags=["health"],
        )

        """ Include custom routes """

        for route in self.config.cogito.server.routes:
            self._logger.info("Adding route", extra={'route': route})
            map_route_to_model[route.path] = route.predictor
            if route.predictor not in map_model_to_instance:
                predictor = load_predictor(route.predictor)
                try:
                    predictor.setup()
                except Exception as e:
                    self._logger.critical("Unable to setting up predictor", extra={
                        'predictor': route.predictor, 'error': e
                    })
                    raise  # fixme Use a custom exception

                map_model_to_instance[route.predictor] = predictor
            else:
                self._logger.info("Predictor class already loaded", extra={'predictor': route.predictor})

            model = map_model_to_instance.get(route.predictor)
            response_model = get_predictor_handler_return_type(model)

            self.app.add_api_route(
                    route.path,
                    create_predictor_handler(model, response_model),  # fixme Handle None
                    methods=["POST"],
                    name=route.name,
                    description=route.description,
                    tags=route.tags,
                    response_model=response_model,
                    responses={500: {"model": ErrorResponse}},

            )

    def run(self):
        uvicorn.run(
                self.app,
                host=self.config.cogito.server.fastapi.host,
                port=self.config.cogito.server.fastapi.port
        )

    @classmethod
    def _get_default_logger(cls):
        return get_logger("cogito.app")
