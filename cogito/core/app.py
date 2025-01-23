import logging
import os
from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from cogito.core.exceptions import ConfigFileNotFoundError
from cogito.core.models import BasePredictor
from cogito.api.handlers import (
    health_check_handler,
)
from cogito.core.utils import wrap_handler
from cogito.core.config import ConfigFile
from cogito.core.utils import load_predictor


class Application:
    def __init__(
            self,
            config_file_path: str = "."
    ):

        try:
            self.config = ConfigFile.load_from_file(
                os.path.join(
                    f"{config_file_path}/cogito.yaml"
                )
            )
        except ConfigFileNotFoundError as e:
            logging.warning(f"Error loading config file: {e}. Using default configuration.")
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
            map_route_to_model[route.path] = route.predictor
            if route.predictor not in map_model_to_instance:
                predictor = load_predictor(route.predictor)
                try:
                    predictor.setup()
                except Exception as e:
                    print(f"Error setting up predictor {route.predictor}: {e}")
                    raise #fixme Use a custom exception

                map_model_to_instance[route.predictor] = predictor
            else:
                logging.info(f"Predictor {route.predictor} already loaded")
            logging.debug(f"Adding route {route.path} with predictor {route.predictor}")
            handler = wrap_handler(
                class_name=route.predictor,
                original_handler=getattr(map_model_to_instance.get(route.predictor), "predict"),
            )

            self.app.add_api_route(
                route.path,
                handler,
                methods=["POST"],
                name=route.name,
                description=route.description,
                tags=route.tags,
                response_model=handler.__annotations__["return"],
            )

        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "detail": "There is an error with the request parameters.",
                    "errors": exc.errors(),
                    "body": exc.body,
                },
            )
        self.app.add_exception_handler(
            RequestValidationError,
            validation_exception_handler
        )

    def run(self):
        uvicorn.run(
                self.app,
                host=self.config.cogito.server.fastapi.host,
                port=self.config.cogito.server.fastapi.port
        )