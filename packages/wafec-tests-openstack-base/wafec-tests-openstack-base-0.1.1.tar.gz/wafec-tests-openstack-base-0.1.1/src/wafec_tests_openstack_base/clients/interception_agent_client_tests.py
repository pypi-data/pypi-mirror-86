import unittest

from .interception_agent_client import InterceptionAgentClient

_HOST = 'http://localhost:7654'


class InterceptionAgentClientTests(unittest.TestCase):
    def setUp(self):
        self.client = InterceptionAgentClient(_HOST)

    def test_interception_post(self):
        self.client.post('test', 'test', 'test', 'test')
        self.assertTrue(True)

    def test_interception_put(self):
        self.client.put('test', 'test')
        self.assertTrue(True)
