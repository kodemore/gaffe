from gaffe import Error, raises


class MyError(Error):
    test_error: Exception


class AnotherError(MyError):
    pass


a = AnotherError.test_error(123)
b = MyError.test_error(123)

try:
    raise MyError.test_error("a", "b")
except MyError.test_error as e:
    print(e)


class Temp:
    @raises(MyError.test_error)
    def do_a(self) -> None:
        ...


@raises(MyError.test_error)
def bla() -> None:
    raise MyError.test_error("a", "b")
