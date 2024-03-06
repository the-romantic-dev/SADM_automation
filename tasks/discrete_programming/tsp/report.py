from dataclasses import dataclass

from tasks.discrete_programming.tsp.tsp_city_matrix import TSPCityMatrix


@dataclass
class TSPReportDataMinimal:
    # Уровень узла на дереве
    tree_level: int

    # Преобразованная матрица, где в каждой строке и каждом столбце есть
    # хотя бы один нуль
    zeroing_matrix: TSPCityMatrix

    # Список элементов, вычтенных из строк/столбцов матрицы
    # для получения zeroing_matrix. В сумме дают h.
    h_terms: list[float | int]


@dataclass
class TSPReportDataLast:
    # Уровень узла на дереве
    tree_level: int

    # Включенные и исключенные пути на текущем узле
    paths_way: list[tuple[tuple[int, int], bool]]

    # Начальная матрица узла
    start_matrix: TSPCityMatrix

    # Итоговый оптимальный путь
    result_path: list[tuple[int, int]] | None


@dataclass
class TSPReportData(TSPReportDataMinimal):
    # Начальная матрица узла
    start_matrix: TSPCityMatrix

    # Значение оценочной функции родительского узла
    previous_evaluation: float | int

    # Включенные и исключенные пути на текущем узле
    paths_way: list[tuple[tuple[int, int], bool]]

    # Список сумм оптимальных элементов строк и столбцов
    taus: list[tuple[tuple[int, int], float | int, tuple[float | int, float | int]]]

    # Наихудший из списка tau. Путь k -> l
    worst_tau: tuple[tuple[int, int], float | int, tuple[float | int, float | int]]

    # Значение оценочной функции для ветки, исключающей путь k -> l
    exclude_evaluation: float | int

    # Матрица с удаленными из нее строкой k и столбцом l
    trimmed_matrix: TSPCityMatrix

    # Матрица с удаленными из нее строкой k и столбцом l +
    # в ней элементы, дающие пути, не обходящие все вершины,
    # заменены на бесконечность
    filtered_paths_matrix: TSPCityMatrix

    # Значение оценочной функции для ветки, включающей путь k -> l
    include_evaluation: float | int

    # Флаг, показывающий, делали ли мы возврат вверх по дереву вариантов
    is_next_from_candidates: bool = False

    # Флаг, показывающий, является оптимальным на этом шаге включение или исключение
    # пути k -> l
    is_included: bool = False
