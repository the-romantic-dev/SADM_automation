from copy import deepcopy

from sympy import Matrix, Expr

from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator
from tasks.task1_2_lp.model.lp_problem.enums.objective_type import ObjectiveType
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective


class LPProblem:
    def __init__(self, constraints: list[Constraint], objective: Objective):
        self._constraints = constraints
        self._objective = objective

    @property
    def constraints(self):
        return self._constraints

    @property
    def var_count(self):
        return self._objective.vars_count

    @property
    def objective(self):
        return self._objective

    @property
    def matrices(self) -> tuple[Matrix, Matrix, Matrix]:
        """
        Возвращает матрицы (sympy.Matrix):
         - матрицу коэффициентов ограничений A
         - матрицу (вектор) констант b
         - матрицу (вектор) коэффициентов целевой функции
         """
        A = []
        b = []
        c = self._objective.coeffs
        for con in self._constraints:
            A.append(con.coeffs)
            b.append(con.const)

        return Matrix(A), Matrix(b), Matrix(c)

    @property
    def constraints_expressions(self) -> list[Expr]:
        result = []
        for i in self._constraints:
            result.append(i.as_expr)
        return result

    @property
    def is_canonical(self):
        """
        Проверка, является ли форма задачи ЛП канонической
        """
        return self._is_all_eq() and self._is_consts_positive() and self._objective.type == ObjectiveType.MAX

    @property
    def start_basis(self) -> list[int]:
        # TODO изменить на поиск базиса
        return [2, 3]

    @property
    def canonical_form(self):
        """
        Возвращает каноническую форму задачи ЛП. Каноническая форма должна соответствовать следующим критериям:
            - поиск максимума целевой функции
            - неотрицательный вектор констант b
            - все переменные неотрицательные
            - все ограничения представлены равенствами
        """
        if self.is_canonical:
            return self

        new_constraints = []
        total_vars = self.var_count
        for c in self._constraints:
            new_c = c.eq_form(art_var_index=total_vars)
            if new_c.const < 0:
                new_c = -new_c
            if not c.is_eq:
                total_vars += 1
            new_constraints.append(new_c)

        for c in new_constraints:
            c.expand_coefs(total_vars)

        new_objective = deepcopy(self._objective)
        new_objective.expand_coefs(total_vars)
        if new_objective.type == ObjectiveType.MIN:
            new_objective = -new_objective

        return LPProblem(constraints=new_constraints, objective=new_objective)

    def _is_all_eq(self):
        result = True
        for con in self._constraints:
            if con.comp_operator != CompOperator.EQ:
                result = False
                break
        return result

    def _is_consts_positive(self):
        result = True
        for con in self._constraints:
            if con.const < 0:
                result = False
                break
        return result

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        result = [str(self._objective)]
        for c in self._constraints:
            result.append(str(c))

        return "\n".join(result)

    def __repr__(self):
        return str(self)
