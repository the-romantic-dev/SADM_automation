from matplotlib.axes import Axes

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds
from tasks.task1_2_lp.view.plot.util.objective_plot_data import ObjectivePlotData
from tasks.task1_2_lp.view.plot.util.plot_data import LinearPlotData


class ObjectivePlotter:
    def __init__(self, objective: Objective, opt_sol: BasisSolution):
        self.opt_sol = opt_sol
        self.objective = objective

    def plot_data(self, ax_bounds: AxBounds, resolution: int) -> LinearPlotData:
        return ObjectivePlotData(self.objective, self.opt_sol, ax_bounds, resolution)

    def plot(self, ax: Axes, ax_bounds: AxBounds, resolution: int):
        pd = self.plot_data(ax_bounds, resolution)
        ax.plot(pd.x, pd.y, color=pd.color, linewidth=2, linestyle='--')
