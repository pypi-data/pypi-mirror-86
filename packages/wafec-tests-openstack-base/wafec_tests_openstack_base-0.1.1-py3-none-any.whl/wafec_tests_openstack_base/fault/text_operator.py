import random, string

from .base_operator import BaseOperator


class TextOperator(BaseOperator):
    VARCHAR_MAX_LEN = 23000

    def __init__(self):
        BaseOperator.__init__(self)
        self.map['text_none'] = lambda _: None
        self.map['text_random'] = self.text_random
        self.map['text_varchar_overflow'] = self.text_varchar_overflow

    @staticmethod
    def text_random(**kwargs):
        size = 10
        if 'value' in kwargs:
            size = len(kwargs['value'])
        return ''.join(random.sample(string.ascii_letters + string.digits, size))

    @staticmethod
    def text_varchar_overflow(**kwargs):
        return ''.join(random.sample(string.ascii_letters + string.digits, TextOperator.VARCHAR_MAX_LEN))

    @staticmethod
    def text_empty(**kwargs):
        return ''

    def should_apply(self, x, value):
        return x == 'string'
