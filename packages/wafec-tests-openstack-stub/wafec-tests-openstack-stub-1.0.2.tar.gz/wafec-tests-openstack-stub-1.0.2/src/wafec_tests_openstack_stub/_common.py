from wrapt import ObjectProxy
import threading
import requests

from .utility import Utility
from ._base import white_list, simple_types

__all__ = [
    'is_proxy_allowed',
    'safe_requests_post_run_async'
]


def is_proxy_allowed(x):
    if not isinstance(x, ObjectProxy):
        if isinstance(x, dict) or isinstance(x, list) or callable(x) or\
           type(x).__name__ == 'dict_items' or isinstance(x, tuple):
            return True
        if x is not None and type(x) not in simple_types:
            if Utility.starts_with(white_list, Utility.fullname(x)):
                return True
    return False


def safe_run(target, args, kwargs):
    try:
        target(*args, **kwargs)
    except:
        pass


def safe_requests_post_run_async(*args, **kwargs):
    thread = threading.Thread(target=safe_run, args=(requests.post, args, kwargs))
    thread.start()
