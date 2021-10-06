from scroll.descriptor import Descriptor, Integer, String, Generic, PositiveInteger
from scroll.base import BaseModel

import pytest


class Tclass(BaseModel):
    integer = Integer()
    string = String()
    pinteger = PositiveInteger()


@pytest.fixture
def tclass():
    return Tclass(12, "qwerty", 100)


def test_delete():
    d = Descriptor()

    assert str(d) == "Descriptor"
    del d

    with pytest.raises(UnboundLocalError):
        id(d)  # noqa: F821


def test_correct_type(tclass):
    tclass.integer = 134
    assert tclass.integer == 134


def test_wrong_type(tclass):
    with pytest.raises(TypeError):
        tclass.integer = "123"


def test_generic():
    class Gen(BaseModel):
        test = Generic(set)

    t = Gen({1, 2, 2, 3, 1})

    assert t.test == {1, 2, 3, 1}


def test_generic_convert():
    def convert(t):
        if isinstance(t, list):
            return set(t)
        return t

    class Gen(BaseModel):
        test = Generic(set, convert=convert)

    t = Gen([1, 2, 2, 3, 1])

    assert t.test == {1, 2, 3, 1}


def test_poitive(tclass):
    with pytest.raises(ValueError):
        tclass.pinteger = -100


if __name__ == "__main__":
    test_delete()
