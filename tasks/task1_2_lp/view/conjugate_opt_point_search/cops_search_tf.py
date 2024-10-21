from pathlib import Path

from sympy import latex, Matrix

from report.docx.omml import latex2omml
from report.model.elements.math.matrix import matrix_from_sympy, matrix_from_elements
from report.model.elements.math.braces import braces, BraceType
from report.model.docx_parts.formula import Formula
from report.model.elements.math.sup import sup
from report.model.report_prettifier import expr_latex, rational_latex
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula, image
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.model import BasisSolution, Objective
from tasks.task1_2_lp.model.solvers import BruteforceSolver
from tasks.task1_2_lp.view.plot import PlotColors
from tasks.task1_2_lp.view.plot.plotter import save_lpp_plot

template_path = Path(Path(__file__).parent, "conjugate_opt_point_search.docx")

pic_path = Path(Path(__file__).parent, "dual_sol_pic.png")


class COPSSearchTF(TemplateFiller):
    def __init__(self, opt_sol: BasisSolution):
        self.opt_sol = opt_sol
        template = DocumentTemplate(template_path)
        basis = self.opt_sol.basis

        A = self.opt_sol.lp_problem.canonical_form.matrices[0]
        C = self.opt_sol.lp_problem.canonical_form.matrices[2]

        self.A_b: Matrix = Matrix.hstack(A.col(basis[0]), A.col(basis[1]))
        self.C_b: Matrix = Matrix([C[basis[0], 0], C[basis[1], 0]])
        self.yopt = self.A_b.T.inv() * self.C_b
        self.dual_lpp = self.opt_sol.lp_problem.canonical_form.get_dual_problem(variable_symbol="y")
        super().__init__(template)

    @formula
    def _fill_X_opt(self):
        X_latex = "X_{opt}^{Б}"
        variables = self.opt_sol.basis_variables
        variables_element = latex2omml(",".join([latex(v) for v in variables]))
        formula_data = [
            f"{X_latex} = ",
            braces(variables_element)
        ]
        return Formula(formula_data)

    @formula
    def _fill_A_b(self):
        formula_data = [
            f"A_Б = ",
            matrix_from_sympy(self.A_b)
        ]
        return Formula(formula_data)

    @formula
    def _fill_C_b(self):
        formula_data = [
            f"C_Б = ",
            matrix_from_sympy(self.C_b)
        ]
        return Formula(formula_data)

    @formula
    def _fill_Yopt(self):
        basis_variables = self.opt_sol.basis_variables
        step_1_data = [
            sup(matrix_from_sympy(self.A_b.T), sup_element=latex2omml("-1")),
            "\\cdot",
            matrix_from_sympy(self.C_b)
        ]
        step_2_data = [
            matrix_from_sympy(self.A_b.T.inv()),
            "\\cdot",
            matrix_from_sympy(self.C_b)
        ]
        step_3_data = [
            matrix_from_sympy(self.yopt),
        ]
        formula_data = [
            "Y_{opt} = ",
            *step_1_data,
            '=',
            *step_2_data,
            '=',
            *step_3_data

        ]
        return Formula(formula_data)

    @formula
    def _fill_objective_value(self):
        objective_coeffs = self.dual_lpp.objective.coeffs
        objective_variables = self.dual_lpp.objective.variables

        C = self.dual_lpp.matrices[2]
        formula_data = [
            'F = ',
            expr_latex(objective_coeffs, objective_variables),
            ' = ',
            rational_latex((C.T * self.yopt)[0])
        ]
        return Formula(formula_data)

    @formula
    def _fill_result(self):
        formula_data = [
            f"y_1 = {rational_latex(self.yopt[0, 0])}, y_2 = {rational_latex(self.yopt[1, 0])}"
        ]
        return Formula(formula_data)

    @image
    def _fill_cops_plot(self):
        lpp = self.opt_sol.lp_problem.canonical_form.get_dual_problem(variable_symbol="y")
        solutions = BruteforceSolver(lp_problem=lpp).solve()[0]
        colors = PlotColors(constraints_color='#2D70B3', objective_color='#FA6501', solutions_color='#BAFFC9')
        save_lpp_plot(lpp, solutions, colors, pic_path)
        return pic_path
