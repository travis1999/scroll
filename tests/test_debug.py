from scroll.debug import debug, debugmethords
import pytest


@debug
def add_no_arg(a: int, b: int) -> int:
    return a + b


@debug(prefix='[DEBUG]')
def add_with_arg(a: int, b: int) -> int:
    return a + b


@debugmethords
class Foo:
    def baz(self):
        pass

    def bar(self):
        pass


def test_wrap_no_arg(capfd):
    print(add_no_arg(1, 2))

    captured = capfd.readouterr()

    assert captured.out == "Called add_no_arg\n3\n"


def test_wrap_with_arg(capfd):
    print(add_with_arg(1, 2))

    captured = capfd.readouterr()

    assert captured.out == "[DEBUG]Called add_with_arg\n3\n"


def test_raises_ValueError():
    with pytest.raises(ValueError):
        @debug('[DEBUG]')
        def add_with_arg(a: int, b: int) -> int:
            return a + b


def test_wrap_dgbmeth(capfd):
    foo = Foo()

    foo.baz()

    captured = capfd.readouterr()
    assert captured.out == "Called Foo.baz\n"
