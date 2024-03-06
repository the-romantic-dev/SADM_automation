from dataclasses import dataclass

from tasks.scheduling_theory.scheduling_data import SchedulingData
from tasks.scheduling_theory.solvers.moments.reserves_calculator import ReservesCalculator
from tasks.scheduling_theory.solvers.scheduling_problem.rule import RuleType, Rule


@dataclass
class SchedulingStep:
    # Общее время
    T: int

    # Список уже выполненных работ
    D: list[tuple[int, int]]

    # Список пройденных узлов
    E: set[int]

    # Список еще выполняемых работ
    N: dict[int, tuple[int, int]]

    # Список доступных на выполнение работ
    W: list[tuple[int, int]]

    # Список длительностей доступных работ
    A: list[int]

    # Список резервов доступных работ
    R: list[int]

    # Список уровней доступных работ
    V: list[int]

    # Список начатых на этом шаге работ
    B: dict[int, tuple[int, int]]

    # Список времен освобождения ресурсов
    L: dict[int, int]


def get_free_performers_num(current_tasks):
    counter = 0
    for i in current_tasks:
        if current_tasks[i] is None:
            counter += 1
    return counter


def get_new_tasks(started_tasks_indices: list, current_tasks: dict, available_tasks: list):
    result = current_tasks.copy()
    indices = started_tasks_indices.copy()
    for i in result:
        if result[i] is None and len(indices) > 0:
            index = indices.pop()
            result[i] = available_tasks[index]
        else:
            result[i] = None
    return result


def merge_new_and_current_tasks(new_tasks: dict, current_tasks: dict):
    result = new_tasks.copy()
    for i in result:
        if result[i] is None:
            result[i] = current_tasks[i]
    return result


def get_earliest_finished_performers(performers_finish_times: dict):
    earliest = None
    for i in performers_finish_times:
        if performers_finish_times[i] is None:
            continue
        if earliest is None or performers_finish_times[i] < performers_finish_times[earliest]:
            earliest = i
    result = [earliest]
    for i in performers_finish_times:
        if i != earliest and performers_finish_times[i] == performers_finish_times[earliest]:
            result.append(i)
    return result


def handle_downtime(
        downtime_intervals: dict[int, list[tuple]],
        current_tasks: dict,
        new_tasks: dict,
        current_time: int,
        is_last_step: bool = False):
    if is_last_step:
        for p in downtime_intervals:
            if len(downtime_intervals[p]) > 0 and downtime_intervals[p][-1][1] is None:
                downtime_intervals[p][-1] = (downtime_intervals[p][-1][0], current_time)
        return
    for p in downtime_intervals:
        is_downtime = current_tasks[p] is None and new_tasks[p] is None
        if len(downtime_intervals[p]) > 0:
            last_interval = downtime_intervals[p][-1]
            does_downtime_begin = is_downtime and last_interval[1] is not None
            does_downtime_finish = new_tasks[p] is not None and last_interval[1] is None
        else:
            does_downtime_begin = is_downtime
            does_downtime_finish = False

        if does_downtime_begin:
            downtime_intervals[p].append((current_time, None))
        if does_downtime_finish:
            downtime_intervals[p][-1] = (downtime_intervals[p][-1][0], current_time)


