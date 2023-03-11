from __future__ import annotations

from inspect import isclass
from typing import Any, Dict, List, Type, TypedDict, Union, overload


class _ErrorMeta(TypedDict):
    value: str
    sub_types: List[Type[Exception]]


class ErrorMeta(type):
    def __new__(mcs, what, bases=None, body=None):
        if body["__module__"] == __name__ and body["__qualname__"] == "Error":
            return super().__new__(mcs, what, bases, body)

        errors: Dict[str, _ErrorMeta] = {}

        for err_name, err_value in body.items():
            if err_name.startswith("__"):
                continue
            errors[err_name] = _ErrorMeta(value=err_value, sub_types=[])

        if "__annotations__" in body:
            for err_name, err_type in body["__annotations__"].items():
                if hasattr(err_type, "__origin__") and err_type.__origin__ == Union:
                    errors[err_name]["sub_types"] = list(err_type.__args__)
                elif isclass(err_type) and issubclass(err_type, Exception):
                    errors[err_name]["sub_types"] = [err_type]
                else:
                    raise ValueError(f"Invalid subtype `{err_type}` provided " f"for `{err_name}` in `{what}` class.")

        for base in bases:
            if not issubclass(base, Error):
                continue

            if not hasattr(base, "__errors__"):
                continue

            errors = {**base.__errors__, **errors}

        return type.__new__(mcs, what, bases, {**body, "__errors__": errors})

    def __init__(cls, what, bases, body):
        if body["__module__"] == __name__ and body["__qualname__"] == "Error":
            return

        errors = cls.__errors__

        for a_name, a_value in errors.items():
            qual_name = f"{what}@{a_name}"
            child_dct = {
                "__module__": body["__module__"],
                "__qualname__": qual_name,
                "__value__": a_value["value"],
            }
            extra_bases = [getattr(base, a_name) for base in bases if hasattr(base, a_name)]
            all_bases = [cls] + a_value["sub_types"] + extra_bases
            child_error_class = super().__new__(cls.__class__, qual_name, tuple(all_bases), child_dct)
            setattr(cls, a_name, child_error_class)


class Error(Exception, metaclass=ErrorMeta):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @overload  # type: ignore[override]
    def __eq__(self, object: Error) -> bool:
        pass

    @overload  # type: ignore[override]
    def __eq__(self, object: Type[Error]) -> bool:
        pass

    def __eq__(self, object):
        if isclass(object):
            return object.__name__ == self.__class__.__name__ and object.__module__ == self.__class__.__module__

        return (
            object.__class__.__name__ == self.__class__.__name__
            and object.__class__.__module__ == self.__class__.__module__
        )


def error(value: Any) -> Type[Exception]:
    return value
