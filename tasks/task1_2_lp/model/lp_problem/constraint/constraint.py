from copy import deepcopy
from typing import Type

from sympy import Rational, Eq, symbols, pretty, Equality, Le, GreaterThan, LessThan, Ge, Symbol
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator


class Constraint:
    """ Класс представляет ограничение задачи линейного программирования """

    def __init__(self, coeffs: list[Rational], const: Rational, comp_operator: CompOperator = CompOperator.LE,
                 variable_symbol: str = "x"):
        """
        :param coeffs: коэффициенты при переменных левой части ограничения
        :param const: константа в правой части ограничения
        :param comp_operator: оператор сравнения в ограничении (=, <= или >=)
        """
        self.variable_symbol = variable_symbol
        self._coeffs = coeffs
        self._comp_operator = comp_operator
        self._const = const

    @property
    def const(self):
        """ Константа в правой части ограничения """
        return self._const

    def __neg__(self):
        coeffs = [i * -1 for i in self.coeffs]
        const = self.const * -1
        comp_operator = None
        match self._comp_operator:
            case CompOperator.EQ:
                comp_operator = CompOperator.EQ
            case CompOperator.LE:
                comp_operator = CompOperator.GE
            case CompOperator.GE:
                comp_operator = CompOperator.LE
        return Constraint(coeffs, const, comp_operator)

    @property
    def vars_count(self):
        """ Количество переменных в ограничении """
        return len(self._coeffs)

    @property
    def variables(self) -> list[Symbol]:
        return list(symbols(f"{self.variable_symbol}(1:{self.vars_count + 1})"))

    @property
    def coeffs(self):
        return self._coeffs.copy()

    @property
    def comp_operator(self):
        return self._comp_operator

    @property
    def is_eq(self):
        return self._comp_operator == CompOperator.EQ

    def eq_form(self, art_var_index: int):
        """ Преобразовывает неравенство в равенство с помощью добавления искусственной переменной """
        eq_op = CompOperator.EQ
        if art_var_index < len(self._coeffs):
            raise ValueError("Индекс икусственной переменной должен быть больше существующих")
        if self._comp_operator == CompOperator.EQ:
            return Constraint(coeffs=self.coeffs, comp_operator=eq_op, const=self.const)
        else:
            expanded_coefs = [self._coeffs[i] if i < len(self._coeffs) else Rational(0) for i in range(art_var_index)]
            if self._comp_operator == CompOperator.LE:
                expanded_coefs.append(Rational(1))
            else:
                expanded_coefs.append(Rational(-1))
            return Constraint(coeffs=expanded_coefs, comp_operator=eq_op, const=self.const)

    @property
    def as_expr(self) -> Type[Equality | GreaterThan | LessThan]:
        """ Возвращает выражение sympy (Equality | GreaterThan | LessThan) """
        x = self.variables
        terms = [x[i] * self._coeffs[i] for i in range(len(self._coeffs))]

        match self._comp_operator:
            case CompOperator.EQ:
                return Eq(sum(terms), self.const)
            case CompOperator.LE:
                return Le(sum(terms), self.const)
            case CompOperator.GE:
                return Ge(sum(terms), self.const)

    def expand_coefs(self, total_vars: int):
        for _ in range(total_vars - len(self._coeffs)):
            self._coeffs.append(Rational(0))

    def __repr__(self):
        # return str(self.as_expr)
        return str(self.as_expr)

    def pretty_str(self):
        return pretty(self.as_expr)

    def __str__(self):
        return str(self.as_expr)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            coefs_eq = self._coeffs == other._coeffs
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
