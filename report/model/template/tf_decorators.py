from functools import wraps
from typing import Type

from report.model.template.template_filler import TemplateFiller

__root_template = None


def root_tf(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def wrapped_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.template.root_template = self.template
        global __root_template
        __root_template = self.template

    cls.__init__ = wrapped_init
    return cls


# def root_tf(cls: Type[TemplateFiller]):
#     # @wraps(cls, updated=())
#     class Wrapped(cls):
#         def __init__(self, *args, **kwargs):
#
#             super().__init__(*args, **kwargs)
#             self.template.root_template = self.template
#             global __root_template
#             __root_template = self.template
#     # Сохраняем метаданные оригинального класса
#     Wrapped.__name__ = cls.__name__
#     Wrapped.__module__ = cls.__module__
#     Wrapped.__doc__ = cls.__doc__
#     return Wrapped


def sub_tf(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def wrapped_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        global __root_template
        self.template.root_template = __root_template

    cls.__init__ = wrapped_init
    return cls

# def sub_tf(cls: Type[TemplateFiller]):
#     # @wraps(cls)
#     class Wrapped(cls):
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             global __root_template
#             self.template.root_template = __root_template
#
#     return Wrapped
