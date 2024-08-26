from pathlib import Path

from docx import Document
from sympy import Matrix

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import template_filler, document
from report.model.template.template_filler import TemplateFiller
from tasks.task1_3_nlp_unlimited.model.methods import IterativeMethod
from tasks.task1_3_nlp_unlimited.view.methods.univariate_first_step_size.univariate_first_step_size_tf import \
    UnivariateFirstStepSizeTF

template_path = Path(Path(__file__).parent, "method.docx")


class MethodTF(TemplateFiller):
    def __init__(self, method: IterativeMethod, start_point: Matrix, description_document_path: Path,
                 is_step_univariate: bool

                 ):
        self.description_document_path = description_document_path
        self.is_step_univariate = is_step_univariate
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.start_point = start_point
        self.method = method

    @document
    def _fill_method_steps_description(self):
        return Document(self.description_document_path.as_posix())

    @template_filler
    def _fill_univariate_first_step_size(self):
        if not self.is_step_univariate:
            return None
        return UnivariateFirstStepSizeTF(self.method, self.start_point)
