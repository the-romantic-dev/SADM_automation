from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from tasks.task1_2_lp.view.plot.dataclasses.axes_bounds import AxesBounds
from tasks.task1_2_lp.view.plot.dataclasses.plot_data import PlotData


def get_plot_data(figure_size: tuple[int, int], ax_bounds: AxesBounds):
    figure, axes = plt.subplots(figsize=figure_size)
    _set_desmos_style(axes)
    _set_ax_limits(axes, ax_bounds)
    return PlotData(figure, axes, ax_bounds, _calc_aspect(figure, axes))


def _calc_aspect(figure: Figure, axes: Axes) -> float:
    x_range = axes.get_xlim()[1] - axes.get_xlim()[0]
    y_range = axes.get_ylim()[1] - axes.get_ylim()[0]
    return figure.get_size_inches()[1] / figure.get_size_inches()[0] * x_range / y_range


def _set_desmos_style(ax: Axes):
    """Устанавливает стиль графика, похожий на Desmos."""
    ax.set_facecolor('#f8f9fa')
    ax.spines['top'].set_color('#dadada')
    ax.spines['bottom'].set_color('#dadada')
    ax.spines['left'].set_color('#dadada')
    ax.spines['right'].set_color('#dadada')
    ax.grid(True, color='#dadada', linestyle=':')

    ax.tick_params(axis='both', which='both', color='#dadada')
    ax.axhline(y=0, color='#404040', linestyle='-', linewidth=1.2)
    ax.axvline(x=0, color='#404040', linestyle='-', linewidth=1.2)
    ax.set_xlabel('x₁', fontsize=12)
    ax.set_ylabel('x₂', fontsize=12)


def _set_ax_limits(ax: Axes, bounds: AxesBounds):
    ax.set_xlim(bounds.left_x, bounds.right_x)
    ax.set_ylim(bounds.bottom_y, bounds.top_y)
