from matplotlib.axes import Axes

from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds
from tasks.task1_2_lp.view.plot.util.constraint_plot_data import ConstraintPlotData
from tasks.task1_2_lp.view.plot.util.plot_data import LinearPlotData


class ConstraintsPlotter:
    def __init__(self, constraints: list[Constraint]):
        self.constraints = constraints

    def plot_data(self, ax_bounds: AxBounds, resolution: int) -> list[LinearPlotData]:
        result = []
        for constraint in self.constraints:
            cpd = ConstraintPlotData(constraint, resolution=resolution, ax_bounds=ax_bounds)
            result.append(cpd)
        return result

    def plot(self, ax: Axes, ax_bounds: AxBounds, resolution: int):
        plot_data = self.plot_data(ax_bounds=ax_bounds, resolution=resolution)
        for pd in plot_data:
            ax.plot(pd.x, pd.y, color=pd.color, linewidth=2)
