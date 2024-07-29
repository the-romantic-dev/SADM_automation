import json
from pathlib import Path

from tasks.task2_1_st.solvers.scheduling_problem.rule import RuleType

folder = Path(r"D:\Убежище\Университет\6 семестр\САПР\1\Сиднев\Садовников")

graph_edges = [
    (1, 2, 5), (1, 3, 4), (1, 4, 4), (1, 5, 7),
    (2, 6, 6),
    (3, 6, 7),
    (4, 5, 6), (4, 7, 5),
    (5, 6, 5), (5, 7, 5), (5, 8, 4),
    (6, 7, 5), (6, 8, 5),
    (7, 8, 3),
    (8, 9, 7),
]

variant = 9

is_sidnev = True

performers_number = 4

rule_types = [RuleType.MIN_RESERVE, RuleType.MAX_DURATION, RuleType.MIN_RESERVE]

intensity_limit = 0.8

standard_deviation = 0.09

overtime_limit = 0.17

# Создаем словарь с данными
rule_types_json = [rule.name for rule in rule_types]
data = {
    'graph_edges': graph_edges,
    'variant': variant,
    'is_sidnev': is_sidnev,
    'performers_number': performers_number,
    'intensity_limit': intensity_limit if not is_sidnev else None,
    'standard_deviation': standard_deviation if not is_sidnev else None,
    'overtime_limit': overtime_limit if not is_sidnev else None,
    'rule_types': rule_types_json if not is_sidnev else [rule_types_json[0]]
}

if __name__ == "__main__":
    with open(f'{folder.as_posix()}/data.json', 'w') as file:
        json.dump(data, file)

