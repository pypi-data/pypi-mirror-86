import abc

from ..exceptions import FaultNotFoundException


class BaseOperator(object, metaclass=abc.ABCMeta):
    def __init__(self):
        self.map = {}

    @property
    def names(self):
        return list(self.map.keys())

    def apply_fault(self, name, value):
        if name in self.names:
            return self.map[name](value=value)
        else:
            raise FaultNotFoundException()
        
    @abc.abstractmethod
    def should_apply(self, x, value):
        pass
