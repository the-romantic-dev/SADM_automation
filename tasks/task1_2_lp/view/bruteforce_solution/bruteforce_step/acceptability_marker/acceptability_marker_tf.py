import os
from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from report.model.elements.formula import Formula
from report.model.template.template_filler import TemplateFiller

package_path = Path(os.path.dirname(os.path.abspath(__file__)))
template_path = Path(package_path, "acceptability_marker.docx")


class AcceptabilityMarkerTF(TemplateFiller):
    def __init__(self, unacceptable_variables: list[int]):
        self.unacceptable_variables = unacceptable_variables
        template = DocumentTemplate(template_path)
        super().__init__(template)

    @TemplateFiller.filler_method
    def _fill_unacceptable_variable(self):
        elements_latexes = [f"x_{i + 1} \lt 0" for i in self.unacceptable_variables]
        formula_latex = ",".join(elements_latexes)
        formula = Formula([formula_latex])
        self.template.insert_formula(key="unacceptable_variables", formula=formula)
