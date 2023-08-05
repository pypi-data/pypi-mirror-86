from ._base import simple_types

__all__ = [
    'Utility'
]


class Utility(object):
    @staticmethod
    def fullname(o):
        if o is None:
            return None
        module = o.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return o.__class__.__name__
        else:
            return module + '.' + o.__class__.__name__

    @staticmethod
    def create_name(*args):
        name = ''
        for arg in [arg for arg in args if arg]:
            if type(arg) not in simple_types:
                name += Utility.fullname(arg) + ' '
            else:
                name += str(arg) + ' '
        return name.strip()

    @staticmethod
    def starts_with(collection, text):
        if text is None or collection is None:
            return False
        for item in collection:
            if text.startswith(item):
                return True
        return False
