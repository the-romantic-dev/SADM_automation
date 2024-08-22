import os
from pathlib import Path

from report.model.elements.formula import Formula
from report.model.elements.paragraph import Paragraph
from report.model.elements.plain_text import PlainText
from report.model.report_prettifier import expr_latex
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula, elements_list
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.model.solvers.symplex_solver.symplex_solver import SymplexSolver
from tasks.task1_2_lp.view.solution_tf import SolutionTF
from tasks.task1_2_lp.view.symplex.table_symplex_solution.symplex_table import SymplexTable
from tasks.task1_2_lp.viewmodel.basis_solution_viewmodel import BasisSolutionViewModel
from tasks.task1_2_lp.viewmodel.reverse_symplex_viewmodel import ReverseSymplexViewModel

package_path = Path(os.path.dirname(os.path.abspath(__file__)))
template_path = Path(package_path, "reverse_symplex.docx")


@sub_tf
class ReverseSymplexTF(SolutionTF):
    def __init__(self, opt_sol: BasisSolution, new_constraint: Constraint):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.opt_sol = opt_sol
        self.new_constraint = new_constraint
        lpp = opt_sol.lp_problem
        self.new_lpp = LPProblem(constraints=lpp.constraints + [self.new_constraint], objective=lpp.objective)
        self.new_var = lpp.canonical_form.var_count
        self.new_basis = list(self.opt_sol.basis) + [self.new_var]
        self.rsvm = ReverseSymplexViewModel(new_var=self.new_var, new_constraint=self.new_constraint)
        solver = SymplexSolver(lp_problem=self.new_lpp)
        self.solution_steps, self.swaps = solver.solve(start_basis=self.new_basis, is_reversed=True)

    @formula
    def _fill_new_constraint(self):
        return self.rsvm.new_constraint_formula

    @formula
    def _fill_new_canonical_constraint(self):
        return self.rsvm.new_constraint_canonical_formula

    @formula
    def _fill_new_var(self):
        return Formula(f"x_{self.new_var + 1}")

    @formula
    def _fill_new_var_expression(self):
        old_opt_sol = self.opt_sol

        new_lpp = self.new_lpp
        old_opt_ext_basis_sol = BasisSolution(
            lp_problem=new_lpp,
            basis=self.new_basis,
            free=old_opt_sol.free
        )
        new_constraint_expression = expr_latex(
            coeffs=old_opt_ext_basis_sol.basis_coeffs[-1],
            variables=old_opt_ext_basis_sol.free_variables,
            constant=old_opt_ext_basis_sol.basis_values[-1]
        )
        formula_data = [f"x_{new_lpp.canonical_form.var_count} = ", new_constraint_expression]
        return Formula(formula_data)

    @elements_list
    def _fill_reverse_symplex_steps(self):
        _elements_list = []
        solutions, swaps = self.solution_steps, self.swaps
        for i, sol in enumerate(solutions):
            swap = swaps[i] if i < len(swaps) else None
            symplex_table = SymplexTable(sol, swap, is_reversed=True)
            basis_variables_latex = BasisSolutionViewModel(sol).basis_variables_latex
            paragraph_data = [
                PlainText(text=f"Псевдоплан {i}: ", bold=True, italic=False, size=28),
                Formula(",".join(basis_variables_latex), font_size=28, bold=True)
            ]
            _elements_list.append(Paragraph(paragraph_data))
            _elements_list.append(symplex_table.symplex_table)
        return _elements_list

    @formula
    def _fill_result(self):
        return self.result_formula(self.solution_steps[-1])
