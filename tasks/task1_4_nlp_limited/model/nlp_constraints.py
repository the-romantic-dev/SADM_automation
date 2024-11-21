from abc import ABC, abstractmethod
from typing import Type

from sympy import Rational, Symbol, symbols, Equality, GreaterThan, LessThan, Eq, Le, Ge

from tasks.task1_2_lp.model import Constraint, CompOperator


class NLPConstraint(ABC):
    def __init__(self, coeffs: list[int], const: int, comp_operator: CompOperator):
        self.coeffs = coeffs
        self.const = const
        self.comp_operator = comp_operator

    @property
    def vars_count(self):
        """ Количество переменных в ограничении """
        return len(self.coeffs)

    @property
    def variables(self) -> list[Symbol]:
        return list(symbols(f"x(1:{self.vars_count + 1})"))

    @property
    @abstractmethod
    def as_expr(self) -> Type[Equality | GreaterThan | LessThan]: ...


class NLPLinearConstraint(NLPConstraint):
    @property
    def as_expr(self) -> Type[Equality | GreaterThan | LessThan]:
        """ Возвращает выражение sympy (Equality | GreaterThan | LessThan) """
        x = self.variables
        terms = [x[i] * self.coeffs[i] for i in range(len(self.coeffs))]

        match self.comp_operator:
            case CompOperator.EQ:
                return Eq(sum(terms), self.const)
            case CompOperator.LE:
                return Le(sum(terms), self.const)
            case CompOperator.GE:
                return Ge(sum(terms), self.const)


class NLPSquareConstraint(NLPConstraint):
    @property
    def as_expr(self) -> Type[Equality | GreaterThan | LessThan]:
        """ Возвращает выражение sympy (Equality | GreaterThan | LessThan) """
        x = self.variables
        terms = [x[i] ** 2 * self.coeffs[i] for i in range(len(self.coeffs))]

        match self.comp_operator:
            case CompOperator.EQ:
                return Eq(sum(terms), self.const)
            case CompOperator.LE:
                return Le(sum(terms), self.const)
            case CompOperator.GE:
                return Ge(sum(terms), self.const)
