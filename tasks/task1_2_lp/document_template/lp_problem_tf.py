from pathlib import Path

from sympy import symbols, Rational

from report.docx.pretty_omml import sympy_matrix_to_omml, replace_rationals_expr
from report.model.document_template import DocumentTemplate
from report.model.formula import Formula
from report.model.template_filler import TemplateFiller
from tasks.task1_2_lp.document_template.bruteforce_step_tf import BruteforceStepTF
from tasks.task1_2_lp.document_template.matrix_symplex_step_tf import MatrixSymplexStepTF
from tasks.task1_2_lp.document_template.util import eq_latex
from tasks.task1_2_lp.local_definitions import TASK_DIR
from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.models.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.solvers.bruteforce_solver.bruteforce_solver import BruteforceSolver
from tasks.task1_2_lp.solvers.symplex_solver.symplex_solver import get_next_basis, SymplexSolver


class LPProblemTF(TemplateFiller):
    def __init__(self, variant: int, lp_problem: LPProblem, template: DocumentTemplate):
        self.variant = variant
        self.lp_problem = lp_problem
        bruteforce_solver = BruteforceSolver(lp_problem=self.lp_problem)
        self.bruteforce_solution, self.best_bruteforce_solution_index = bruteforce_solver.solve()
        self.symplex_solution = SymplexSolver(lp_problem).solve()
        super().__init__(template)

    @TemplateFiller.filler_method
    def _fill_variant(self):
        self.template.insert_text(key="variant", text=str(self.variant))

    @TemplateFiller.filler_method
    def _fill_problem(self):
        formulas_list = []
        for ltx in self.lp_problem.get_latex_list():
            formula = Formula([ltx])
            formulas_list.append(formula)
        self.template.insert_formulas_list(key="problem", formulas_list=formulas_list)

    @TemplateFiller.filler_method
    def _fill_canonical_form_problem(self):
        formulas_list = []
        for ltx in self.lp_problem.canonical_form.get_latex_list():
            formula = Formula([ltx])
            formulas_list.append(formula)
        self.template.insert_formulas_list(key="canonical_form_problem", formulas_list=formulas_list)

    @TemplateFiller.filler_method
    def _fill_bruteforce_solution(self):
        TEMPLATES_DIR = Path(TASK_DIR, "templates/sabonis/bruteforce/")
        template_path = Path(TEMPLATES_DIR, "brutforce_step.docx")

        filled_documents = []
        for i, sol in enumerate(self.bruteforce_solution):
            bruteforce_step_template = DocumentTemplate(template_path)
            bruteforce_step_tf = BruteforceStepTF(bruteforce_step_template, solution_index=i, basis_solution=sol)
            bruteforce_step_tf.fill()

            filled_documents.append(bruteforce_step_tf.template.document)
        self.template.insert_data_from_documents_list(key="bruteforce_solution", documents=filled_documents)

    @TemplateFiller.filler_method
    def _fill_bruteforce_result(self):
        best_solution: BasisSolution = self.bruteforce_solution[self.best_bruteforce_solution_index]
        variables = best_solution.basis_variables + best_solution.free_variables + (symbols('f'),)
        basis_values = [replace_rationals_expr(expr) for expr in best_solution.basis_values]
        values = basis_values + [Rational(0), Rational(0)] + [replace_rationals_expr(best_solution.objective_value)]
        formula_latex = ",".join(f"{eq_latex(variables[i], values[i])}" for i in range(len(variables)))
        formula = Formula(formula_latex)
        self.template.insert_formula(key="bruteforce_result", formula=formula)

    @TemplateFiller.filler_method
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
        formula = Formula(formula_elements)
        self.template.insert_formula(key="canonical_matrices", formula=formula)

    @TemplateFiller.filler_method
    def _fill_matrix_symplex_solution(self):
        TEMPLATES_DIR = Path(TASK_DIR, "templates/sabonis/matrix_symplex/")
        template_path = Path(TEMPLATES_DIR, "matrix_symplex_step.docx")

        filled_documents = []
        for i, sol in enumerate(self.symplex_solution):
            matrix_symplex_step_template = DocumentTemplate(template_path)
            matrix_symplex_step_tf = MatrixSymplexStepTF(matrix_symplex_step_template, solution_index=i, basis_solution=sol)
            matrix_symplex_step_tf.fill()

            filled_documents.append(matrix_symplex_step_tf.template.document)
        self.template.insert_data_from_documents_list(key="matrix_symplex_solution", documents=filled_documents)
