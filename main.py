#!/usr/bin/env python3
from abc import ABC, abstractmethod
import functools


class BaseInjectionClass(ABC):
    @abstractmethod
    def print(self):
        print("ABC Print")


class InjectionClassDefault(BaseInjectionClass):
    def print(self):
        print("Injected class Default")


class InjectionClassA(BaseInjectionClass):
    def print(self):
        print("Injected class A")


class InjectionClassB(BaseInjectionClass):
    def print(self):
        print("Injected class B")


def inject(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Does func have arguments?
        # 2. Do any arguments have a default value that is a class?
        # 3. Are there args/kwargs?
        # 4. If not, create an instance of the default class, replace that parameter
        # 5. If there is, forward that instance as the parameter
        argument_count = func.__code__.co_argcount
        arguments = func.__code__.co_varnames[:argument_count]
        argument_types = func.__annotations__
        # Key/value for arguments that have annotations
        for argument_name in argument_types:
            print(argument_name)
            # Is there a default value for this annotated argument?
        argument_defaults = func.__defaults__
        # Argument defaults are mapped as default values to the list of arguments backwards

        # Priorities
        # 1. Pass through already instanced types
        # 2. Create instances of the defaulted class types
        # 3. Create instances of the class type


        print("Create concrete instances of the class types")
        for default in argument_defaults:
            pass
            # if class then:
            #     create an instance
        # Injected classes will be represented by default values so they're always last


        result = func(*args, **kwargs)
        print("After function execution")
        return result
    return wrapper


@inject
def test(first_argument, unclass: InjectionClassDefault, inclass: BaseInjectionClass = InjectionClassDefault, second_argument=False):
    # Objective: Create a decorator that replaces the line below
    inobj = inclass()
    inobj.print()

class TestInjectionClass(BaseInjectionClass):
    def print(self):
        print("Testing stuff here")


def main():
    test(1, InjectionClassA)
    test(2, InjectionClassA, InjectionClassA)
    test(3, InjectionClassA, InjectionClassB)
    test(4, InjectionClassA, TestInjectionClass, second_argument=False)
    print("Hello from playground!")


if __name__ == "__main__":
    main()
