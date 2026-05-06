import functools  # This is only needed for debugging, you can remove

def injectinator(func):
    @functools.wraps(func)  # This is only needed for debugging, you can remove
    def wrapper(*args, **kwargs):
        """
        Very simple dependency injection wrapper that supplies concrete instances of specified class definitions from a functions specification
        """
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
