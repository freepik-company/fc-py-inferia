import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Union

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from inferia.api.handlers import (
    health_check_handler,
)
from inferia.core.utils import wrap_handler
from inferia.api.responses import ErrorResponse
from inferia.core.config import ConfigFile
from inferia.core.exceptions import (
    ConfigFileNotFoundError,
    SetupError,
)
from inferia.core.logging import get_logger
from inferia.core.models import BasePredictor
from inferia.core.utils import (
    get_predictor_handler_return_type,
    load_predictor,
)
from examples.fastapi_sandbox import lifespan


class Application:
    _logger: logging.Logger
    ready : bool

    def __init__(
            self,
            config_file_path: str = ".",
            logger: Union[Any, logging.Logger] = None,
    ):

        self._logger = logger or Application._get_default_logger()

        try:
            self.config = ConfigFile.load_from_file(
                    os.path.join(
                            f"{config_file_path}/inferia.yaml"
                    )
            )
        except ConfigFileNotFoundError as e:
            self._logger.warning("config file does not exist. Using default configuration.", extra={
                'error': str(e),
                'config_file_path': config_file_path
            })
            self.config = ConfigFile.default()

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            asyncio.create_task(self.setup(app))
            yield

        self.app = FastAPI(
                title=self.config.inferia.server.name,
                version=self.config.inferia.server.version,
                description=self.config.inferia.server.description,
                access_log=self.config.inferia.server.fastapi.access_log,
                debug=self.config.inferia.server.fastapi.debug,
                lifespan=lifespan,
        )
        self.app.state.ready = False

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

        map_route_to_model: Dict[str, str] = {}
        self.map_model_to_instance: Dict[str, BasePredictor] = {}

        for route in self.config.inferia.server.routes:
            self._logger.info("Adding route", extra={'route': route})
            map_route_to_model[route.path] = route.predictor
            if route.predictor not in self.map_model_to_instance:
                predictor = load_predictor(route.predictor)
                self.map_model_to_instance[route.predictor] = predictor
            else:
                self._logger.info("Predictor class already loaded", extra={'predictor': route.predictor})


            handler = wrap_handler(
                class_name=route.predictor,
                original_handler=getattr(
                    self.map_model_to_instance.get(route.predictor),
                    "predict"))

            self.app.add_api_route(
                    route.path,
                    handler,
                    methods=["POST"],
                    name=route.name,
                    description=route.description,
                    tags=route.tags,
                    response_model=handler.__annotations__["return"],
                responses={500: {"model": ErrorResponse}},
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

    async def setup(self, app: FastAPI):
        self._logger.info("Setting up application", extra={})
        for predictor in self.map_model_to_instance.values():
            try:
                self._logger.debug("Setting up predictor", extra={'predictor': predictor.__class__.__name__})
                await predictor.setup()
            except Exception as e:
                self._logger.critical("Unable to setting up predictor", extra={
                    'predictor': predictor.__class__.__name__, 'error': e
                })
                raise SetupError(predictor.__class__.__name__, e)
        app.state.ready = True

    def run(self):
        uvicorn.run(
                self.app,
                host=self.config.inferia.server.fastapi.host,
                port=self.config.inferia.server.fastapi.port
        )

    @classmethod
    def _get_default_logger(cls):
        return get_logger("inferia.app")
