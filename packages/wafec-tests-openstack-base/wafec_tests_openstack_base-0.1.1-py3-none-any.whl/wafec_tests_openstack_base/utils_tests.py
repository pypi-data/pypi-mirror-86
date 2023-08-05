import unittest

from .utils import dict_get_or_else, get_first_not_none


class UtilsTests(unittest.TestCase):
    def test_dict_get_or_else_when_exists(self):
        d = {'x': 'test'}
        result = dict_get_or_else(d, 'x')
        self.assertEqual('test', result)

    def test_dict_get_or_else_when_not_exists(self):
        d = {'x': 'test'}
        result = dict_get_or_else(d, 'y')
        self.assertIsNone(result)

    def test_dict_get_or_else_when_dict_is_none(self):
        d = None
        result = dict_get_or_else(d, 'x')
        self.assertIsNone(result)

    def test_get_first_not_none_when_exists(self):
        args = [None, 10, 3]
        result = get_first_not_none(*args)
        self.assertEqual(10, result)

    def test_get_first_not_none_when_args_is_empty(self):
        result = get_first_not_none()
        self.assertIsNone(result)
