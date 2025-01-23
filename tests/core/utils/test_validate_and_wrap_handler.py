from pydantic import BaseModel
import pytest

from cogito.core.utils import validate_and_wrap_handler

def test_validate_and_wrap_handler_str_input_str_output():
    class MockPredictor:
        def predict(self, input: str) -> str:
            return f"Hello, {input}"

    original_handler = MockPredictor().predict
    wrapped_handler = validate_and_wrap_handler("MockPredictor", original_handler)

    class InputModel(BaseModel):
        input: str

    input_data = InputModel(input="World")
    response = wrapped_handler(input_data)
    assert response == "Hello, World"


def test_validate_and_wrap_handler_float_input_int_output():
    class MockPredictor:
        def predict(self, input: float) -> int:
            return int(input)

    original_handler = MockPredictor().predict
    wrapped_handler = validate_and_wrap_handler("MockPredictor", original_handler)

    class InputModel(BaseModel):
        input: float

    input_data = InputModel(input=3.14)
    response = wrapped_handler(input_data)
    assert response == 3


def test_validate_and_wrap_handler_pydantic_input_str_output():

    class MyModel(BaseModel):
        input: str

    class MockPredict:
        def predict(self, input: MyModel) -> str:
            return f"Hello, {input}"

    original_handler = MockPredict().predict
    wrapped_handler = validate_and_wrap_handler("MockPredict", original_handler)

    input_data = MyModel(input="World")
    response = wrapped_handler(input_data)
    assert response == "Hello, World"