class SchedulingProblemSolver:
    def __init__(self, scheduling_data: SchedulingData, reserves_calculator: ReservesCalculator):
        self.scheduling_data = scheduling_data
        self.reserves_calculator = reserves_calculator
        self.rules = [Rule(rule_type=rt) for rt in scheduling_data.rule_types]
        # self.total_time = -1
        self.downtime_intervals = []
        self.total_times = []
        self.solution_steps_per_rule = [self.get_solution_steps(rule) for rule in self.rules]


    def _get_available_tasks(self, passed_nodes, executed_tasks, current_tasks):
        available_tasks = []
        for node in passed_nodes:
            outcoming_nodes = self.scheduling_data.get_outcoming_nodes(node)
            for o_node in outcoming_nodes:
                available_tasks.append((node, o_node))
        for task in executed_tasks:
            if task in available_tasks:
                available_tasks.remove(task)
        for task in current_tasks.values():
            if task in available_tasks:
                available_tasks.remove(task)
        return available_tasks

    def performers_finish_times(self, new_tasks: dict, current_tasks: dict, previous_finish_times: dict,
                                current_time: int):
        result = new_tasks.copy()
        for i in result:
            if result[i] is None:
                if current_tasks[i] is not None:
                    result[i] = previous_finish_times[i]
                else:
                    result[i] = None
            else:
                result[i] = current_time + self.scheduling_data.get_edge_weight(result[i])
        return result

    def get_solution_steps(self, rule: Rule) -> list[SchedulingStep]:
        tasks_for_execution = self.scheduling_data.get_edges()
        result = []
        performers_list = [i for i in range(self.scheduling_data.performers_number)]
        current_tasks = {i + 1: None for i in performers_list}
        executed_tasks = []
        downtimes_intervals = {i + 1: [] for i in performers_list}
        current_time = 0
        passed_nodes = {1}
        performers_finish_times = {i + 1: None for i in performers_list}
        while len(tasks_for_execution) != len(executed_tasks):
            available_tasks = self._get_available_tasks(passed_nodes, executed_tasks, current_tasks)
            available_tasks_durations = [self.scheduling_data.get_edge_weight(task) for task in available_tasks]
            available_tasks_reserves = [int(self.reserves_calculator.calc_full_reserve(i, j)) for i, j in
                                        available_tasks]
            available_tasks_levels = [self.scheduling_data.get_node_level(task[0]) for task in available_tasks]
            started_tasks_indices = rule.optimal_tasks_indices(
                tasks_count=get_free_performers_num(current_tasks),
                durations=available_tasks_durations,
                reserves=available_tasks_reserves,
                levels=available_tasks_levels
            )
            new_tasks = get_new_tasks(started_tasks_indices, current_tasks, available_tasks)

            handle_downtime(downtimes_intervals, current_tasks, new_tasks, current_time)
            performers_finish_times = self.performers_finish_times(new_tasks, current_tasks, performers_finish_times,
                                                                   current_time)
            step = SchedulingStep(
                T=current_time,
                D=executed_tasks.copy(),
                E=passed_nodes.copy(),
                N=current_tasks.copy(),
                W=available_tasks,
                A=available_tasks_durations,
                R=available_tasks_reserves,
                V=available_tasks_levels,
                B=new_tasks,
                L=performers_finish_times
            )
            all_executing_tasks = merge_new_and_current_tasks(new_tasks, current_tasks)
            earliest_finished_performers = get_earliest_finished_performers(performers_finish_times)

            finished_tasks = [all_executing_tasks[p] for p in earliest_finished_performers]
            # if finished_task is None:
            #     result.append(step)
            #     break
            executed_tasks.extend(finished_tasks)
            passed_nodes.update([task[1] for task in finished_tasks])
            for p in earliest_finished_performers:
                all_executing_tasks[p] = None

            current_time = performers_finish_times[earliest_finished_performers[0]]
            current_tasks = all_executing_tasks
            result.append(step)
        step = SchedulingStep(
            T=current_time,
            D=executed_tasks.copy(),
            E=passed_nodes.copy(),
            N=current_tasks.copy(),
            W=[],
            A=[],
            R=[],
            V=[],
            B={i + 1: None for i in performers_list},
            L={i + 1: None for i in performers_list}
        )
        handle_downtime(downtimes_intervals, current_tasks, {i + 1: None for i in performers_list}, current_time, is_last_step=True)
        self.downtime_intervals.append(downtimes_intervals)
        self.total_times.append(current_time)
        result.append(step)
        return result
