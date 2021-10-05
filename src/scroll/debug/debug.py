"""Debug module
debug wrappers that show some debug info on stdout
"""
from functools import wraps, partial


def debug(func=None, *, prefix=''):
    """prints debug info for a function

    Args:
        func (Callable): function to be debuged
        prefix (str): Additional info to be added before printing

    Return:
        wrapper (Callable): wrapped function
    """
    if func is None:
        return partial(debug, prefix=prefix)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if isinstance(func, str):
            raise ValueError(f"To add prefix use @debug(prefix='{func}') not @debug('{func}')")

        print(f'{prefix}Called {func.__qualname__}')
        return func(*args, **kwargs)
    return wrapper


def debugmethords(cls):
    """prints debug info for methords defined in cls

    Args:
        cls (Class): class to add debug info

    Return:
        wrapper (Callable): wrapped class
    """
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val))
    return cls
