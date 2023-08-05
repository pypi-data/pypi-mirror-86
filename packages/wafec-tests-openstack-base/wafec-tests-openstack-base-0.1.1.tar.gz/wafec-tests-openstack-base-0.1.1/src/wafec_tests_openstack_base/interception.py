import base64

from .fault import *
from .exceptions import MethodNotFoundException

__all__ = [
    'generate_key',
    'apply_fault',
    'operators',
    'names_map'
]

operators = [
    TextOperator()
]

names_map = {}

for operator in operators:
    for name in operator.names:
        names_map[name] = operator


def generate_key(*args):
    if args and len(args) and args != (None,):
        result = '-'.join([str(arg) for arg in args if arg is not None])
        return base64.b64encode(str.encode(result)).decode('ascii')
    else:
        return None


def apply_fault(method, value):
    if method in names_map:
        operator = names_map[method]
        return operator.apply_fault(method, value)
    else:
        raise MethodNotFoundException()
