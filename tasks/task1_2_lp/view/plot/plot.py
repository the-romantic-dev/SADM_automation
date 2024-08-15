import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from tasks.task1_2_lp.view.plot.dataclasses.ax_bounds import AxBounds
from tasks.task1_2_lp.view.plot.dataclasses.position import Position


def set_desmos_style(ax: Axes):
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


def set_ax_limits(ax: Axes, box: AxBounds, square_grid: bool, figure_size: tuple[int, int]):
    if square_grid:
        aspect = figure_size[0] / figure_size[1]
        x_side = abs(box.right_x - box.left_x)
        y_side = abs(box.top_y - box.bottom_y)
        x_center = box.left_x + x_side / 2
        y_center = box.bottom_y + y_side / 2
        min_side = min(x_side, y_side)
        if x_side == min_side:
            x_side = y_side * aspect

        else:
            y_side = x_side / aspect
        new_box = AxBounds(left_x=x_center - x_side / 2, right_x=x_center + x_side / 2,
                           bottom_y=y_center - y_side / 2, top_y=y_center + y_side / 2)
        ax.set_xlim(new_box.left_x, new_box.right_x)
        ax.set_ylim(new_box.bottom_y, new_box.top_y)
    else:
        ax.set_xlim(box.left_x, box.right_x)
        ax.set_ylim(box.bottom_y, box.top_y)


class Plot:
    def __init__(self,
                 ax_bounds: AxBounds,
                 figure_size: tuple[int, int] = (16, 10),
                 square_grid: bool = False):
        fig, ax = plt.subplots(figsize=figure_size)
        self.fig: Figure = fig
        self.ax: Axes = ax
        set_desmos_style(self.ax)
        set_ax_limits(self.ax, ax_bounds, square_grid, figure_size)

    @property
    def aspect(self) -> float:
        x_range = self.ax.get_xlim()[1] - self.ax.get_xlim()[0]
        y_range = self.ax.get_ylim()[1] - self.ax.get_ylim()[0]
        return self.fig.get_size_inches()[1] / self.fig.get_size_inches()[0] * x_range / y_range

    def add_plot(self,
                 x: np.ndarray, y: np.ndarray,
                 color: str = "#000000", width: int = 2
                 ) -> list[Line2D]:
        return self.ax.plot(x, y, color=color, linewidth=width)

    def add_annotation(self,
                       text: str,
                       position: Position,
                       text_offset: tuple[int, int] = (0, 10),
                       angle: float = 0,
                       fill_color: str = 'white',
                       border_color: str = 'gray',
                       alpha: float = 0.5,
                       font_size: int = 9,
                       arrow_properties: dict | None = None,
                       z_order: int = 4):
        if angle > 90:
            angle -= 180
        elif angle < -90:
            angle += 180

        return self.ax.annotate(
            text=text,
            xy=(position.x, position.y),
            xytext=text_offset,
            textcoords='offset points',
            ha='center', va='bottom',
            rotation=angle,
            rotation_mode='anchor',
            bbox=dict(boxstyle='round,pad=0.5', fc=fill_color, ec=border_color, alpha=alpha),
            fontsize=font_size,
            arrowprops=arrow_properties,
            zorder=z_order
        )

    def add_fill(self, x: np.ndarray, y: np.ndarray, color: str, alpha: float):
        return self.ax.fill(x, y, color, alpha=alpha)

    def add_points(self, positions: list[Position], size: float, color: str, z_order: int):
        x = [pos.x for pos in positions]
        y = [pos.y for pos in positions]
        return self.ax.scatter(x=x, y=y, s=size, c=color, zorder=z_order, linewidths=1.5, edgecolors="#000000")

    def show(self):
        self.add_all()
        self.fig.show()
        plt.show()

    def add_all(self):
        pass
