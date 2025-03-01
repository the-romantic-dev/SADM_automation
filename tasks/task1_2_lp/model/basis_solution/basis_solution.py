from __future__ import annotations

from functools import cached_property

import numpy as np
from sympy import symbols, solve, Expr, Symbol, Rational, pretty, Matrix, sqrt
from tasks.task1_2_lp.model import LPProblem, Constraint


class BasisSolution:
    """ Класс представляющий решение задачи линейного программирования в определенном базисе """

    def __init__(self, lp_problem: LPProblem, basis: list[int], free: list[int] = None):
        """
        :param lp_problem: экземпляр задачи линейного программирования
        :param basis: базис в котором нужно искать решение
        :param free: необязательный параметр, нужен в случае, если порядок свободных переменных имеет значение
        """
        self.lp_problem = lp_problem
        self.basis = basis
        self._free = free

    @property
    def free(self) -> list[int]:
        """ Список индексов свободных переменных """
        if self._free is not None:
            return self._free
        canonical = self.lp_problem.canonical_form
        vars_indices = [i for i in range(canonical.var_count)]
        free = list(filter(lambda index: index not in self.basis, vars_indices))
        self._free = free
        return free

    @property
    def free_variables(self) -> list[Symbol]:
        """ Список символов (:class:`sympy.Symbol`) свободных переменных """
        return list(symbols(" ".join([f"{self.lp_problem.objective.variable_symbol}{i + 1}" for i in self.free])))

    @property
    def basis_variables(self) -> list[Symbol]:
        """ Список символов (:class:`sympy.Symbol`) базисных переменных """
        return list(symbols(" ".join([f"{self.lp_problem.objective.variable_symbol}{i + 1}" for i in self.basis])))

    @property
    def objective_coeffs(self) -> list[Rational]:
        """ Коэффициенты целевой функции, выраженной через свободные переменные """
        from sympy import collect, expand
        expr = self._express_objective_through_free
        expanded_expr = collect(expand(expr), self.free_variables)
        coeffs = [expanded_expr.coeff(x) for x in self.free_variables]
        return coeffs

    @property
    def objective_value(self) -> Rational:
        """ Значение целевой функции при обнулении всех свободных переменных """
        e = self._express_objective_through_free
        const = e
        for x in self.free_variables:
            const = const.subs(x, 0)
        return const

    @property
    def basis_coeffs(self) -> list[list[Rational]]:
        """ Коэффициенты в выражении базисных переменных через свободные переменные """
        result = []
        for e in self._express_basis_through_free:
            coeffs = [e.coeff(x) for x in self.free_variables]
            result.append(coeffs)
        return result

    @property
    def basis_values(self) -> list[Rational]:
        """ Значения базисных переменных при обнулении всех свободных переменных """
        result = []
        for e in self._express_basis_through_free:
            const = e
            for x in self.free_variables:
                const = const.subs(x, 0)
            result.append(const)
        return result

    @cached_property
    def solution(self):
        result = []
        var_count = self.lp_problem.canonical_form.var_count
        basis = self.basis
        basis_values = self.basis_values
        for i in range(var_count):
            if i in basis:
                in_basis_index = basis.index(i)
                value = basis_values[in_basis_index]
                result.append(value)
            else:
                result.append(Rational(0))
        return result

    @property
    def is_acceptable(self):
        """ Является ли решение допустимым (значения базисных переменных должны быть неотрицательными) """
        result = True
        for v in self.basis_values:
            if v < 0:
                result = False
                break
        return result

    @property
    def unacceptable_variables(self):
        """ Возвращает индексы базисных переменных, значения которых являются недопустимыми (отрицательными) """
        result = []
        for i, v in enumerate(self.basis_values):
            if v < 0:
                result.append(self.basis[i])
        return result

    @property
    def is_opt(self):
        """ Является ли решение оптимальным (коэффициенты целевой функции при свободных переменных неположительные) """
        obj_coeffs = self.objective_coeffs
        # if not self.is_acceptable:
        #     return False
        result = True
        for c in obj_coeffs:
            c = c.subs({self.lp_problem.M: Rational(1000)})
            if c > 0:
                result = False
                break
        return result

    @property
    def _express_basis_through_free(self) -> list[Expr]:
        """ Базисные переменные выраженные через свободные. Порядок соответствует порядку базисных переменных """
        basis_variables = self.basis_variables
        equations = self.lp_problem.canonical_form.constraints_expressions
        solution_dict = solve(equations, basis_variables)
        result = []
        for b in basis_variables:
            result.append(solution_dict[b])
        return result

    @property
    def _express_objective_through_free(self) -> Expr:
        """ Целевая функция, выраженная через свободные переменные """
        obj = self.lp_problem.objective
        expr = obj.as_expr
        basis_expressions = self._express_basis_through_free
        objective_vars = expr.free_symbols
        reps = []
        for i, x in enumerate(self.basis_variables):
            if x not in objective_vars:
                continue
            reps.append((x, basis_expressions[i]))
        result = expr.subs(reps)
        return result

    def is_neighbor(self, basis_sol: BasisSolution) -> bool:
        """
        Проверяет, являются ли базисы соседними, т.е. имеют ли общее ограничение
        :param basis_sol: Другой базис
        :return: True - базисы соседние, иначе False
        """
        basis_1 = self.basis
        basis_2 = basis_sol.basis

        if len(basis_1) != len(basis_2):
            return False
        basis_2 = set(basis_2)
        diff_count = 0
        for b1 in basis_1:
            if b1 in basis_2:
                diff_count += 1
            if diff_count > 1:
                return False
        return diff_count == 1

    def distance(self, sol: BasisSolution):
        x1, y1 = self.solution[:2]
        x2, y2 = sol.solution[:2]
        dx = x2 - x1
        dy = y2 - y1
        return sqrt(dx ** 2 + dy ** 2)

    @cached_property
    def active_constraints(self) -> list[Constraint]:
        """
        Активные ограничения в данном базисном решении
        :return: Список активных ограничений
        """
        result = []

        sol = self.solution
        # Проверяем пересечение с ограничениями на неотрицательность переменных
        if sol[0] == 0:
            result.append(self.lp_problem.var_value_constraints[0])
        if sol[1] == 0:
            result.append(self.lp_problem.var_value_constraints[1])

        # Проверяем остальные ограничения
        tol = 0.01
        A, b, _ = self.lp_problem.matrices
        constraint_values = A @ Matrix(sol[:2])
        active_constraints_indices = np.where(np.abs(constraint_values - b) <= tol)[0]
        active_constraints = [self.lp_problem.constraints[i] for i in active_constraints_indices]
        result.extend(active_constraints)
        return result

    def __str__(self):
        return ', '.join([f'{pretty(x)} = {v}' for x, v in zip(self.basis_variables, self.basis_values)])


