from __future__ import annotations

from inspect import isclass
from typing import Dict, List, Type, TypedDict, Union, overload


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
            if err_value is Ellipsis:
                err_value = err_name
            errors[err_name] = _ErrorMeta(value=err_value, sub_types=[])

        if "__annotations__" in body:
            for err_name, err_type in body["__annotations__"].items():
                if hasattr(err_type, "__origin__") and err_type.__origin__ == Union:
                    sub_types = list(err_type.__args__)
                elif isclass(err_type) and issubclass(err_type, Exception) or err_type is Ellipsis:
                    sub_types = [err_type]
                else:
                    raise ValueError(
                        f"Invalid subtype `{err_type}` provided " 
                        f"for `{err_name}` in `{what}` class."
                    )
                if Exception in sub_types:
                    sub_types.remove(Exception)
                if Ellipsis in sub_types:
                    sub_types.remove(Ellipsis)
                if Error in sub_types:
                    sub_types.remove(Error)

                if err_name not in errors:
                    errors[err_name] = _ErrorMeta(
                        value=err_name,
                        sub_types=sub_types
                    )
                else:
                    errors[err_name]["sub_types"] = sub_types

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
                "full_name": qual_name,
                "name": a_name,
                "value": a_value["value"],
            }
            extra_bases = [getattr(base, a_name) for base in bases if hasattr(base, a_name)]
            all_bases = [cls] + extra_bases + a_value["sub_types"]
            child_error_class = type.__new__(cls.__class__, qual_name, tuple(all_bases), child_dct)
            setattr(cls, a_name, child_error_class)


class Error(Exception, metaclass=ErrorMeta):
    value: str
    name: str
    full_name: str

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

    def __str__(self) -> str:
        return self.value

