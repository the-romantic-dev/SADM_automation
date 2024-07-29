import pytest
from sympy import Rational

from tasks.task1_2_lp.models.constraint.constraint import Constraint
from tasks.task1_2_lp.models.enums.comp_operator import CompOperator
from tasks.task1_2_lp.models.enums.objective_type import ObjectiveType
from tasks.task1_2_lp.models.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.models.objective.objective import Objective


@pytest.mark.parametrize(
    "problem, expected",
    [
        (
                LPProblem(
                    [
                        Constraint([Rational(1), Rational(2)], Rational(5), CompOperator.LE),
                        Constraint([Rational(6), Rational(8)], Rational(3), CompOperator.LE)
                    ],
                    Objective(ObjectiveType.MAX, [Rational(1), Rational(-7)])
                ),
                LPProblem(
                    [
                        Constraint([Rational(1), Rational(2), Rational(1), Rational(0)], Rational(5), CompOperator.EQ),
                        Constraint([Rational(6), Rational(8), Rational(0), Rational(1)], Rational(3), CompOperator.EQ)
                    ],
                    Objective(ObjectiveType.MAX, [Rational(1), Rational(-7), Rational(0), Rational(0)])
                )

        ),
        (
                LPProblem(
                    [
                        Constraint([Rational(1), Rational(2)], Rational(5), CompOperator.EQ),
                        Constraint([Rational(6), Rational(8)], Rational(3), CompOperator.EQ)
                    ],
                    Objective(ObjectiveType.MAX, [Rational(1), Rational(-7)])
                ),
                LPProblem(
                    [
                        Constraint([Rational(1), Rational(2)], Rational(5), CompOperator.EQ),
                        Constraint([Rational(6), Rational(8)], Rational(3), CompOperator.EQ)
                    ],
                    Objective(ObjectiveType.MAX, [Rational(1), Rational(-7)])
                )

        )
    ]
)
def test_canonical_form(problem: LPProblem, expected: LPProblem):
    cf = problem.canonical_form
    assert cf == expected
