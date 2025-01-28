from pydantic import BaseModel

from inferia.core.utils import wrap_handler


def test_wrap_handler_str_output():
    class MockPredictor:
        def predict(self, input: str) -> str:
            return f"Hello, {input}"

    original_handler = MockPredictor().predict
    wrapped_handler = wrap_handler("predict:MockPredictor", original_handler)

    class InputModel(BaseModel):
        input: str

    input_data = InputModel(input="World")
    response = wrapped_handler(input_data)
    assert response == "Hello, World"


def test_wrap_handler_float_input_int_output():
    class MockPredictor:
        def predict(self, input: float) -> int:
            return int(input)

    original_handler = MockPredictor().predict
    wrapped_handler = wrap_handler("predict:MockPredictor", original_handler)

    class InputModel(BaseModel):
        input: float

    input_data = InputModel(input=3.14)
    response = wrapped_handler(input_data)
    assert response == 3


def test_wrap_handler_base_model_input_str_output():

    class MyModel(BaseModel):
        input: str

    class MockPredict:
        def predict(self, input: MyModel) -> str:
            return f"Hello, {input}"

    original_handler = MockPredict().predict
    wrapped_handler = wrap_handler("predict:MockPredictor", original_handler)

    input_data = MyModel(input="World")
    response = wrapped_handler(input_data)
    assert response == "Hello, World"
    wrapped_handler_annotations = wrapped_handler.__annotations__
    assert issubclass(wrapped_handler_annotations["input"], BaseModel)
    assert wrapped_handler_annotations["return"] == str
