"""Descriptor Module

This module creates descriptors to be used with the BaseModel class

users can create their own descriptors by inheriting from the Descriptor class or
combine existing descriptors

eg
>>> class SizedList(PyList, Sized):
>>>     pass

creates a sized list descriptor with some maxlen

the above descriptor or any decriptor can be used as

>>> Class Person(BaseModel):
>>>     name = String()
>>>     age = Integer()
>>>     hobbies = SizedList(maxlen=5)
>>> me = Person('me me', 23, [1, 2, 3, 4, 5])
"""

from typing import Callable, Any, Optional


class Descriptor:
    """Descriptor base Class for all descriptors

    This descriptors work well with an instance of BaseModel (scroll.base.BaseModel)

    Args:
        name (Optional[str]): name of the descriptor

    Attributes:
        name (Optional[str]): name of the descriptor

    """

    def __init__(self, name: Optional[str] = None):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __str__(self):
        return 'Descriptor'


class Typed(Descriptor):
    """Descriptor that checks if value to be set is of the correct type

    Attributes:
        _type (Any): type of the value to be set
        name (str): name of the descriptor
    """

    _type = object

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise TypeError(f'Expected {self._type} got {type(value)}')
        super().__set__(instance, value)

    def __str__(self):
        return f'Typed descriptor ({self._type})'


class Generic(Typed):
    """Descriptor that checks if value to be set is of the correct type

    convinience class for Typed

    Args:
        _type (Any): type of the value to be set
        convert (Optional[Callable[..., Any]]]): to convert the value to the correct type
    """

    def __init__(self, _type: Any, *args, convert: Optional[Callable[..., Any]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = _type
        self.convert = convert

    def __set__(self, instance, value):
        if self.convert:
            value = self.convert(value)
        super().__set__(instance, value)

    def __str__(self):
        return f'Generic descriptor ({self._type})'


class Positive(Descriptor):
    """Descriptor that checks if value to be set is positive"""

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected positive value')
        super().__set__(instance, value)

    def __str__(self):
        return 'Positive Descriptor'


class Sized(Descriptor):
    """Descriptor that checks the size of the value to be set

    used as a mix in with python objects that have a length

    Args:
        maxlen (int): maximum length of the value to be set

    Attributes:
        maxlen (int): maximum length of the value to be set
    """

    def __init__(self, *args, maxlen, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxlen = maxlen

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError(f"{self.name} argument too long max length is {self.maxlen}")
        super().__set__(instance, value)


class Integer(Typed):
    """Descriptor that checks if the value to be set is an integer"""
    _type = int


class Float(Typed):
    """Descriptor that checks if the value to be set is a float"""
    _type = float


class String(Typed):
    """Descriptor that checks if the value to be set is a String"""
    _type = str


class Default(Descriptor):
    """Default descriptors act like keyword aruments with defaults

    Args:
        default (Any): default type to be set

    Attributes:
        default (Any): fallback value if value set is None
    """

    def __init__(self, *args, default, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = default

    def __set__(self, instance, value):
        if value is None:
            value = self.default() if callable(self.default) else self.default
        super().__set__(instance, value)

    def __str__(self):
        return f'Default value={self.default}'


class DefaultString(Default, String):
    """Convinience class for default strings"""
    pass


class DefaultGeneric(Default, Generic):
    """Convinience class for default generic"""
    pass


class PyList(Typed):
    """Descriptor that checks if the value to be set is a list"""
    _type = list


class PyDict(Typed):
    """Descriptor that checks if the value to be set is a dict"""
    _type = dict


class PositiveInteger(Integer, Positive):
    """Descriptor that checks if the
    value to be set is positive and an integer"""
    pass


class PositiveFloat(Float, Positive):
    """Descriptor that checks if the value
    to be set is a float and positive"""
    pass


class SizedString(String, Sized):
    """Descriptor that checks if the value to be set
    is a string and is of the correct length
    """
    pass
