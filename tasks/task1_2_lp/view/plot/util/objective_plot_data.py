from functools import cached_property

import numpy as np

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds
from tasks.task1_2_lp.view.plot.util.plot_data import LinearPlotData


class ObjectivePlotData(LinearPlotData):
    def __init__(self, objective: Objective, opt_sol: BasisSolution, ax_bounds: AxBounds, resolution: int):
        super().__init__(coeffs=objective.coeffs, const=float(opt_sol.objective_value), ax_bounds=ax_bounds,
                         resolution=resolution, expr=objective.as_expr,
                         variables=objective.variables, color="#FA6501")
        self.objective = objective
