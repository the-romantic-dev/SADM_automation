from functools import cached_property

import numpy as np

from report.model.report_prettifier import expr_str
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds
from tasks.task1_2_lp.view.plot.util.plot_data import LinearPlotData


class ObjectivePlotData(LinearPlotData):
    @property
    def annotation_text(self):
        coeffs = self.objective.coeffs
        variables = self.objective.variables
        const = self.objective.const
        return f'max({expr_str(coeffs, variables, const)})'

    def __init__(self, objective: Objective, opt_sol: BasisSolution, ax_bounds: AxBounds, resolution: int):
        super().__init__(coeffs=objective.coeffs, const=float(opt_sol.objective_value), ax_bounds=ax_bounds,
                         resolution=resolution, color="#FA6501")
        self.objective = objective
