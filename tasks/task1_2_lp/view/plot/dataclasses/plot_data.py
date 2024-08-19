from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from tasks.task1_2_lp.view.plot.dataclasses.axes_bounds import AxesBounds


@dataclass
class PlotData:
    figure: Figure
    axes: Axes
    axes_bounds: AxesBounds
    aspect: float
