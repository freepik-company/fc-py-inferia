from typing import Any

from cogito.core.utils import get_response_base_model

def test_get_return_signature_any():
    class MyClass:
        def method(self, param1: int, param2):
            return param1 + param2

    return_type = get_response_base_model(MyClass, 'method')
    assert return_type == Any

def test_get_return_signature_int():
    class MyClass:
        def method(self, param1: int, param2: int) -> int:
            return param1 + param2

    return_type = get_response_base_model(MyClass, 'method')
    assert return_type == int

def test_get_return_signature_float():
    class MyClass:
        def method(self, param1: int, param2: int) -> float:
            return param1 + param2

# boolean type
def test_get_return_signature_bool():
    class MyClass:
        def method(self, param1: int, param2: int) -> bool:
            return param1 + param2

    return_type = get_response_base_model(MyClass, 'method')
    assert return_type == bool

def test_get_return_signature_str():
    class MyClass:
        def method(self, param1: int, param2: int) -> str:
            return param1 + param2

    return_type = get_response_base_model(MyClass, 'method')
    assert return_type == str