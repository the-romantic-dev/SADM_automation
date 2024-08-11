import os
from pathlib import Path

from report.model.elements.formula import Formula
from report.model.report_prettifier import expression_latex, rational_latex
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.viewmodel.reverse_symplex_viewmodel import ReverseSymplexViewModel

package_path = Path(os.path.dirname(os.path.abspath(__file__)))
template_path = Path(package_path, "reverse_symplex.docx")


class ReverseSymplexTF(TemplateFiller):
    def __init__(self, all_solutions: list[BasisSolution]):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.lp_problem = all_solutions[0].lp_problem
        self.rsvm = ReverseSymplexViewModel(all_solutions)
        self.new_constraint = self.rsvm.new_constraint
        self.canonical_var_count = self.lp_problem.canonical_form.var_count

    @formula
    def _fill_new_constraint(self):
        new_constraint = self.new_constraint
        formula_data = [
            expression_latex(new_constraint.coeffs, new_constraint.variables),
            "\\le",
            rational_latex(new_constraint.const)
        ]
        return Formula(formula_data)

    @formula
    def _fill_new_canonical_constraint(self):
        eq_constraint = self.new_constraint.eq_form(self.canonical_var_count)
        formula_data = [
            expression_latex(eq_constraint.coeffs, eq_constraint.variables),
            "=",
            rational_latex(eq_constraint.const)
        ]
        return Formula(formula_data)

    @formula
    def _fill_new_var(self):
        return Formula(f"x_{self.canonical_var_count}")

    @formula
    def _fill_new_var_expression(self):
        old_opt_sol = self.rsvm.opt_sol

        new_lpp = LPProblem(
            constraints=self.lp_problem.constraints + [self.new_constraint],
            objective=self.lp_problem.objective
        )
        old_opt_ext_basis_sol = BasisSolution(
            lp_problem=new_lpp,
            basis=list(old_opt_sol.basis) + [self.canonical_var_count],
            free=old_opt_sol.free
        )
        new_constraint_expression = expression_latex(
            coeffs=old_opt_ext_basis_sol.basis_coeffs[-1],
            variables=old_opt_ext_basis_sol.free_variables,
            constant=old_opt_ext_basis_sol.basis_values[-1]
        )
        formula_data = [f"x_{new_lpp.canonical_form.var_count} = ", new_constraint_expression]
        return Formula(formula_data)
