from functools import cached_property

from matplotlib.axes import Axes
from sympy import Rational

from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator
from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds
from tasks.task1_2_lp.view.plot.util.constraint_plot_data import ConstraintPlotData


def _plot_data(constraints: list[Constraint], ax_bounds: AxBounds, resolution: int):
    result = []
    for constraint in constraints:
        cpd = ConstraintPlotData(constraint, resolution=resolution, ax_bounds=ax_bounds)
        result.append(cpd)
    return result


class ConstraintsPlotter:
    def __init__(self, constraints: list[Constraint]):
        variable_symbol = constraints[0].variable_symbol
        self.constraints = constraints
        # + [
        #     Constraint([Rational(1), Rational(0)], Rational(0), CompOperator.GE, variable_symbol=variable_symbol),
        #     Constraint([Rational(0), Rational(1)], Rational(0), CompOperator.GE, variable_symbol=variable_symbol)
        # ]

    def plot(self, ax: Axes, ax_bounds: AxBounds, resolution: int):
        plot_data = _plot_data(constraints=self.constraints, ax_bounds=ax_bounds, resolution=resolution)
        for pd in plot_data:
            ax.plot(pd.x, pd.y, color=pd.color, linewidth=2)
