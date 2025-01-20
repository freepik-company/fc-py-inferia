import uvicorn
from fastapi import FastAPI


class Application:
    def __init__(
            self,
            title: str = "Cogito ergo sum",
            version: str = "0.1.0",
            description: str = "An API for inference and reasoning with an amazing user interface",
            host: str = "127.0.0.1",
            port: int = 8000,
            show_fastapi_access_logs: bool = True,
    ):

        self.host = host
        self.port = port

        self.app = FastAPI(
            title=title,
            version=version,
            description=description,
            access_log=show_fastapi_access_logs,
        )

        #self.app.include_router(router)

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)