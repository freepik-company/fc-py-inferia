import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from threading import Thread
import time
import sys

from starlette.responses import JSONResponse


class CustomFastAPI(FastAPI):
    """
    Clase personalizada que hereda de FastAPI.
    Realiza validaciones antes de iniciar el servicio.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state.ready = False
        print("Iniciando aplicación...")
        print(f"Aplicación lista: {self.state.ready}")

    def validate_before_start(self):
        """
        Método para realizar validaciones antes de iniciar el servicio.
        Si falla la validación, detiene la aplicación.
        """
        try:
            print("Realizando validaciones antes de iniciar...")
            # Simula una validación (reemplázala con tu lógica)
            asyncio.sleep(10)
            if not self.custom_validation_logic():
                raise Exception("Falló la validación")
            print("Validaciones completadas con éxito.")
        except Exception as e:
            print(f"Error en validaciones: {e}", file=sys.stderr)
            sys.exit(1)  # Apagar la aplicación si falla la validación

    @staticmethod
    def custom_validation_logic():
        """
        Simula lógica de validación.
        Devuelve True si la validación es exitosa, False si falla.
        """
        # Cambia a `False` para simular un fallo
        return True


@asynccontextmanager
async def lifespan(app: CustomFastAPI):
    """
    Hook que se ejecuta al inicio de la aplicación.
    """

    asyncio.create_task(initialize_app(app))

    yield


# Crear instancia de la clase personalizada
app = CustomFastAPI(lifespan=lifespan)


@app.get("/healthz")
async def healthz():
    """
    Endpoint de salud que devuelve:
    - 200 si la aplicación está lista.
    - 400 si la aplicación aún no está lista.
    """
    if app.state.ready:
        return JSONResponse({"status": "OK"})
    return JSONResponse({"status": "Initializing"}, 400)


async def initialize_app(app: CustomFastAPI):
    """
    Simula la inicialización de la aplicación.
    """
    try:
        print("Iniciando tareas de inicialización...")
        await asyncio.sleep(20)  # Simula tareas largas
        print("Inicialización completada.")
        app.state.ready = True
    except Exception as e:
        print(f"Error durante la inicialización: {e}", file=sys.stderr)
        sys.exit(1)  # Apagar la aplicación si falla la inicialización


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
