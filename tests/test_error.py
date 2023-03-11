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


def test_can_define_property_as_error() -> None:
    # given
    class MyError(Error):
        child_error = "child_error"

    # then
    with pytest.raises(MyError.child_error):
        raise MyError.child_error


def test_can_extend_property_error() -> None:
    # given
    class MyError(Error):
        child_error = "child_error"

    class MyChildError(MyError.child_error):
        sub_child_error = "sub_child_error"

    # then
    with pytest.raises(MyError.child_error):
        raise MyChildError

    with pytest.raises(MyError):
        raise MyChildError

    with pytest.raises(MyError):
        raise MyChildError.sub_child_error

    with pytest.raises(MyError.child_error):
        raise MyChildError.sub_child_error


def test_can_use_shared_error() -> None:
    # given
    class TestError(Exception):
        pass

    class MyError(Error):
        child_error = "child_error"
        test_error: TestError = "test_error"

    class OtherError(Error):
        test_error: TestError = "test_error"

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
    except OtherError:
        pass


def test_can_raise_error_with_kwargs() -> None:
    # given
    class MyError(Error):
        test_error = "test_error"

    # when
    try:
        raise MyError.test_error(param_a="a", param_b="b")
    except MyError.test_error as e:

        assert e.kwargs.get("param_a") == "a"
        assert e.kwargs.get("param_b") == "b"


def test_can_raise_error_with_args() -> None:
    # given
    class MyError(Error):
        test_error = "test_error"

    # when
    try:
        raise MyError.test_error("a", "b")
    except MyError.test_error as e:

        assert e.args[0] == "a"
        assert e.args[1] == "b"
