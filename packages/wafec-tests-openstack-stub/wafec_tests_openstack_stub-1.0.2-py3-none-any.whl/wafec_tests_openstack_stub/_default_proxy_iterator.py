from .utility import Utility

__all__ = [
    'DefaultProxyIterator'
]


class DefaultProxyIterator(object):
    def __init__(self, self_trace, wrapped, default_proxy_factory):
        self.self_trace = self_trace
        self.wrapped = wrapped
        self.iterator = iter(wrapped)
        self.n = 0
        self.default_proxy_factory = default_proxy_factory

    def __iter__(self):
        return self

    def __next__(self):
        result = next(self.iterator)
        self.n += 1
        trace = Utility.create_name(self.self_trace, f'[{self.n - 1}]')
        return self.default_proxy_factory.of(result, trace=trace)
