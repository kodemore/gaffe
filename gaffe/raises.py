from functools import wraps
from typing import TypeVar, Callable, Type, Any

T = TypeVar("T")


def raises(*allowed_errors: Type[Exception]) -> Callable[[T], T]:

    def _decorate(what: T) -> T:

        @wraps(what)
        def _execute_what(*args, **kwargs) -> Any:
            try:
                return what(*args, **kwargs)
            except Exception as error:
                if not isinstance(error, allowed_errors):
                    raise AssertionError(
                        f"{what} raised {error.__class__} exception which "
                        f"is not within allowed list {allowed_errors}"
                    )
                raise error

        return _execute_what

    return _decorate
