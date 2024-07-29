from dataclasses import dataclass

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
from tasks.task2_1_st.solvers.scheduling_problem.scheduling_problem_solver import SchedulingProblemSolver

@dataclass
class ChartTaskData:
    ij: tuple[int, int]
    start: int
    end: int

def x_tick_labels(arrange, step: int):
    result = []
    a_list = list(arrange)
    for i in range(len(a_list)):
        if i % step == 0:
            result.append(str(a_list[i]))
        else:
            result.append("")
    return result

class GanttChartCreator:
    def __init__(self, scheduling_problem_solver: SchedulingProblemSolver):
        self.scheduling_problem_solver = scheduling_problem_solver
        self.chart_data_per_rule = [self._get_chart_data(i) for i in range(len(scheduling_problem_solver.rules))]

    def _get_chart_data(self, rule_index) -> dict[int, list[ChartTaskData]]:
        table_data = self.scheduling_problem_solver.solution_steps_per_rule[rule_index]
        performers_num = self.scheduling_problem_solver.scheduling_data.performers_number
        data_per_performer = {i + 1: [] for i in range(performers_num)}
        for step in table_data:
            for p in data_per_performer:
                if step.B[p] is not None:
                    data_per_performer[p].append(
                        ChartTaskData(
                            ij=step.B[p],
                            start=step.T,
                            end=step.L[p]
                        )
                    )
        return data_per_performer

    def make_diagram(self, is_compact: bool, rule_index: int):
        chart_data_dict = self.chart_data_per_rule[rule_index]
        fig, ax = plt.subplots(figsize=(17, 6))
        performers = chart_data_dict.keys()
        p_num = len(performers)
        max_tasks_len = max([len(chart_data_dict[i]) for i in chart_data_dict])
        if is_compact:
            performers_labels = [f"Ресурс {p}" for p in performers]
        else:
            performers_labels = []
        for i in range(max_tasks_len):
            for p in performers:
                if not is_compact:
                    performers_labels.append(f"Ресурс {p}")
                if i >= len(chart_data_dict[p]):
                    continue
                data = chart_data_dict[p][i]
                task_name = f"{data.ij[0]}{data.ij[1]}"
                if is_compact:
                    y = p - 1
                else:
                    y = i * p_num + p - 1
                ax.barh(y, data.end - data.start, left=data.start, height=1, align='center', label=task_name, zorder=2)
                ax.text(
                    (data.start + data.end) / 2,
                    y,
                    task_name,
                    ha='center',
                    va='center',
                    color='white',
                    fontsize=14,
                    zorder=3,
                    path_effects=[pe.withStroke(linewidth=2, foreground='black')]
                )

        ax.invert_yaxis()  # Перевернем ось Y
        ax.xaxis.tick_top()  # Разместим метки делений оси X наверху
        ax.xaxis.set_label_position('top')  # Переместим подпись оси X наверх
        ax.set_yticks(range(len(performers_labels)))
        ax.set_yticklabels(performers_labels)
        ax.set_xlabel('Системное время')

        total_time = self.scheduling_problem_solver.total_times[rule_index]
        x_ticks = np.arange(0, total_time + 1, step=1)
        ax.set_xticks(x_ticks)
        ticks_labels = x_tick_labels(x_ticks, step=5)
        ax.set_xticklabels(ticks_labels)

        ax.set_ylabel('Ресурсы')
        # ax.set_title('Диаграмма Гантта')

        # Уменьшим шрифт подписей оси X
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.grid(True, which='both', linestyle='-', linewidth=0.5, zorder=1)
        # plt.show()
        return plt