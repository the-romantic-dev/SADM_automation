import numpy as np
from matplotlib.axes import Axes
from shapely import Point

from tasks.task1_2_lp.view.plot.util.plot_data import LinearPlotData


def angle(pd: LinearPlotData, aspect: float) -> float:
    """ Угол графика в градусах. Зависит от размерности aspect всего plot-a"""
    dx = pd.x[-1] - pd.x[0]
    dy = pd.y[-1] - pd.y[0]
    result = np.degrees(np.arctan2(dy * aspect, dx))

    if result > 90:
        result -= 180
    elif result < -90:
        result += 180
    return result


class LinearAnnotationsPlotter:
    def __init__(self, linear_plot_data: list[LinearPlotData]):
        self.linear_plot_data = linear_plot_data

    def plot(self, ax: Axes, aspect: float, intersections: list[Point]):
        plot_data = self.linear_plot_data
        for pd in plot_data:
            belonging_solutions = pd.get_belonging_intersections(intersections)
            annotated_section = pd.get_widest_section_indices(belonging_solutions)
            mid_point = (annotated_section[0] + annotated_section[1]) // 2
            mid_x = float(pd.x[mid_point])
            mid_y = float(pd.y[mid_point])
            ax.annotate(
                text=pd.annotation_text,
                xy=(mid_x, mid_y),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center', va='bottom',
                rotation=angle(pd, aspect),
                rotation_mode='anchor',
                bbox=dict(boxstyle='round,pad=0.5', fc=pd.color, ec='gray', alpha=0.5),
                fontsize=9
            )
            # self.add_annotation(
            #     text=pd.constraint.pretty_str(),
            #     point=Point(mid_x, mid_y),
            #     ha="center", va="bottom",
            #     text_offset=(0, 10),
            #     angle=angle(aspect),
            #     fill_color=pd.color,
            #     alpha=0.3
            # )
