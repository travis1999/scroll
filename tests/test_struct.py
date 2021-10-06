from scroll.base import BaseModel
from scroll.descriptor import Integer, DefaultString


class Point(BaseModel):
    x = Integer()
    y = Integer()


class Point3D(Point):
    z = Integer()


class Place(BaseModel):
    name = DefaultString(default="here")


def test_create():
    point = Point(1, 2)

    assert point.x == 1
    assert point.y == 2


def test_inherit():
    point = Point3D(1, 2, 4)

    assert point.x == 1
    assert point.y == 2
    assert point.z == 4


def test_no_arg_default():
    place = Place()

    assert place.name == 'here'


def test_arg_default():
    place = Place('there')

    assert place.name == 'there'


def test_kwarg_default():
    place = Place(name='there')

    assert place.name == 'there'
