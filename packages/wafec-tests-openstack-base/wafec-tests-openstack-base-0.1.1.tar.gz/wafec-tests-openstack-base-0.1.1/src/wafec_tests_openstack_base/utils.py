import os

from .exceptions import ArgumentException

__all__ = [
    'dict_get_or_else',
    'get_first_not_none',
    'get_or_env',
    'first_existent_path',
    'get_or_else'
]


def dict_get_or_else(d, key, else_value=None):
    if d is None:
        return else_value
    if key in d:
        return d[key]
    else:
        return else_value


def get_first_not_none(*args):
    for arg in args:
        if arg is not None:
            return arg
    return None


def get_or_env(value, name):
    if value is not None:
        return value
    return os.environ.get(name)


def first_existent_path(sources):
    if not sources:
        raise ArgumentException()
    for source in sources:
        if os.path.exists(source):
            return source
    return None


def get_or_else(value, other=None):
    if value is not None:
        return value
    return other

