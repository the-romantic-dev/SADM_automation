from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from sympy import symbols

from report.model.report_prettifier import expr_str
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective
from tasks.task1_2_lp.view.plot.dataclasses.plot_data import PlotData


@dataclass
class LinearFunction:
    """ Функция вида Ax + By = C """
    x_coeff: float
    y_coeff: float
    const: float

    @staticmethod
    def from_constraint(constraint: Constraint) -> LinearFunction:
        coeffs = constraint.coeffs
        if len(coeffs) != 2:
            raise ValueError('Incorrect constraint size')
        return LinearFunction(
            x_coeff=float(coeffs[0]),
            y_coeff=float(coeffs[1]),
            const=float(constraint.const)
        )

    @staticmethod
    def from_objective(objective: Objective, opt_sol: BasisSolution) -> LinearFunction:
        coeffs = objective.coeffs
        if len(coeffs) != 2:
            raise ValueError('Incorrect objective size')
        return LinearFunction(
            x_coeff=float(coeffs[0]),
            y_coeff=float(coeffs[1]),
            const=float(opt_sol.objective_value)
        )

    def y(self, x: float | np.ndarray) -> float | None:
        if self.y_coeff == 0:
            return None
        return (self.const - self.x_coeff * x) / self.y_coeff

    def x(self, y: float | np.ndarray) -> float | None:
        if self.x_coeff == 0:
            return None
        return (self.const - self.y_coeff * y) / self.x_coeff

    def plot_values(self, plot_data: PlotData, resolution: int):
        # x = self.x_plot_values(plot_data, resolution)
        # y = self.y_plot_values(plot_data, resolution)
        left_y = self.y(plot_data.axes_bounds.left_x)
        right_y = self.y(plot_data.axes_bounds.right_x)
        if left_y is None or right_y is None:
            y0 = plot_data.axes_bounds.bottom_y
            y1 = plot_data.axes_bounds.top_y
            x0 = self.x(y0)
            x1 = self.x(y1)
        else:
            y0 = left_y
            y1 = right_y
            x0 = plot_data.axes_bounds.left_x
            x1 = plot_data.axes_bounds.right_x
        if x1 == x0:
            x = np.array([x0 for _ in range(resolution)])
            y = np.linspace(y0, y1, resolution)
        elif y1 == y0:
            x = np.linspace(x0, x1, resolution)
            y = np.array([y0 for _ in range(resolution)])
        else:
            x = np.linspace(x0, x1, resolution)
            y = self.y(x)
        return x, y

    def angle(self, aspect: float) -> float:
        """ Угол графика в градусах. Зависит от размерности aspect всего plot-a"""
        k = -self.x_coeff / self.y_coeff
        rad = math.atan(k * aspect)
        result = math.degrees(rad)
        if result < 0:
            result += 360
        return result

    def __str__(self):
        expr = expr_str(coeffs=[self.x_coeff, self.y_coeff], variables=list(symbols('x1 x2')))
        return f"{expr} = {self.const}"