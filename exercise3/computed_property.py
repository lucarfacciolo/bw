import functools
from typing import Any, Callable, Tuple


class computed_property:
    def __init__(self, *variables: str) -> None:
        # NOTE(lfacciolo) Stores the list of attributes this property depends on. This is triggered when python reads the decorator above the method
        self.variables = variables

    def __call__(self, func: Callable):
        # NOTE(lfacciolo) this is called right after init, and sets property
        self.func = func
        self.__doc__ = (
            func.__doc__
        )  # NOTE(lfacciolo) this make the docstring from wrapped func works

        # NOTE(lfacciolo) set attribute names internally
        self._attr_name = func.__name__
        self._name = f"__name_{self._attr_name}__"
        self._state = f"__state_{self._attr_name}__"

        functools.update_wrapper(self, func)  # NOTE(lfacciolo) makes our help works

        return self

    def __get__(self, instance: Any, owner: Any) -> Any:
        # NOTE(lfacciolo) this is the main  method. this method fires when I try to access my object attribute
        if instance is None:
            return self

        # NOTE(lfacciolo) get current variables
        current = tuple(getattr(instance, d, object()) for d in self.variables)

        # NOTE(lfacciolo) get cached variables, None is default
        cached = getattr(instance, self._state, None)

        # NOTE(lfacciolo) if something changed, call function and compute new values
        if cached != current:
            value = self.func(instance)
            setattr(instance, self._name, value)
            setattr(instance, self._state, current)

        return getattr(instance, self._name)

    def setter(self, func: Callable) -> "computed_property":
        self.func_set = func
        return self

    def __set__(self, instance: Any, value: Any) -> None:
        if hasattr(self, "func_set"):
            self.func_set(instance, value)
            if hasattr(instance, self._name):
                delattr(instance, self._name)
            if hasattr(instance, self._state):
                delattr(instance, self._state)
        else:
            raise AttributeError("setter not set")

    def deleter(self, func: Callable) -> "computed_property":
        self.func_del = func
        return self

    def __delete__(self, instance: Any) -> None:
        if hasattr(self, "func_del"):
            self.func_del(instance)

            if hasattr(instance, self._name):
                delattr(instance, self._name)
            if hasattr(instance, self._state):
                delattr(instance, self._state)
        else:
            raise AttributeError("deleter not set")
