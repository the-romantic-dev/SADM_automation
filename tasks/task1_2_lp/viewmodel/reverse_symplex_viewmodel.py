from report.model.elements.formula import Formula
from report.model.report_prettifier import expr_latex, rational_latex
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint


class ReverseSymplexViewModel:
    def __init__(self, new_var: int, new_constraint: Constraint):
        self.new_constraint = new_constraint
        self.new_var = new_var

    @property
    def new_constraint_formula(self):
        formula_data = [
            expr_latex(self.new_constraint.coeffs, self.new_constraint.variables),
            "\\le",
            rational_latex(self.new_constraint.const)
        ]
        return Formula(formula_data)

    @property
    def new_constraint_canonical_formula(self):
        eq_constraint = self.new_constraint.eq_form(self.new_var)
        formula_data = [
            expr_latex(eq_constraint.coeffs, eq_constraint.variables),
            "=",
            rational_latex(eq_constraint.const)
        ]
        return Formula(formula_data)
