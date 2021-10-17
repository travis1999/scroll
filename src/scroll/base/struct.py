from ..descriptor import Descriptor
from ..descriptor import Default
from collections import OrderedDict
from inspect import Signature, Parameter
from typing import List


def create_signature(args: List[str], kwargs: List[str]) -> Signature:
    """creates signatue from a list of arguments and keyword arguments

    Args:
        args (List[str]): list of args
        kwargs (List[str]): list of kwargs

    Returns:
        (Signatue): function signature
    """
    pargs = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in args]
    pkwargs = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, default=None) for name in kwargs]
    return Signature(pargs + pkwargs)


class StructMeta(type):
    """metaclass for BaseModel

    The metaclass is used to intergrate Descriptors
    """
    @classmethod
    def __prepare__(cls, name, bases):
        clsdict = OrderedDict()
        for base in bases:
            clsdict.update(base.__dict__)
        return clsdict

    def __new__(cls, clsname, bases, clsdict):
        args = []
        kwargs = []

        fields = {}

        for key, value in clsdict.items():
            if isinstance(value, Descriptor):
                if isinstance(value, Default):
                    kwargs.append(key)
                else:
                    args.append(key)
                fields[key] = value

        for name in args + kwargs:
            clsdict[name].name = name

        clsobj = super().__new__(cls, clsname, bases, dict(clsdict))
        setattr(clsobj, '__fields__', fields)

        sig = create_signature(args, kwargs)
        setattr(clsobj, '__signature__', sig)

        return clsobj


class BaseModel(metaclass=StructMeta):
    """Base Class for all classes that want to use descriptors

    defines an init methord suitable for most needs

    Attributes:
        __signature___ (Signature): signature for the classes init methord
    """
    __signature__: Signature

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            setattr(self, name, value)
