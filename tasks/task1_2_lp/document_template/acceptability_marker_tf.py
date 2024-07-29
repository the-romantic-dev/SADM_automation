from report.model.document_template import DocumentTemplate
from report.model.formula import Formula
from report.model.template_filler import TemplateFiller


class AcceptabilityMarkerTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, unacceptable_variables: list[int]):
        self.unacceptable_variables = unacceptable_variables
        super().__init__(template)

    @TemplateFiller.filler_method
    def _fill_unacceptable_variable(self):
        elements_latexes = [f"x_{i + 1} \lt 0" for i in self.unacceptable_variables]
        formula_latex = ",".join(elements_latexes)
        formula = Formula([formula_latex])
        self.template.insert_formula(key="unacceptable_variables", formula=formula)
