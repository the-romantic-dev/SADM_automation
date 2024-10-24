from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sympy import lambdify, symbols, Rational

from tasks.task1_3_nlp_unlimited.model import NLPObjective
import matplotlib.pyplot as plt

from tasks.task1_3_nlp_unlimited.model.dataclasses.solution_step import SolutionStep

x1, x2 = symbols('x1 x2')


@dataclass
class Bounds:
    min_x1: float
    min_x2: float
    max_x1: float
    max_x2: float


def solution_bounds(solution: list[SolutionStep], padding_percent: float):
    min_x1 = min(sol.x1 for sol in solution)
    min_x2 = min(sol.x2 for sol in solution)
    max_x1 = max(sol.x1 for sol in solution)
    max_x2 = max(sol.x2 for sol in solution)

    width = float(max_x1 - min_x1)
    height = float(max_x2 - min_x2)

    return Bounds(
        float(min_x1) - width * padding_percent,
        float(min_x2) - height * padding_percent,
        float(max_x1) + width * padding_percent,
        float(max_x2) + height * padding_percent
    )


class NLPMethodPlotter:
    def __init__(self, objective: NLPObjective, solution: list[SolutionStep]):
        self.objective = objective
        self.solution = solution

    def plot_level_lines(self):
        expr = self.objective.expr
        bounds = solution_bounds(self.solution, padding_percent=0.05)
        x1_vals = np.linspace(bounds.min_x1, bounds.max_x1, 1000)
        x2_vals = np.linspace(bounds.min_x2, bounds.max_x2, 1000)

        X1, X2 = np.meshgrid(x1_vals, x2_vals)
        Z = lambdify((x1, x2), expr, 'numpy')
        Z_values = Z(X1, X2)

        min_levels_num = 20
        base_levels = np.linspace(Z_values.min(), Z_values.max(), min_levels_num)
        levels = np.sort(
            np.hstack(
                [base_levels, np.array([sol.value for sol in self.solution])]
            )
        )
        contours = plt.contour(X1, X2, Z_values, levels=levels)  # levels - количество линий равного уровня

        # Добавляем подписи к осям и заголовок
        plt.xlabel('x1')
        plt.ylabel('x2')

        # Добавляем цветовую шкалу
        plt.colorbar(contours)

    def plot_solution_steps(self):
        plt.scatter(
            [float(sol.x1) for sol in self.solution],
            [float(sol.x2) for sol in self.solution],
            c='red',
            linewidths=0,
            zorder=3
        )
        for i in range(len(self.solution) - 1):
            plt.plot(
                [float(self.solution[i].x1), float(self.solution[i + 1].x1)],
                [float(self.solution[i].x2), float(self.solution[i + 1].x2)],
                marker=' ',
                linestyle='-',
                color='red',
                label='Линии между точками')

    def save_png(self, path: Path):
        self.plot_level_lines()
        self.plot_solution_steps()
        plt.savefig(path)
        plt.clf()
