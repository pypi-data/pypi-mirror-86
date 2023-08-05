import abc
import copy
from wrapt import ObjectProxy
import json

from .utility import Utility
from ._default_proxy_iterator import DefaultProxyIterator
from ._common import is_proxy_allowed
from .interception import Interception
from ._auto import Auto

__all__ = [
    'DefaultProxy'
]


class DefaultProxy(ObjectProxy, abc.ABC):
    _default_add_proxy_interception_info = Interception.add_proxy_interception_info
    _json_default_encoder_default = json._default_encoder.default

    def __init__(self, wrapped, trace=None):
        ObjectProxy.__init__(self, wrapped)
        self._self_trace = trace

    def __copy__(self):
        result = copy.copy(self.__wrapped__)
        return DefaultProxy.of(result)

    def __deepcopy__(self, memodict={}):
        result = copy.deepcopy(self.__wrapped__, memodict)
        return DefaultProxy.of(result)

    def __getitem__(self, item):
        trace = Utility.create_name(self._self_trace, f'[{item}]')
        DefaultProxy._default_add_proxy_interception_info(item, x=self.__wrapped__, trace=trace)
        result = self.__wrapped__[item]
        return DefaultProxy.of(result, trace=trace)

    def __getattr__(self, item):
        trace = Utility.create_name(self._self_trace, f'.{item}')
        DefaultProxy._default_add_proxy_interception_info(item, x=self.__wrapped__, trace=trace)
        result = getattr(self.__wrapped__, item)
        return DefaultProxy.of(result, trace=trace)

    def __call__(self, *args, **kwargs):
        result = self.__wrapped__(*args, **kwargs)
        return DefaultProxy.of(result, trace=self._self_trace)

    def __iter__(self):
        return DefaultProxyIterator(self._self_trace, self.__wrapped__, DefaultProxy)

    def __reduce__(self):
        result = self.__wrapped__.__reduce__()
        return result

    def __reduce_ex__(self, protocol):
        result = self.__wrapped__.__reduce_ex__(protocol)
        return result

    @staticmethod
    def of(x, trace=None):
        if is_proxy_allowed(x):
            if isinstance(trace, Auto):
                trace = Utility.create_name(x)
            DefaultProxy.try_ensure_correct_json_encoder()
            return DefaultProxy(x, trace=trace)
        return x

    @staticmethod
    def try_ensure_correct_json_encoder():
        def default(cls, o):
            if isinstance(o, DefaultProxy) or isinstance(o, ObjectProxy):
                return o.__wrapped__
            raise TypeError('')

        json._default_encoder.default = default.__get__(json._default_encoder, DefaultProxy._json_default_encoder_default)
