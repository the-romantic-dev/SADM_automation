from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula, image
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.view.solution_tf import SolutionTF

template_path = Path(Path(__file__).parent, "geometric_solution.docx")


class GeometricSolutionTF(SolutionTF):
    def __init__(self, opt_solution: BasisSolution):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.opt_solution = opt_solution

    @image
    def _fill_solution_img(self):
        pass


    @formula
    def _fill_result(self):
        return self.result_formula(self.opt_solution)


