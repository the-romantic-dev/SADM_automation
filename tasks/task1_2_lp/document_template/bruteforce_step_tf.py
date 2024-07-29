from pathlib import Path
from sympy import latex, symbols

from report.docx.pretty_omml import replace_rationals_expr
from report.model.document_template import DocumentTemplate
from report.model.formula import Formula
from report.model.template_filler import TemplateFiller
from tasks.task1_2_lp.document_template.acceptability_marker_tf import AcceptabilityMarkerTF
from tasks.task1_2_lp.document_template.util import eq_latex
from tasks.task1_2_lp.local_definitions import TASK_DIR
from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution



class BruteforceStepTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate, solution_index: int, basis_solution: BasisSolution):
        self.basis_solution = basis_solution
        self.solution_index = solution_index
        super().__init__(template)

    @TemplateFiller.filler_method
    def _fill_solution_index(self):
        self.template.insert_text(key="solution_index", text=str(self.solution_index + 1))

    @TemplateFiller.filler_method
    def _fill_basis_variables(self):
        formula_latex = ",".join([latex(x) for x in self.basis_solution.basis_variables])
        formula = Formula(formula_latex)
        self.template.insert_formula(key="basis_variables", formula=formula)

    @TemplateFiller.filler_method
    def _fill_expressions(self):
        basis_expressions = [replace_rationals_expr(expr) for expr in self.basis_solution.basis_expressions]
        basis_variables = self.basis_solution.basis_variables
        formulas_list = []
        for i, variable in enumerate(basis_variables):
            formula = Formula(eq_latex(variable, basis_expressions[i]))
            formulas_list.append(formula)

        f = symbols('f')
        expr = replace_rationals_expr(self.basis_solution.objective_expression)
        objective_formula = Formula(eq_latex(f, expr))
        formulas_list.append(objective_formula)
        self.template.insert_formulas_list(key="expressions", formulas_list=formulas_list)

    @TemplateFiller.filler_method
    def _fill_values(self):
        basis_values = self.basis_solution.basis_values
        objective_value = self.basis_solution.objective_value
        basis_variables = self.basis_solution.basis_variables
        f = symbols('f')
        variables = [*basis_variables, f]
        values = [replace_rationals_expr(v) for v in [*basis_values, objective_value]]
        formulas_list = []
        for i, variable in enumerate(variables):
            formula = Formula(eq_latex(variable, values[i]))
            formulas_list.append(formula)
        self.template.insert_formulas_list(key="values", formulas_list=formulas_list)

    @TemplateFiller.filler_method
    def _fill_acceptable_marker(self):
        template_path = Path(TASK_DIR, "templates/sabonis/bruteforce/acceptability_marker.docx")
        acceptability_marker_tf = AcceptabilityMarkerTF(
            template=DocumentTemplate(template_path),
            unacceptable_variables=self.basis_solution.unacceptable_vars_indices
        )
        key = "acceptable_marker"
        if self.basis_solution.is_acceptable:
            self.template.delete_key(key)
        else:
            acceptability_marker_tf.fill()
            filled_document = acceptability_marker_tf.template.document
            self.template.insert_data_from_document(key=key, document=filled_document)
