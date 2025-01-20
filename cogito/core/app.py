import uvicorn
from fastapi import FastAPI

from cogito.api.handlers import create_model_handler, health_check_handler


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
        routes = [
            {'path': '/v1/predict/text2image', 'predictor_class': "text2image"},
            {'path': '/v1/predict/image2image', 'predictor_class': "image2image"},
        ] # fixme Add real routes here

        for route in routes:
            self.app.add_api_route(
                    route['path'],
                    create_model_handler(route['predictor_class']),
                    methods=["POST"],
                    name=route['model'],
                    description=f"Predict using the {route['predictor_class']} predictor class",
                    tags=[route['model']],
            )

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)