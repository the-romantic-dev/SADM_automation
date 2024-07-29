from pathlib import Path

from docx import Document
from sympy import latex, Matrix

from report.docx.pretty_omml import sympy_matrix_to_omml
from report.model.document_template import DocumentTemplate
from report.model.formula import Formula
from report.model.template_filler import TemplateFiller
from tasks.task1_2_lp.document_template.opt_part_tf import OptPartTF
from tasks.task1_2_lp.document_template.util import P_matrix, P_latex, CTB_latex, CTB_vector
from tasks.task1_2_lp.local_definitions import TASK_DIR
from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution


class MatrixSymplexStepTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, basis_solution: BasisSolution, solution_index: int):
        super().__init__(template)
        self.basis_solution = basis_solution
        self.solution_index = solution_index

    @TemplateFiller.filler_method
    def _fill_index(self):
        self.template.insert_text(key="index", text=str(self.solution_index))

    @TemplateFiller.filler_method
    def _fill_basis_variables(self):
        formula_data = ",".join([latex(variable) for variable in self.basis_solution.basis_variables])
        formula = Formula(formula_data)
        self.template.insert_formula(key="basis_variables", formula=formula)

    @TemplateFiller.filler_method
    def _fill_P_matrix(self):
        formula = Formula(f"P_{self.solution_index}")
        self.template.insert_formula(key="P_matrix", formula=formula)

    @TemplateFiller.filler_method
    def _fill_P_matrix_equation(self):
        matrix = P_matrix(self.basis_solution)

        formula_data = [
            f"{P_latex(self.solution_index)} = ",
            sympy_matrix_to_omml(matrix)
        ]
        formula = Formula(formula_data)
        self.template.insert_formula(key="P_matrix_equation", formula=formula)

    @TemplateFiller.filler_method
    def _fill_P_inverse_matrix(self):
        formula_data = f"P_{self.solution_index}^{{-1}}"
        formula = Formula(formula_data)
        self.template.insert_formula(key="P_inverse_matrix", formula=formula)

    @TemplateFiller.filler_method
    def _fill_P_inverse_matrix_equation(self):
        matrix = P_matrix(self.basis_solution).inv()
        formula_data = [
            f"{P_latex(self.solution_index)}^{{-1}} = ",
            sympy_matrix_to_omml(matrix)
        ]
        formula = Formula(formula_data)
        self.template.insert_formula(key="P_inverse_matrix_equation", formula=formula)

    @TemplateFiller.filler_method
    def _fill_CTB_vector(self):
        formula = Formula(CTB_latex(self.solution_index))
        self.template.insert_formula(key="CTB_vector", formula=formula)

    @TemplateFiller.filler_method
    def _fill_CTB_vector_equation(self):
        vector = CTB_vector(self.basis_solution)
        formula = Formula([
            f"{CTB_latex(self.solution_index)} = ",
            sympy_matrix_to_omml(vector)
        ])
        self.template.insert_formula(key="CTB_vector_equation", formula=formula)

    @TemplateFiller.filler_method
    def _fill_deltas_equations(self):
        formulas_list = []
        for i, var_i in enumerate(self.basis_solution.free):
            ctb_vector = CTB_vector(self.basis_solution)
            p_matrix = P_matrix(self.basis_solution).inv()
            a_column = self.basis_solution.lp_problem.canonical_form.matrices[0].col(var_i)
            c_elem = self.basis_solution.lp_problem.canonical_form.matrices[2][var_i, 0]
            result = (ctb_vector * p_matrix * a_column)[0, 0] - c_elem
            formula_data = [
                f"\\Delta_{var_i + 1} = ",
                CTB_latex(self.solution_index),
                f"{P_latex(self.solution_index)}^{{-1}}",
                f"A_{var_i + 1} - ",
                f"c_{var_i + 1} = ",
                sympy_matrix_to_omml(ctb_vector),
                sympy_matrix_to_omml(p_matrix),
                sympy_matrix_to_omml(a_column),
                f" - {c_elem} = ",
                f"{latex(result)}"
            ]
            formula = Formula(formula_data)
            formulas_list.append(formula)
        self.template.insert_formulas_list(key="deltas_equations", formulas_list=formulas_list)

    @TemplateFiller.filler_method
    def _fill_opt_dependency_part(self):
        TEMPLATES_DIR = Path(TASK_DIR, "templates/sabonis/matrix_symplex/")
        if self.basis_solution.is_opt:
            template_path = Path(TEMPLATES_DIR, "opt_part.docx")
        else:
            template_path = Path(TEMPLATES_DIR, "non_opt_part.docx")

        template = DocumentTemplate(template_path)
        if self.basis_solution.is_opt:
            tf = OptPartTF(template, basis_solution=self.basis_solution, solution_index=self.solution_index)
            tf.fill()
        else:
            return

        self.template.insert_data_from_document(key="opt_dependency_part", document=template.document)