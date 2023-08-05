import base64
import unittest

from .interception import generate_key


class InterceptionTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_key(self):
        result = generate_key('test1', 'test2')
        self.assertEqual(base64.b64encode(b'test1-test2').decode('ascii'), result)

    def test_generate_key_when_one_arg_none(self):
        result = generate_key('test1', None)
        self.assertEqual(base64.b64encode(b'test1').decode('ascii'), result)

    def test_generate_key_when_only_none(self):
        result = generate_key(None)
        self.assertIsNone(result)

    def test_generate_key_must_return_string(self):
        result = generate_key('test1', 'test2')
        self.assertIsInstance(result, str)
