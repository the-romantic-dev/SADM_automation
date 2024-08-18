from functools import cached_property

import numpy as np
from shapely import Point
from sympy import Expr

from report.model.report_prettifier import expr_str, rational_str
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.view.plot.plotter import AxBounds
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.view.plot.util.plot_data import LinearPlotData


class ConstraintPlotData(LinearPlotData):
    @property
    def annotation_text(self):
        coeffs = self.constraint.coeffs
        variables = self.constraint.variables
        const = self.constraint.const
        return f'{expr_str(coeffs, variables)} ≤ {rational_str(const)}'

    def __init__(self, constraint: Constraint, resolution: int, ax_bounds: AxBounds):
        super().__init__(coeffs=constraint.coeffs, const=constraint.const, ax_bounds=ax_bounds, resolution=resolution,
                         color='#2d70b3')
        self.constraint = constraint
