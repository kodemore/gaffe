import pytest

from gaffe import Error


def test_can_define_error_class() -> None:
    # given
    class MyError(Error):
        pass

    # then
    assert issubclass(MyError, Exception)


def test_raise_exception_as_class() -> None:
    # given
    class MyError(Error):
        pass

    # then
    with pytest.raises(MyError):
        raise MyError

    with pytest.raises(Error):
        raise MyError

    with pytest.raises(Exception):
        raise MyError


def test_get_name_value_and_full_name() -> None:
    # given
    class MyError(Error):
        error_one: ...
        error_two: ...
        custom_error = "custom_value"

    class MyChildError(MyError):
        error_three: ...
        custom_error = "child_custom_value"

    # when
    try:
        raise MyError.error_one
    # then
    except MyError as e:
        assert e.name == "error_one"
        assert e.value == "error_one"
        assert e.full_name == "MyError@error_one"

    # when
    try:
        raise MyError.custom_error
    # then
    except MyError as e:
        assert e.name == "custom_error"
        assert e.value == "custom_value"
        assert e.full_name == "MyError@custom_error"

    # when
    try:
        raise MyChildError.error_one
    # then
    except MyError as e:
        assert e.name == "error_one"
        assert e.value == "error_one"
        assert e.full_name == "MyChildError@error_one"

    # when
    try:
        raise MyChildError.custom_error
    # then
    except MyError as e:
        assert e.name == "custom_error"
        assert e.value == "child_custom_value"
        assert e.full_name == "MyChildError@custom_error"


def test_can_define_property_as_error() -> None:
    # given
    class MyError(Error):
        child_error = ...

    # then
    with pytest.raises(MyError.child_error):
        raise MyError.child_error

    assert str(MyError.child_error()) == "child_error"


def test_can_define_property_as_error_with_exception_type_hint() -> None:
    # given
    class MyError(Error):
        child_error: Error

    # then
    with pytest.raises(MyError.child_error):
        raise MyError.child_error

    assert str(MyError.child_error()) == "child_error"


def test_can_use_shared_error() -> None:
    # given
    class TestError(Exception):
        pass

    class MyError(Error):
        child_error: ...
        test_error: TestError

    class OtherError(Error):
        test_error: TestError

    # then
    with pytest.raises(TestError):
        raise MyError.test_error

    with pytest.raises(TestError):
        raise OtherError.test_error

    with pytest.raises(MyError):
        raise MyError.test_error

    with pytest.raises(OtherError):
        raise OtherError.test_error

    try:
        OtherError.test_error
    except MyError:
        pytest.fail()
    except OtherError as e:
        assert str(e) == "test_error"
        pass


def test_can_raise_error_with_kwargs() -> None:
    # given
    class MyError(Error):
        test_error = ...

    # when
    try:
        raise MyError.test_error(param_a="a", param_b="b")
    except MyError.test_error as e:
        assert str(e) == "test_error"
        assert e.kwargs.get("param_a") == "a"
        assert e.kwargs.get("param_b") == "b"


def test_can_raise_error_with_args() -> None:
    # given
    class MyError(Error):
        test_error = ...

    # when
    try:
        raise MyError.test_error("a", "b")
    except MyError.test_error as e:
        assert str(e.full_name) == "MyError@test_error"
        assert str(e) == "test_error"
        assert e.args[0] == "a"
        assert e.args[1] == "b"
