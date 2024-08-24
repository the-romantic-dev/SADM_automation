from pathlib import Path

from report.model.elements.pretty_elements import sympy_matrix_to_omml
from report.model.docx_parts.formula import Formula
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import formula, elements_list
from report.model.template.tf_decorators import sub_tf
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.view.solution_tf import SolutionTF
from tasks.task1_2_lp.view.symplex.matrix_symplex_solution.matrix_symplex_step.matrix_symplex_step_tf import \
    MatrixSymplexStepTF
from tasks.task1_2_lp.view.symplex.step_data import SymplexStepData

template_path = Path(Path(__file__).parent, "matrix_symplex_solution.docx")


@sub_tf
class MatrixSymplexSolutionTF(SolutionTF):
    def __init__(self, lpp: LPProblem, solutions: list[BasisSolution], swaps: list[tuple[int, int]],
                 start_basis_index: int):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.lpp = lpp
        self.solutions = solutions
        self.swaps = swaps
        self.start_basis_index = start_basis_index

    @formula
    def _fill_canonical_matrices(self):
        canonical_matrices = self.lpp.canonical_form.matrices
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
    def _fill_solution_steps(self):
        filled_documents = []
        for i, sol in enumerate(self.solutions):
            in_var = None
            out_var = None
            if i < len(self.swaps):
                swap = self.swaps[i]
                in_var = swap[1]
                out_var = swap[0]
            current_index = self.start_basis_index + i
            step_data = SymplexStepData(current_solution=sol, current_index=current_index, in_var=in_var,
                                        out_var=out_var)
            matrix_symplex_step_tf = MatrixSymplexStepTF(step_data)
            matrix_symplex_step_tf.fill()

            filled_documents.append(matrix_symplex_step_tf.template.document)
        return filled_documents

    @formula
    def _fill_result(self):
        return self.result_formula(self.solutions[-1])
