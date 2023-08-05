import abc
import requests
from threading import Thread

from ..utils import dict_get_or_else, get_first_not_none
from ..exceptions import ClientException


class ClientBase(object, metaclass=abc.ABCMeta):
    def __init__(self, opt):
        self.prefix = dict_get_or_else(opt, 'prefix')

    def _request(self, opt, asynchronous=False, callback=None):
        if asynchronous:
            return self._request_async(opt, callback)
        else:
            return self._request_internal(opt)

    def _request_internal(self, opt):
        prefix = get_first_not_none(dict_get_or_else(opt, 'prefix'), self.prefix)
        path = get_first_not_none(dict_get_or_else(opt, 'path'), '')
        url = f'{prefix}{path}'
        method = get_first_not_none(dict_get_or_else(opt, 'method'), 'get')
        fx = getattr(requests, method.lower())
        kwargs = {'url': url, 'headers': dict_get_or_else(opt, 'headers'), 'json': dict_get_or_else(opt, 'json')}
        result = fx(**kwargs)
        if 200 <= result.status_code < 300:
            return result.json()
        else:
            raise ClientException()

    def _request_async(self, opt, callback=None):
        def request(**kwargs):
            result = kwargs['self']._request(opt=kwargs['opt'])
            if kwargs['callback']:
                kwargs['callback'](result)
        thread = Thread(target=request, kwargs={'self': self, 'opt': opt, 'callback': callback})
        thread.start()
