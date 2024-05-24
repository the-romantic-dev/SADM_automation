import json
from pathlib import Path

from tasks.scheduling_theory.solvers.scheduling_problem.rule import RuleType

folder = Path(r"D:\Убежище\Университет\6 семестр\САПР\1\Сиднев\Писарик")

graph_edges = [
    (1, 2, 6), (1, 3, 7),
    (2, 4, 3), (2, 3, 4), (2, 5, 7),
    (3, 4, 6), (3, 5, 3), (3, 6, 6),
    (4, 5, 5), (4, 7, 3),
    (5, 7, 5), (5, 6, 5), (5, 8, 7),
    (6, 7, 3), (6, 8, 7),
    (7, 8, 6),
]

variant = 8

is_sidnev = True

performers_number = 3

rule_types = [RuleType.MAX_DURATION, RuleType.MAX_DURATION, RuleType.MIN_RESERVE]

intensity_limit = 0.7

standard_deviation = 0.1

overtime_limit = 0.16

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

