import importlib
<<<<<<< Updated upstream
from typing import Any
=======
import inspect
from typing import Any, Type

from pydantic import BaseModel, create_model, Field
>>>>>>> Stashed changes

from cogito.core.models import BasePredictor
from cogito.core.exceptions import InvalidHandlerSignature


def load_predictor(class_path) -> Any:
    predictor_path, predictor_class = class_path.split(":")
    module = importlib.import_module(f"{predictor_path}")

    if not hasattr(module, predictor_class):
        raise AttributeError(f"Class {predictor_class} not found in module {predictor_path}")

    predict_class = getattr(module, predictor_class)

    # Build an instance of the class
    predict_instance = predict_class()

    # Instantiate and return the class
    return predict_instance


<<<<<<< Updated upstream
def get_predictor_handler_return_type(predictor: BasePredictor):
    """This method returns the type of the output of the predictor.predict method"""
    return predictor.predict.__annotations__["return"]

def get_predictor_handler_params_type(predictor: BasePredictor):
    """This method returns the type of the input of the predictor.predict method"""
    annotations = predictor.predict.__annotations__  # NOQA

    params = {k: v for k, v in annotations.items() if k != 'return'}
    if not params:
        return object

    if len(params) != 1:
        raise InvalidHandlerSignature(f"Predict {predictor.__class__.__name__} method must have one and only one parameter")

    return list(params.values())[0]
=======
def build_basemodel_method_class(cls, method_name: str, model_name : str = "InputModel") -> Type[BaseModel]:
    """
    Generate a Pydantic BaseModel for the input parameters of a method.

    :param cls: The class containing the method.
    :param method_name: The name of the method to inspect.
    :param model_name: The name of the Pydantic BaseModel class to create.
    :return: A Pydantic BaseModel class representing the input parameters.

    >>> class MyClass:
    ...     def my_method(self, param1: int, param2):
    ...         return param1 + param2
    ...
    >>> InputModel = build_basemodel_method_class(MyClass, 'method')
    >>> type(InputModel)
    <class 'pydantic.main.BaseModel'>
    >>> InputModel.model_json_schema()
    {'title': 'InputModel', 'type': 'object', 'properties': {'param1': {'title': 'Param1', 'type': 'integer'}, 'param2': {'title': 'Param2', 'type': 'object'}}, 'required': ['param
    """
    method = getattr(cls, method_name)
    signature = inspect.signature(method)

    # Build a dictionary of fields for Pydantic BaseModel
    fields = {}
    for param_name, param in signature.parameters.items():
        if param_name == 'self':
            continue  # Skip the 'self' parameter
        annotation = param.annotation if param.annotation != inspect.Parameter.empty else Any
        default = param.default if param.default != inspect.Parameter.empty else ...
        fields[param_name] = (annotation, default)

    # Create a Pydantic BaseModel dynamically using create_model
    model = create_model(
        f"{method_name.capitalize()}{model_name}",
        **fields
    )
    return model


def get_response_base_model(cls, method_name: str = "predict") -> Any:
    """
    Retrieve the return type annotation of a method.

    :param cls: The class containing the method.
    :param method_name: The name of the method to inspect.
    :return: The return type annotation of the method, or Any if not specified.
    """
    method = getattr(cls, method_name)
    signature = inspect.signature(method)
    return signature.return_annotation if signature.return_annotation != inspect.Signature.empty else Any
>>>>>>> Stashed changes
