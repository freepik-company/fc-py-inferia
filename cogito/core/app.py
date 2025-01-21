from pathlib import Path

import uvicorn
from fastapi import FastAPI

from cogito.api.handlers import create_model_handler, health_check_handler
from cogito.core.config import ConfigFile


class Application:
    def __init__(
            self,
            title: str = "Cogito ergo sum",
            version: str = "0.1.0",
            description: str = "An API for inference and reasoning with an amazing user interface",
            host: str = "127.0.0.1",
            port: int = 8000,
            show_fastapi_access_logs: bool = True,
            debug_mode: bool = False,
    ):

        self.host = host
        self.port = port
        self.debug_mode = debug_mode

        self.app = FastAPI(
            title=title,
            version=version,
            description=description,
            access_log=show_fastapi_access_logs,
            debug=debug_mode,
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
        config = ConfigFile.load_from_file(f"{Path.cwd()}/cogito.yaml")

        for route in config.routes:
            self.app.add_api_route(
                    route.path,
                    create_model_handler(route.predictor),
                    methods=["POST"],
                    name=route.name,
                    description=route.description,
                    tags=route.tags,
            )

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)