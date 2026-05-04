![build workflow](https://github.com/Centurix/injectinator/actions/workflows/test.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![uv-managed](https://img.shields.io/badge/uv-managed-blueviolet)

INJECTINATOR
=

Very Simple Dependency Injection.

Here's the function, just paste it where you need it:

```
def injectinator(func):
    def wrapper(*args, **kwargs):
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
```

Need some kind of dependency injection but don't want a massive library adding to your
dependency graph that introduces potential supply chain attacks? Well, this is what you need.

This also doesn't need any imports to work. Just paste the script above here's an example of how to use it:

```
class BaseClass:
    # You don't really need this base class, but for the sake of method contracts it's here 
    def print(self):
        ...

class InjectedClass(BaseClass):
    # This will be the default injected class if nothing is provided in a call
    def print(self):
        print("Default class")


class SuppliedClass(BaseClass):
    # This will be a supplied class
    def print(self):
        print("Supplied class")


@injectinator
def test(injected=InjectedClass):
    # Can have as many parameters as you like, note that the class is a reference to the class, not an instance
    injected.print()

# Two calls, first creates an instance of InjectedClass and passes it to the function, second supplies an instance of SuppliedClass
test()
test(SuppliedClass())
```

Wait I hear you say: Can't we just create an instance of the class in the function specification like this?

```
def test(injected=InjectedClass()):
    ...
```

You can, but the instantiation is performed when Python creates the definition of the function, not at the time you run
the function. Which means that the object it creates is re-used every time you call the function, which is not desirable.

Also, if you need to debug this, you might need to change it to:

```
import functools

def injectinator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ...
```

This will retain the call stack and debugging easier. But as the script is below, you can add it without imports.

Notes on this script
-

- It relies on dunder methods on `func` itself, so these _could_ change in the future. They've all been clumped up together for this reason to make it obvious when it fails because the Python foundation changed their usage of dunders
- There is no parameter support on the injected class, it could be adjusted to support them
- All the config for the injection is in the function specification rather than the decorator
- There's no types. It should have types I guess. Probably added to the two function specifications. Could be lazy and just make it all `Any` but then you'd have to drag in `typing` as an import for this gist
- I have not timed this. It could be wildly inefficient. There's an iteration enumerating over the function parameter list so its O(n)
- This script does work with arbitrary length argument specifications like adding `*args` to the end
- Although it is DI in 11 lines, I've no interest in code golf.

Operation
-

1. Figure out what the default values are for each argument, dump the results in `replacements`
1. Skip supplied positional values
1. For arguments with a default value that do not have a keyword supplied value and the default is a class type, create an instance and add to the keyword argument dictionary
1. Invoke the wrapped function/method with positional and keyword values
