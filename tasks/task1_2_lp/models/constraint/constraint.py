from copy import deepcopy
from typing import Type

from sympy import Rational, Eq, symbols, pretty, Equality, Le, GreaterThan, LessThan, Ge, latex

from report.docx.pretty_omml import replace_rationals_expr
from tasks.task1_2_lp.models.enums.comp_operator import CompOperator


class Constraint:
    def __init__(self, coefs: list[Rational], const: Rational, comp_operator: CompOperator = CompOperator.LE):
        self._coefs = coefs
        self._comp_operator = comp_operator
        self._const = const

    @property
    def const(self):
        return self._const

    def __neg__(self):
        coefs = [i * -1 for i in self.coefs]
        const = self.const * -1
        comp_operator = None
        match self._comp_operator:
            case CompOperator.EQ:
                comp_operator = CompOperator.EQ
            case CompOperator.LE:
                comp_operator = CompOperator.GE
            case CompOperator.GE:
                comp_operator = CompOperator.LE
        return Constraint(coefs, const, comp_operator)

    @property
    def vars_count(self):
        return len(self._coefs)

    @property
    def coefs(self):
        return self._coefs.copy()

    @property
    def comp_operator(self):
        return self._comp_operator

    @property
    def is_eq(self):
        return self._comp_operator == CompOperator.EQ

    def eq_form(self, art_var_index: int):
        """ Преобразовывает неравенство в равенство с помощью добавления искусственной переменной """
        eq_op = CompOperator.EQ
        if art_var_index < len(self._coefs):
            raise ValueError("Индекс икусственной переменной должен быть больше существующих")
        if self._comp_operator == CompOperator.EQ:
            return Constraint(coefs=self.coefs, comp_operator=eq_op, const=self.const)
        else:
            expanded_coefs = [self._coefs[i] if i < len(self._coefs) else Rational(0) for i in range(art_var_index)]
            if self._comp_operator == CompOperator.LE:
                expanded_coefs.append(Rational(1))
            else:
                expanded_coefs.append(Rational(-1))
            return Constraint(coefs=expanded_coefs, comp_operator=eq_op, const=self.const)

    @property
    def as_expr(self) -> Type[Equality | GreaterThan | LessThan]:
        """ Возвращает выражение sympy (Equality | GreaterThan | LessThan) """
        x = symbols(f"x(1:{len(self._coefs) + 1})")
        terms = [x[i] * self._coefs[i] for i in range(len(self._coefs))]

        match self._comp_operator:
            case CompOperator.EQ:
                return Eq(sum(terms), self.const)
            case CompOperator.LE:
                return Le(sum(terms), self.const)
            case CompOperator.GE:
                return Ge(sum(terms), self.const)

    @property
    def as_latex(self):
        float_expr = replace_rationals_expr(self.as_expr)
        return latex(float_expr)

    def expand_coefs(self, total_vars: int):
        for _ in range(total_vars - len(self._coefs)):
            self._coefs.append(Rational(0))

    def __str__(self):
        eq = self.as_expr
        return pretty(eq)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            coefs_eq = self._coefs == other._coefs
            const_eq = self._const == other._const
            comp_op_eq = self._comp_operator == other._comp_operator
            return coefs_eq and const_eq and comp_op_eq
        else:
            return False

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
