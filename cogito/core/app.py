import uvicorn
from fastapi import FastAPI

from cogito.api.handlers import create_model_handler, health_check_handler
from cogito.core.config import ConfigFile


class Application:
    def __init__(
            self,
            config_file_path: str = "."
    ):

        self.config = ConfigFile.load_from_file(f"{config_file_path}/cogito.yaml")

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
            self.app.add_api_route(
                    route.path,
                    create_model_handler(route.predictor),
                    methods=["POST"],
                    name=route.name,
                    description=route.description,
                    tags=route.tags,
            )

    def run(self):
        uvicorn.run(
                self.app,
                host=self.config.cogito.server.fastapi.host,
                port=self.config.cogito.server.fastapi.port
        )