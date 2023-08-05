from .client_base import ClientBase

__all__ = [
    'InterceptionAgentClient'
]


class InterceptionAgentClient(ClientBase):
    def __init__(self, host):
        ClientBase.__init__(self, {
            'prefix': f'{host}/api/interception'
        })

    def post(self, ps, name, x, trace, asynchronous=False, callback=None):
        self._request({
            'json': {
                'ps': ps,
                'name': name,
                'x': x,
                'trace': trace
            },
            'method': 'post'
        }, asynchronous=asynchronous, callback=callback)

    def put(self, key, method):
        self._request({
            'json': {
                'key': key,
                'method': method
            },
            'method': 'put'
        })
