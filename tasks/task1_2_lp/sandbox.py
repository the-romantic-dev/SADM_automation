from sympy import Rational, symbols

from report.model.report_prettifier import coeff_with_symbol_latex
from tasks.task1_2_lp.model import LPProblem, Objective, ObjectiveType, Constraint, CompOperator, BasisSolution
from tasks.task1_2_lp.model.solvers import SymplexSolver, BruteforceSolver

lpp = LPProblem(
    objective=Objective(obj_type=ObjectiveType.MIN, coeffs=[Rational(23, 5), Rational(37, 10)], variable_symbol='y'),
    constraints=[
        Constraint([Rational(1), Rational('3.5')], Rational('1'), CompOperator.GE, variable_symbol='y'),
        Constraint([Rational('1.4'), Rational(1)], Rational('2'), CompOperator.GE, variable_symbol='y')
    ]
)

if __name__ == '__main__':
    print(lpp.canonical_form)
    a = BruteforceSolver(lpp).solve()[0]
    for i in a:
        print(i)