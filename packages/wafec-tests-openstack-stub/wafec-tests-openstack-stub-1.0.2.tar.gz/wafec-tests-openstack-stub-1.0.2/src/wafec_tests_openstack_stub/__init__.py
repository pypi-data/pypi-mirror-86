from pkg_resources import declare_namespace
from .default_proxy import DefaultProxy

declare_namespace(__name__)

__all__ = [
    'DefaultProxy',
    'create_proxy'
]

create_proxy = DefaultProxy.of
