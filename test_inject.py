from inject import injectinator
from abc import ABC, abstractmethod


# Classes to test injection with
class BaseClass(ABC):
    @abstractmethod
    def test_method(self, arg1: int = 1) -> int:
        raise NotImplemented("test_method Not implemented")

class ClassA(BaseClass):
    def test_method(self, arg1: int = 1) -> int:
        return arg1 + 1

class ClassB(BaseClass):
    def test_method(self, arg1: int = 1) -> int:
        return arg1 + 2

def test_inject_with_no_arguments_no_return():
    """No arguments, no return"""
    @injectinator
    def function_to_test() -> None:
        pass

    result = function_to_test()
    assert result is None

def test_inject_with_no_arguments_int_return():
    """No arguments, integer return"""
    @injectinator
    def function_to_test() -> int:
        return 1

    result = function_to_test()
    assert type(result) == int
    assert result == 1

def test_inject_with_positional_arguments_int_return():
    """One positional argument, integer return"""
    @injectinator
    def function_to_test(arg1: int) -> int:
        return arg1

    result = function_to_test(2)
    assert type(result) == int
    assert result == 2

def test_inject_with_injected_argument_int_return():
    """Positional argument with injected class and integer return"""
    @injectinator
    def function_to_test(arg1: int, arg2: BaseClass=ClassA) -> int:
        return arg2.test_method(arg1)

    result = function_to_test(0)
    assert type(result) == int
    assert result == 1

    result = function_to_test(0, ClassB())
    assert type(result) == int
    assert result == 2

    result = function_to_test(arg1=0)
    assert type(result) == int
    assert result == 1

    result = function_to_test(arg1=0, arg2=ClassB())
    assert type(result) == int
    assert result == 2
