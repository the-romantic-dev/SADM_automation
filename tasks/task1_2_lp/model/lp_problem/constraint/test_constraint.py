import pytest
from sympy import Rational, Le, Eq
from sympy import symbols as sym

from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator


@pytest.mark.parametrize(
    "constraint, art_var_index, expected",
    [
        (
                Constraint([Rational(1), Rational(2)], Rational(5), CompOperator.LE),
                2,
                Constraint([Rational(1), Rational(2), Rational(1)], Rational(5), CompOperator.EQ),
        ),
        (
                Constraint([Rational(1), Rational(2)], Rational(5), CompOperator.LE),
                3,
                Constraint([Rational(1), Rational(2), Rational(0), Rational(1)], Rational(5), CompOperator.EQ),
        ),
    ]
)
def test_eq_form(constraint: Constraint, art_var_index: int, expected):
    assert constraint.eq_form(art_var_index) == expected


@pytest.mark.parametrize(
    "constraint, expected",
    [
        (
                Constraint([Rational(1), Rational(2)], Rational(-5), CompOperator.LE),
                Constraint([Rational(-1), Rational(-2)], Rational(5), CompOperator.GE),
        ),
        (
                Constraint([Rational(1), Rational(2), Rational(0), Rational(-1)], Rational(-5), CompOperator.EQ),
                Constraint([Rational(-1), Rational(-2), Rational(0), Rational(1)], Rational(5), CompOperator.EQ),
        )
    ]
)
def test__neg__(constraint: Constraint, expected: Constraint):
    assert -constraint == expected
