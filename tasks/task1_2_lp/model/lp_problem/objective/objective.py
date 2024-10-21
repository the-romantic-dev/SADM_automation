from copy import deepcopy

from sympy import Rational, symbols, pretty, Expr, Symbol

from tasks.task1_2_lp.model.lp_problem.enums.objective_type import ObjectiveType


class Objective:
    """ Класс, представляющий целевую функцию задачи линейного программирования """

    def __init__(self, obj_type: ObjectiveType, coeffs: list[Rational | Symbol], const: Rational = Rational(0),
                 variable_symbol: str = "x"):
        """
        :param obj_type: Тип задачи линейного программирования (максимизация или минимизация)
        :param coeffs: Коэффициенты переменных целевой функции
        :param const: Константная часть целевой функции. По умолчанию 0
        """
        self.variable_symbol = variable_symbol
        self._type = obj_type
        self._coeffs = coeffs
        self._const = const

    def __neg__(self):
        if self._type == ObjectiveType.MAX:
            new_type = ObjectiveType.MIN
        else:
            new_type = ObjectiveType.MAX

        coefs = [i * -1 for i in self.coeffs]
        const = self._const * -1
        return Objective(new_type, coefs, const, variable_symbol=self.variable_symbol)

    @property
    def type(self):
        """ Тип задачи линейного программирования (максимизация или минимизация) """
        return self._type

    @property
    def const(self):
        return self._const

    @property
    def variables(self):
        return list(symbols(f"{self.variable_symbol}(1:{self.vars_count + 1})"))

    @property
    def vars_count(self):
        """ Количество переменных в целевой функции """
        return len(self._coeffs)

    @property
    def coeffs(self):
        """ Коэффициенты переменных целевой функции """
        return self._coeffs.copy()

    def expand_coefs(self, total_vars: int):
        """ Расширить список коэффициентов до заданного количества переменных
         :param total_vars: Итоговое количество переменных
         """
        for _ in range(total_vars - len(self._coeffs)):
            self._coeffs.append(Rational(0))

    @property
    def as_expr(self) -> Expr:
        """ Целевая функция в виде :class:`sympy.Expr` """
        x = self.variables
        terms = [x[i] * self._coeffs[i] for i in range(len(self._coeffs))]
        return sum(terms) + self._const

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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __str__(self):
        expr_str = pretty(self.as_expr)
        if self._type == ObjectiveType.MAX:
            return f"max({expr_str})"
        else:
            return f"min({expr_str})"

    def __repr__(self):
        return str(self)
