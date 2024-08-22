from __future__ import annotations

from pathlib import Path
from report.model.template.document_template import DocumentTemplate


class TemplateFiller:
    def __init__(self, template: DocumentTemplate):
        self.template: DocumentTemplate = template

    def get_fillers(self):
        all_methods = [getattr(self, method_name) for method_name in dir(self) if callable(getattr(self, method_name))]
        result = [method for method in all_methods if hasattr(method, '_is_filler') and method._is_filler]
        return result

    def get_template_fillers(self):
        all_methods = [getattr(self, method_name) for method_name in dir(self) if callable(getattr(self, method_name))]
        result = [method for method in all_methods if
                  hasattr(method, 'is_template_filler') and method.is_template_filler]
        return result

    def fill(self):
        fillers = self.get_fillers()
        tf_funcs = self.get_template_fillers()
        for f in tf_funcs:
            tf: TemplateFiller = f()
            fillers.extend(tf.get_fillers())
            tf.template = self.template
        for f in fillers:
            f()
        # methods = [getattr(self, method_name) for method_name in dir(self)
        #            if callable(getattr(self, method_name))]

    @classmethod
    def filler_method(cls, func):
        func._is_filler = True
        return func

    def save(self, save_path: Path, document_name: str = "output.docx", add_pdf: bool = True):
        self.template.save(save_path, document_name, add_pdf)
