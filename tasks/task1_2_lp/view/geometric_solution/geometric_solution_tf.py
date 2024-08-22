from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula, image
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.view.plot import PlotColors
from tasks.task1_2_lp.view.plot.plotter import save_lpp_plot
from tasks.task1_2_lp.view.solution_tf import SolutionTF

template_path = Path(Path(__file__).parent, "geometric_solution.docx")
pic_path = Path(Path(__file__).parent, "sol_pic.png")


@sub_tf
class GeometricSolutionTF(SolutionTF):
    def __init__(self, solutions: list[BasisSolution], opt_sol: BasisSolution):
        self.opt_sol = opt_sol
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.solutions = solutions

    @image
    def _fill_solution_img(self):
        lpp = self.solutions[0].lp_problem
        colors = PlotColors(constraints_color='#2D70B3', objective_color='#FA6501', solutions_color='#BAFFC9')
        save_lpp_plot(lpp, self.solutions, colors, pic_path)
        return pic_path

    @formula
    def _fill_result(self):
        return self.result_formula(self.opt_sol)
