import functools  # This is only needed for debugging, you can remove
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def injectinator(func: Callable[P, R]) -> Callable[P, R]:
    """
    Very simple dependency injection wrapper that supplies concrete instances of specified class definitions from a functions specification
    """
    @functools.wraps(func)  # This is only needed for debugging, you can remove
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        replacements = dict(zip(
            func.__code__.co_varnames[:func.__code__.co_argcount],
            list(([None] * func.__code__.co_argcount) + list(func.__defaults__ or []))[-func.__code__.co_argcount:]
        ))
        for position, default in enumerate(replacements.keys()):
            if position >= len(args):
                if default not in kwargs and isinstance(replacements[default], type):
                    kwargs[default] = replacements[default]()
        return func(*args, **kwargs)
    return wrapper
