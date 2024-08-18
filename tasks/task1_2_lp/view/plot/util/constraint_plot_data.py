from functools import cached_property

import numpy as np
from shapely import Point
from sympy import Expr

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.view.plot.plot import AxBounds
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.view.plot.util.plot_data import LinearPlotData


class ConstraintPlotData(LinearPlotData):
    def __init__(self, constraint: Constraint, resolution: int, ax_bounds: AxBounds):
        super().__init__(coeffs=constraint.coeffs, const=constraint.const, ax_bounds=ax_bounds, resolution=resolution,
                         expr=constraint.as_expr.lhs, variables=constraint.variables,
                         color='#2d70b3')
        self.constraint = constraint
