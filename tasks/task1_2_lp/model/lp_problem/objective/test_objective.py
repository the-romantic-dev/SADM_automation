import pytest
from sympy import Rational

from tasks.task1_2_lp.model.lp_problem.enums.objective_type import ObjectiveType
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective


@pytest.mark.parametrize(
    "objective, total_vars, expected",
    [
        (
                Objective(ObjectiveType.MAX, [Rational(1), Rational(2)]),
                3,
                [Rational(1), Rational(2), Rational(0)]
        ),
        (
                Objective(ObjectiveType.MAX, [Rational(1), Rational(2)]),
                1,
                [Rational(1), Rational(2)]
        ),
        (
                Objective(ObjectiveType.MAX, [Rational(1), Rational(2), Rational(0), Rational(15)]),
                7,
                [Rational(1), Rational(2), Rational(0), Rational(15), Rational(0), Rational(0), Rational(0)]
        )
    ]
)
def test__expand_coefs(objective: Objective, total_vars: int, expected: list[Rational]):
    objective.expand_coefs(total_vars)
    assert objective.coeffs == expected

