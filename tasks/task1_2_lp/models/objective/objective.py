from copy import deepcopy

from sympy import Rational, symbols, pretty, Expr, latex

from report.docx.pretty_omml import replace_rationals_expr
from tasks.task1_2_lp.models.enums.objective_type import ObjectiveType


class Objective:
    def __init__(self, obj_type: ObjectiveType, coefs: list[Rational], const: Rational = Rational(0)):
        self._type = obj_type
        self._coefs = coefs
        self._const = const

    def __neg__(self):
        if self._type == ObjectiveType.MAX:
            new_type = ObjectiveType.MIN
        else:
            new_type = ObjectiveType.MAX

        coefs = [i * -1 for i in self.coefs]
        const = self._const * -1
        return Objective(new_type, coefs, const)

    @property
    def type(self):
        return self._type

    @property
    def vars_count(self):
        return len(self._coefs)

    @property
    def coefs(self):
        return self._coefs.copy()

    def expand_coefs(self, total_vars: int):
        for _ in range(total_vars - len(self._coefs)):
            self._coefs.append(Rational(0))

    @property
    def as_expr(self) -> Expr:
        """ Возвращает выражение sympy"""
        x = symbols(f"x(1:{len(self._coefs) + 1})")
        terms = [x[i] * self._coefs[i] for i in range(len(self._coefs))]

        return sum(terms) + self._const

    @property
    def as_latex(self) -> str:
        float_expr = replace_rationals_expr(self.as_expr)
        return f"max({latex(float_expr)})"
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

    # def __key(self):
    #     return self._type, self._coefs, self._const
    #
    # def __hash__(self):
    #     return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __str__(self):
        # x = symbols(f"x(1:{len(self._coefs) + 1})")
        # terms = [x[i] * self._coefs[i] for i in range(len(self._coefs))]
        expr_str = pretty(self.as_expr)
        if self._type == ObjectiveType.MAX:
            return f"max({expr_str})"
        else:
            return f"min({expr_str})"

    def __repr__(self):
        return str(self)
