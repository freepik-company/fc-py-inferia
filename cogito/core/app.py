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
    ):
        self.title = title
        self.version = version
        self.description = description
        self.host = host
        self.port = port

        self.app = FastAPI(
            title=self.title,
            version=self.version,
            description=self.description,
            docs_url="/",
            redoc_url=None,
        )

        #self.app.include_router(router)

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)