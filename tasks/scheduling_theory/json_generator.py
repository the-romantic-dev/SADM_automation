import json
from pathlib import Path

from tasks.scheduling_theory.solvers.scheduling_problem.rule import RuleType

folder = Path(r"D:\Убежище\Университет\6 семестр\САПР\1\Сабонис\Кейта")

graph_edges = [
    (1, 2, 3), (1, 3, 10),
    (2, 3, 14), (2, 5, 13), (2, 4, 14), (2, 7, 8),
    (3, 5, 15),
    (4, 5, 16), (4, 6, 5), (4, 8, 2),
    (5, 6, 7), (5, 7, 7), (5, 8, 18),
    (6, 7, 2), (6, 8, 11), (6, 9, 6),
    (7, 8, 4), (7, 9, 4),
    (8, 9, 14)
]

variant = 87

is_sidnev = False

performers_number = 3

rule_types = [RuleType.MIN_DURATION, RuleType.MAX_DURATION, RuleType.MIN_RESERVE]

intensity_limit = 0.6

standard_deviation = 0.09

overtime_limit = 0.19

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

