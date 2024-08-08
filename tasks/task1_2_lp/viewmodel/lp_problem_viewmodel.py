from sympy import sign, symbols

from report.model.report_prettifier import expression_latex, rational_latex
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator
from tasks.task1_2_lp.model.lp_problem.enums.objective_type import ObjectiveType
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective


def get_non_negative_vars_latex(vars_count: int):
    result = [f"x_{i + 1} \\ge 0" for i in range(vars_count)]
    return ",".join(result)


def problem_latex(lp_problem: LPProblem) -> list[str]:
    def comp_operator_sign(operator: CompOperator):
        match operator:
            case CompOperator.LE:
                return "\\le"
            case CompOperator.GE:
                return "\\ge"
            case CompOperator.EQ:
                return "="

    obj = lp_problem.objective
    constraints = lp_problem.constraints
    result = []
    # obj_variables = obj.variables
    # obj_coeffs = obj.coeffs
    # for i in range(len(obj_coeffs)):
    #     if obj_coeffs[i] >= LPProblem.M:
    #         obj_variables[i] *= sign(obj_coeffs[i]) * symbols('M')
    obj_latex = f"max({expression_latex(obj.coeffs, obj.variables, obj.const)})"
    result.append(obj_latex)
    for constraint in constraints:
        constraint_expression_latex = expression_latex(constraint.coeffs, constraint.variables)
        constraint_latex = f"{constraint_expression_latex}{comp_operator_sign(constraint.comp_operator)}{rational_latex(constraint.const)}"
        result.append(constraint_latex)
    result.append(get_non_negative_vars_latex(lp_problem.var_count))
    return result


class LPProblemViewModel:
    def __init__(self, lp_problem: LPProblem):
        self.lp_problem = lp_problem

    def problem_latex(self) -> list[str]:
        return problem_latex(self.lp_problem)

    def canonical_problem_latex(self) -> list[str]:
        return problem_latex(self.lp_problem.canonical_form)

    def auxiliary_form_latex(self) -> list[str]:
        return problem_latex(self.lp_problem.auxiliary_form)

    def art_form_latex(self) -> list[str]:
        constraints = self.lp_problem.auxiliary_form.constraints
        m_sym = symbols('M')
        art_form_obj_coeffs = []
        obj_coeffs = self.lp_problem.canonical_form.objective.coeffs
        auxiliary_obj_coeffs = self.lp_problem.auxiliary_form.objective.coeffs
        for i in range(len(auxiliary_obj_coeffs)):
            if i < len(obj_coeffs):
                art_form_obj_coeffs.append(obj_coeffs[i])
            else:
                art_form_obj_coeffs.append(-m_sym)

        objective = Objective(
            obj_type=ObjectiveType.MAX,
            coeffs=art_form_obj_coeffs,
            const=self.lp_problem.objective.const)
        art_form_problem = LPProblem(constraints=constraints, objective=objective)
        return problem_latex(art_form_problem)
