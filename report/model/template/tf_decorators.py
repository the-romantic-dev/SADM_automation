from functools import wraps
from typing import Type

from report.model.template.template_filler import TemplateFiller

__root_template = None


def root_tf(cls: Type[TemplateFiller]):
    # @wraps(cls)
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.template.root_template = self.template
            global __root_template
            __root_template = self.template

    return Wrapped


def sub_tf(cls: Type[TemplateFiller]):
    # @wraps(cls)
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            global __root_template
            self.template.root_template = __root_template

    return Wrapped
