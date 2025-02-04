import asyncio
import importlib
import inspect
import logging
import os
import time
from inspect import Parameter, signature
from typing import Any, Callable, Dict, get_type_hints

from pydantic import create_model, Field

from inferia.api.responses import ErrorResponse, ResultResponse
from inferia.core.config import InferiaConfig
from inferia.core.exceptions import ModelDownloadError, NoThreadsAvailableError
from inferia.core.metrics import inference_duration_histogram
from inferia.core.model_store import download_gcp_model, download_huggingface_model
from inferia.core.models import BasePredictor


def load_predictor(class_path) -> Any:
    predictor_path, predictor_class = class_path.split(":")
    module = importlib.import_module(f"{predictor_path}")

    if not hasattr(module, predictor_class):
        raise AttributeError(
            f"Class {predictor_class} not found in module {predictor_path}"
        )

    predict_class = getattr(module, predictor_class)

    # Build an instance of the class
    predict_instance = predict_class()

    # Instantiate and return the class
    return predict_instance


def get_predictor_handler_return_type(predictor: BasePredictor):
    """This method returns the type of the output of the predictor.predict method"""
    # Get the return type of the predictor.predict method
    return_type = predictor.predict.__annotations__.get("return", None)

    # Create a new dynamic type based on ResultResponse, with the correct module and annotated field
    return_class = type(
        f"{predictor.__class__.__name__}Response",
        (ResultResponse,),
        {
            "__annotations__": {
                "result": return_type
            },  # Annotate the result field with the return type
            "__module__": ResultResponse.__module__,  # Ensure the module is set correctly for Pydantic
        },
    )

    return return_class


def wrap_handler(
    descriptor: str,
    original_handler: Callable,
    response_model: ResultResponse,
    semaphore: asyncio.Semaphore = None,
) -> Callable:
    sig = signature(original_handler)
    type_hints = get_type_hints(original_handler)

    _, class_name = descriptor.split(":")

    input_fields = {}
    for name, param in sig.parameters.items():
        param_type = type_hints.get(name, Any)
        default_value = param.default if param.default != Parameter.empty else ...
        input_fields[name] = (param_type, Field(default=default_value))
    input_model = create_model(f"{class_name}Request", **input_fields)

    # Check if the original handler is an async function
    # Fixme Unify handler after replacing status checking model with file based mode.
    if inspect.iscoroutinefunction(original_handler):

        async def handler(input: input_model):
            async def a_timed_handler(input):
                result = None
                try:
                    start_time = time.time()
                    result = await original_handler(**input.model_dump())
                    end_time = time.time() - start_time
                    inference_duration_histogram.record(
                        end_time * 1000, {"predictor": class_name, "async": True}
                    )
                    # todo Count successful requests
                except Exception as e:
                    logging.exception(e)
                    # todo Count failed requests
                    return ErrorResponse(message=str(e)).to_json_response()

                return response_model(
                    inference_time_seconds=end_time,
                    input=input.model_dump(),
                    result=result,
                )

            if not semaphore:
                return await a_timed_handler(input)
            else:
                if semaphore.locked():
                    raise NoThreadsAvailableError(descriptor)
                await semaphore.acquire()
                try:
                    return await a_timed_handler(input)
                finally:
                    semaphore.release()

    else:

        def handler(input: input_model):
            def timed_handler(intput: input_model):
                result = None
                try:
                    start_time = time.time()
                    result = original_handler(**input.model_dump())
                    end_time = time.time() - start_time
                    inference_duration_histogram.record(
                        end_time * 1000, {"predictor": class_name, "async": False}
                    )
                    # todo Count successful requests
                except Exception as e:
                    logging.exception(e)
                    # todo Count failed requests
                    return ErrorResponse(message=str(e)).to_json_response()

                return response_model(
                    inference_time_seconds=end_time,
                    input=input.model_dump(),
                    result=result,
                )

            if not semaphore:
                return timed_handler(input)
            else:
                if semaphore.locked():
                    raise NoThreadsAvailableError(descriptor)
                semaphore.acquire()
                try:
                    return timed_handler(input)
                finally:
                    semaphore.release()

    handler.__annotations__ = {"input": input_model, "return": response_model}
    logging.debug(
        f"Handler of {original_handler.__name__} annotated with {handler.__annotations__}"
    )
    return handler


def model_download(model_path: str) -> str:
    """
    Download a model from various sources based on the model path format.
    Supported formats:
    - Google Cloud Storage: gs://bucket/path/to/model
    - Hugging Face: repo_owner/repo_name
    """
    cache_dir = os.getenv("INFERIA_HOME")
    os.environ["HF_HOME"] = cache_dir

    try:
        if model_path.startswith("gs://"):
            return download_gcp_model(model_path, cache_dir)
        return download_huggingface_model(model_path, cache_dir)
    except Exception as e:
        raise ModelDownloadError(model_path, e)


def create_routes_semaphores(config: InferiaConfig) -> Dict[str, asyncio.Semaphore]:
    semaphores = {}
    route = config.server.route
    semaphores[route.predictor] = asyncio.Semaphore(config.server.threads)

    return semaphores


# Dependencia para limitar la concurrencia
async def limit_concurrent_requests(semaphore: asyncio.Semaphore):
    await semaphore.acquire()  # Bloquea si se alcanzó el límite

    try:
        yield  # Ejecuta la lógica de la ruta
    finally:
        semaphore.release()  # Libera el semáforo al finalizar
