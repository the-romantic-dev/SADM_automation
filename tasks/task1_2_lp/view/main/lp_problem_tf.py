import os
from pathlib import Path

from report.docx.pretty_omml import sympy_matrix_to_omml
from report.model.elements.paragraph import Paragraph
from report.model.elements.plain_text import PlainText
from report.model.report_prettifier import rational_latex
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import text, elements_list, formula, document
from report.model.elements.formula import Formula
from report.model.template.template_filler import TemplateFiller
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.view.auxiliary_task.auxiliary_task_tf import AuxiliaryTaskTF
from tasks.task1_2_lp.view.bruteforce_step.bruteforce_step_tf import BruteforceStepTF
from tasks.task1_2_lp.view.reverse_symplex.reverse_symplex_tf import ReverseSymplexTF
from tasks.task1_2_lp.view.symplex.matrix_symplex.matrix_symplex_step.matrix_symplex_step_tf import MatrixSymplexStepTF
from tasks.task1_2_lp.view.symplex.table_symplex.symplex_table import SymplexTable
from tasks.task1_2_lp.view.symplex.step_data import SymplexStepData
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.model.solvers.bruteforce_solver.bruteforce_solver import BruteforceSolver
from tasks.task1_2_lp.model.solvers.symplex_solver.symplex_solver import SymplexSolver
from tasks.task1_2_lp.viewmodel.basis_solution_viewmodel import BasisSolutionViewModel
from tasks.task1_2_lp.viewmodel.lp_problem_viewmodel import LPProblemViewModel

package_path = Path(os.path.dirname(os.path.abspath(__file__)))
template_path = Path(package_path, "lp_problem.docx")


class LPProblemTF(TemplateFiller):
    def __init__(self, variant: int, lp_problem: LPProblem):
        self.variant = variant
        self.lp_problem = lp_problem
        self.lp_problem_vm = LPProblemViewModel(lp_problem)
        bruteforce_solver = BruteforceSolver(lp_problem=self.lp_problem)
        self.bruteforce_solution, self.best_bruteforce_solution_index = bruteforce_solver.solve()
        self.symplex_start_basis_index = 0
        symplex_solver = SymplexSolver(lp_problem)
        self.auxiliary_solution: list[BasisSolution] | None = None
        self.auxiliary_swaps: list[tuple[int, int]] | None = None
        if self.lp_problem.has_simple_start_basis:
            start_basis = self.lp_problem.start_basis
        else:
            self.auxiliary_solution, self.auxiliary_swaps = symplex_solver.auxiliary_solve()
            start_basis = self.auxiliary_solution[-1].basis
            self.symplex_start_basis_index = len(self.auxiliary_solution) - 1

        self.symplex_solution, self.symplex_swaps = symplex_solver.solve(start_basis)

        template = DocumentTemplate(template_path)
        super().__init__(template)

    @text
    def _fill_variant(self):
        return str(self.variant)

    @elements_list
    def _fill_problem(self):
        return [Formula(ltx) for ltx in self.lp_problem_vm.problem_latex()]

    @elements_list
    def _fill_canonical_form_problem(self):
        return [Formula(ltx) for ltx in self.lp_problem_vm.canonical_problem_latex()]

    @elements_list
    def _fill_bruteforce_solution(self):
        filled_documents = []
        for i, sol in enumerate(self.bruteforce_solution):
            bruteforce_step_tf = BruteforceStepTF(solution_index=i, basis_solution=sol)
            bruteforce_step_tf.fill()

            filled_documents.append(bruteforce_step_tf.template.document)
        return filled_documents

    @formula
    def _fill_result(self):
        best_solution = self.bruteforce_solution[self.best_bruteforce_solution_index]
        best_solution_vm = BasisSolutionViewModel(best_solution)
        basis_variables = best_solution_vm.basis_variables_latex
        free_variables = best_solution_vm.free_variables_latex
        f_variable = 'f'
        variables = basis_variables + free_variables + [f_variable]

        basis_values = [rational_latex(value) for value in best_solution.basis_values]
        free_values = ["0" for _ in range(len(best_solution.free))]
        f_value = rational_latex(best_solution.objective_value)
        values = basis_values + free_values + [f_value]

        formula_latex = ",".join(f"{variables[i]} = {values[i]}" for i in range(len(variables)))
        return Formula(formula_latex)

    @formula
    def _fill_canonical_matrices(self):
        canonical_matrices = self.lp_problem.canonical_form.matrices
        formula_elements = [
            "A = ",
            sympy_matrix_to_omml(canonical_matrices[0]),
            ", ",
            f"b = ",
            sympy_matrix_to_omml(canonical_matrices[1]),
            ", ",
            f"C^T = ",
            sympy_matrix_to_omml(canonical_matrices[2].T),
        ]
        return Formula(formula_elements)

    @elements_list
    def _fill_matrix_symplex_solution(self):
        filled_documents = []
        for i, sol in enumerate(self.symplex_solution):
            in_var = None
            out_var = None
            if i < len(self.symplex_swaps):
                swap = self.symplex_swaps[i]
                in_var = swap[1]
                out_var = swap[0]
            current_index = self.symplex_start_basis_index + i
            step_data = SymplexStepData(current_solution=sol, current_index=current_index, in_var=in_var,
                                        out_var=out_var)
            matrix_symplex_step_tf = MatrixSymplexStepTF(step_data)
            matrix_symplex_step_tf.fill()

            filled_documents.append(matrix_symplex_step_tf.template.document)
        return filled_documents

    @elements_list
    def _fill_table_symplex_solution(self):
        _elements_list = []
        for i, sol in enumerate(self.symplex_solution):
            swap = self.symplex_swaps[i] if i < len(self.symplex_swaps) else None
            symplex_table = SymplexTable(sol, swap)
            basis_variables_latex = BasisSolutionViewModel(sol).basis_variables_latex
            current_index = self.symplex_start_basis_index + i
            paragraph_data = [
                PlainText(text=f"Базис {current_index}: ", bold=True, italic=False, size=28),
                Formula(",".join(basis_variables_latex), font_size=28, bold=True)
            ]
            _elements_list.append(Paragraph(paragraph_data))
            _elements_list.append(symplex_table.table)
        return _elements_list

    @document
    def _fill_auxiliary_task(self):
        if self.auxiliary_solution is None:
            return None
        template_filler = AuxiliaryTaskTF(self.lp_problem, auxiliary_solution=self.auxiliary_solution,
                                          auxiliary_swaps=self.auxiliary_swaps)
        template_filler.fill()
        return template_filler.template.document

    @document
    def _fill_reverse_symplex(self):
        tf = ReverseSymplexTF(self.bruteforce_solution)
        tf.fill()
        return tf.template.document
