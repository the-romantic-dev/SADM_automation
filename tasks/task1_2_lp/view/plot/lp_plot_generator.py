from functools import cached_property

import numpy as np
from adjustText import adjust_text
from scipy.spatial import ConvexHull
from sympy import Expr, Rational, pretty

from tasks.task1_2_lp.view.plot.plot import Plot, AxBounds, Position
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.view.plot.constraint_plot_data import ConstraintPlotData


# def is_sol_on_constraint(sol: BasisSolution, constraint: Constraint):
#     tol = 1e-3
#     solution = sol.solution
#     variables = constraint.variables
#     expr: Expr = constraint.as_expr.lhs
#     result_value = float(expr.subs({variables[i]: solution[i] for i in range(len(variables))}))
#     expected_value = float(constraint.const)
#     diff = expected_value - result_value
#     return abs(diff) < tol


# def widest_section_sols(sol_to_constraints: dict[BasisSolution, list[Constraint]], constraint: Constraint):
#     sols_on_constraint = [sol for sol in sol_to_constraints if constraint in sol_to_constraints[sol]]
#     ordered_sols = sorted(sols_on_constraint, key=lambda sol: sol.solution[0])
#
#     def distance(sol1: BasisSolution, sol2: BasisSolution):
#         x1, y1 = sol1.solution[:2]
#         x2, y2 = sol2.solution[:2]
#         dx = float(x2 - x1)
#         dy = float(y2 - y1)
#         return np.sqrt(dx ** 2 + dy ** 2)
#
#     max_distance = -1
#     max_distance_edge_sols = None
#     for i in range(1, len(ordered_sols)):
#         dist = distance(ordered_sols[i - 1], ordered_sols[i])
#         if dist > max_distance:
#             max_distance = dist
#             max_distance_edge_sols = [ordered_sols[i - 1], ordered_sols[i]]
#
#     return max_distance_edge_sols


# def widest_section_indices(x: np.ndarray, sol_to_constraints: dict[BasisSolution, list[Constraint]],
#                            constraint: Constraint):
#     section_sols = widest_section_sols(sol_to_constraints, constraint)
#
#     def find_nearest_sol_index(sol: BasisSolution):
#         value = sol.solution[0]
#         idx = (np.abs(x - value)).argmin()
#         return idx
#
#     result = [find_nearest_sol_index(section_sols[0]), find_nearest_sol_index(section_sols[1])]
#     return result


class LPPlotGenerator:
    def __init__(self, lpp: LPProblem, all_solutions: list[BasisSolution]):
        if lpp.var_count != 2:
            raise ValueError("Нельзя отобразить на графике ЗЛП где количество переменных не равно 2")
        self.ax_bounds = AxBounds.get_from_solutions(all_solutions, padding=5.0)
        self.plot = Plot(ax_bounds=self.ax_bounds, square_grid=False)
        self.resolution = 1000
        self.lpp = lpp
        self.all_solutions = all_solutions
        self.annotations = []

    # @cached_property
    # def sol_to_constraints(self):
    #     result = dict()
    #
    #     zero_constraints = [
    #         Constraint(coeffs=[Rational(1), Rational(0)], const=Rational(0), comp_operator=CompOperator.GE),
    #         Constraint(coeffs=[Rational(0), Rational(1)], const=Rational(0), comp_operator=CompOperator.GE)
    #     ]
    #
    #     constraints = self.lpp.constraints + zero_constraints
    #     for sol in self.all_solutions:
    #         for constraint in constraints:
    #             if is_sol_on_constraint(sol, constraint):
    #                 if sol in result:
    #                     result[sol].append(constraint)
    #                 else:
    #                     result[sol] = [constraint]
    #     return result

    # def add_constraint(self, constraint: Constraint):
    #     # plot_data = ConstraintPlotData(constraint, self.resolution, self.ax_bounds)
    #     # x = plot_data.x
    #     # y = plot_data.y
    #     # plot_color = '#2d70b3'
    #     # self.plot.add_plot(x=x, y=y, color=plot_color)
    #     # Находим середину линии
    #     # sol_to_constraints = self.sol_to_constraints
    #     # section = widest_section_indices(x=x, sol_to_constraints=sol_to_constraints, constraint=constraint)
    #     # mid_point = (section[0] + section[1]) // 2
    #     # mid_x = float(x[mid_point])
    #     # mid_y = float(y[mid_point])
    #     #
    #     # annotation = self.plot.add_annotation(
    #     #     text=constraint.pretty_str(),
    #     #     position=Position(x=mid_x, y=mid_y),
    #     #     angle=plot_data.angle(self.plot.aspect)
    #     # )
    #     # self.annotations.append(annotation)

    # def add_fill(self):
    #     acceptable_sols = filter(lambda sol: sol.is_acceptable, self.all_solutions)
    #     positions = np.asarray([(float(sol.solution[0]), float(sol.solution[1])) for sol in acceptable_sols])
    #     hull = ConvexHull(positions)
    #     hull_points = positions[hull.vertices]
    #     self.plot.add_fill(x=hull_points[:, 0], y=hull_points[:, 1], color='r', alpha=0.5)

    def show(self):
        positions = np.asarray([(float(sol.solution[0]), float(sol.solution[1])) for sol in self.all_solutions])
        self.plot.ax.scatter(x=positions[:, 0], y=positions[:, 1], s=100, c='r', zorder=3)
        pos_x = positions[:, 0]
        pos_y = positions[:, 1]
        for i in range(len(positions)):
            sol = self.all_solutions[i]
            b1 = pretty(sol.basis_variables[0])
            b2 = pretty(sol.basis_variables[1])
            b1_value = sol.solution[sol.basis[0]]
            b2_value = sol.solution[sol.basis[1]]
            label = f"Базис: \n{b1} = {b1_value}\n{b2} = {b2_value}"
            annotation = self.plot.add_annotation(label, Position(x=pos_x[i], y=pos_y[i]), angle=0)
            self.annotations.append(annotation)

        self.add_fill()
        for c in self.lpp.constraints:
            self.add_constraint(c)
        adjust_text(texts=self.annotations, expand=(1.2, 2))
        self.plot.show()
