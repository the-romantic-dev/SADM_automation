from enum import Enum


class RuleType(Enum):
    MIN_DURATION = 1
    MAX_DURATION = 2
    MIN_RESERVE = 3
    MIN_LEVELS_MIN_DURATION = 4
    MIN_LEVELS_MAX_DURATION = 5


def _optimal_without_levels(tasks_count: int, properties: list, is_min: bool):
    data_list = [(i, properties[i]) for i in range(len(properties))]
    sorted_data = sorted(data_list, key=lambda x: x[1])

    if is_min:
        optimal_properties = sorted_data[:tasks_count]
    else:
        optimal_properties = sorted_data[-tasks_count:]
    optimal_indices = [x[0] for x in optimal_properties]
    return optimal_indices


def _optimal_min_levels(tasks_count: int, levels: list, properties: list, is_properties_min: bool):
    data_list = [(i, levels[i], properties[i]) for i in range(len(levels))]
    sorted_by_levels_data = sorted(data_list, key=lambda x: x[1])
    equality_level_list = []
    equality_level_sublist = []
    for level in sorted_by_levels_data:
        if len(equality_level_sublist) == 0:
            equality_level_sublist.append(level)
        else:
            if level[1] == equality_level_sublist[-1][1]:
                equality_level_sublist.append(level)
            else:
                equality_level_list.append(equality_level_sublist)
                equality_level_sublist = [level]
    equality_level_list.append(equality_level_sublist)
    result_data = []
    for sublist in equality_level_list:
        free_space = tasks_count - len(result_data)
        if free_space == 0:
            break
        if len(sublist) <= free_space:
            result_data.extend(sublist)
        else:
            sorted_by_properties_sublist = sorted(sublist, key=lambda x: x[2])
            if is_properties_min:
                extend_data = sorted_by_properties_sublist[:free_space]
            else:
                extend_data = sorted_by_properties_sublist[-free_space:]
            result_data.extend(extend_data)
            break
    return [x[0] for x in result_data]


class Rule:
    def __init__(self, rule_type: RuleType):
        self.rule_type: RuleType = rule_type

    def optimal_tasks_indices(self, tasks_count, durations, reserves, levels):
        match self.rule_type:
            case RuleType.MIN_DURATION:
                return _optimal_without_levels(tasks_count, durations, is_min=True)
            case RuleType.MAX_DURATION:
                return _optimal_without_levels(tasks_count, durations, is_min=False)
            case RuleType.MIN_RESERVE:
                return _optimal_without_levels(tasks_count, reserves, is_min=True)
            case RuleType.MIN_LEVELS_MIN_DURATION:
                return _optimal_min_levels(tasks_count, levels, durations, is_properties_min=True)
            case RuleType.MIN_LEVELS_MAX_DURATION:
                return _optimal_min_levels(tasks_count, levels, durations, is_properties_min=False)
            case _:
                raise ValueError("Нет такого правила")

    def rule_text(self):
        match self.rule_type:
            case RuleType.MIN_DURATION:
                return "Работы с наименьшей длительностью"
            case RuleType.MAX_DURATION:
                return "Работы с наибольшей длительностью"
            case RuleType.MIN_RESERVE:
                return "Работы с наименьшим резервом"
            case RuleType.MIN_LEVELS_MIN_DURATION:
                return "Работы с младшим уровнем (ближе к началу), при совпаднии уровня - работа наименьшей длительности"
            case RuleType.MIN_LEVELS_MAX_DURATION:
                return "Работы с младшим уровнем (ближе к началу), при совпаднии уровня - работа наибольшей длительности"
            case _:
                raise ValueError("Нет такого правила")

