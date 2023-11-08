from functools import wraps
from typing import Any, Callable, Type, TypeVar, Union

T = TypeVar("T")


def raises(*allowed_errors: Union[Type[Exception], Exception]) -> Callable:
    def _decorate(what: Callable) -> Callable:
        @wraps(what)
        def _execute_what(*args, **kwargs) -> Any:
            try:
                return what(*args, **kwargs)
            except Exception as error:
                if not isinstance(error, allowed_errors):  # type: ignore
                    raise AssertionError(
                        f"{what} raised {error.__class__} exception which "
                        f"is not within allowed list {allowed_errors}"
                    )
                raise error

        return _execute_what

    return _decorate
