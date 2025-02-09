from typing import List
from copy import deepcopy

from tasks.task1_6_di_p.tsp.model.report_dataclasses import TSPReportData, TSPReportDataMinimal, TSPReportDataLast
from tasks.task1_6_di_p.tsp.old.util import add_candidate, get_better_candidate
from tasks.task1_6_di_p.tsp.model.tsp_city_matrix import TSPCityMatrix

import os

os.environ["PATH"] += os.pathsep + r'D:\Apps\Graphviz-12.2.1-win64\bin'


class TSPSolver:
    def __init__(self, list_matrix: List[List]):
        self.list_matrix = list_matrix

    def solve_max(self, report_data=None):
        return self._solve(is_min=False, report_data=report_data)

    def solve_min(self, report_data=None):
        return self._solve(is_min=True, report_data=report_data)

    def _step(self, tree_level, start_matrix: TSPCityMatrix, previous_evaluation, paths_way, excluded_paths,
              included_paths,
              candidates: dict[int, list],
              report_data: list[TSPReportDataMinimal | TSPReportData | TSPReportDataLast]):
        is_min = start_matrix.is_min
        # Шаг 1.
        # Находим координаты всех нулей в матрице
        if start_matrix.size() == 2:
            zeros = start_matrix.find_zeros()
            filtered_zeros = []

            def is_pairs_intersect(pair: tuple[int, int]):
                for a, b in filtered_zeros:
                    if pair[0] == a or pair[1] == b:
                        return True
                return False

            for z in zeros:
                if not is_pairs_intersect(z):
                    filtered_zeros.append(z)

            result_path = included_paths + filtered_zeros
            report = TSPReportDataLast(
                tree_level=tree_level,
                paths_way=paths_way,
                start_matrix=start_matrix,
                result_path=result_path
            )
            report_data.append(report)
            return 1

        # Для каждого нуля находим оптимальный элемент в строке и столбце.
        # Каждый tau равен их сумме
        # worse_tau(k, l) равен худшему элементу из taus
        taus, worse_tau = start_matrix.calculate_taus_and_worse_tau()

        # Шаг 2.
        # Вычисляем оценочную функцию v для случая исключения пути (k, l) из результата
        exclude_evaluation = previous_evaluation + worse_tau[1]

        # Шаг 3.
        # Модифицируем матрицу, удаляя из нее строку k и столбец l
        trimmed_matrix = start_matrix.copy()
        trimmed_matrix.delete_cross(element_cords=worse_tau[0])
        # remove_row_and_column(matrix=start_matrix, cords=u[0])

        # Элементы, дающие пути, не обходящие все вершины, меняем на бесконечность
        filtered_paths_matrix = trimmed_matrix.copy()
        # filtered_paths_matrix.filter_incomplete_paths(
        #     cords=worse_tau[0],
        #     current_path=included_paths
        # )

        # Шаг 4.
        # h равен сумме вычтенных элементов.
        # Делаем так, чтобы в каждой строке и каждом столбце матрицы был хотя бы один нуль.
        # Делаем это, вычитая max/min элемент в строке/столбце из элементов строки/столбца
        zeroing_matrix = filtered_paths_matrix.copy()
        h_terms = zeroing_matrix.make_zeroing()
        h = sum(h_terms)

        # Вычисляем оценочную функцию v для случая включения пути (k, l) в результат
        include_evaluation = previous_evaluation + h

        report = TSPReportData(
            tree_level=tree_level, start_matrix=start_matrix, previous_evaluation=previous_evaluation,
            paths_way=deepcopy(paths_way), taus=taus, worst_tau=worse_tau, exclude_evaluation=exclude_evaluation,
            trimmed_matrix=trimmed_matrix, filtered_paths_matrix=filtered_paths_matrix,
            zeroing_matrix=zeroing_matrix, h_terms=h_terms, include_evaluation=include_evaluation
        )
        # Шаг 5.
        # Определяем оптимальную ветку на графе по оценочной функции
        if is_min:
            current_step_v = min(exclude_evaluation, include_evaluation)
        else:
            current_step_v = max(exclude_evaluation, include_evaluation)

        include_matrix = zeroing_matrix.copy()

        exclude_matrix = start_matrix.copy()
        exclude_matrix.exclude_path(worse_tau[0])

        other_candidate = get_better_candidate(candidates=candidates, current_evaluation=current_step_v, is_min=is_min)
        if other_candidate is not None:
            report.is_next_from_candidates = True
            candidates[other_candidate[0]].remove(other_candidate[1])

            add_candidate(
                candidates=candidates,
                tree_level=tree_level, excluded_paths=deepcopy(excluded_paths) + [worse_tau[0]],
                included_paths=deepcopy(included_paths),
                matrix=exclude_matrix,
                v=exclude_evaluation,
                paths_way=paths_way + [(worse_tau[0], False)])

            add_candidate(
                candidates=candidates,
                tree_level=tree_level, excluded_paths=deepcopy(excluded_paths),
                included_paths=deepcopy(included_paths) + [worse_tau[0]],
                matrix=include_matrix,
                v=include_evaluation,
                paths_way=paths_way + [(worse_tau[0], True)]
            )

            report_data.append(report)

            return self._step(
                tree_level=other_candidate[0] + 1,
                start_matrix=other_candidate[1]["matrix"],
                previous_evaluation=other_candidate[1]["v"],
                excluded_paths=other_candidate[1]["ex_paths"],
                included_paths=other_candidate[1]["in_paths"],
                candidates=candidates,
                paths_way=other_candidate[1]["paths_way"],
                report_data=report_data
            )
        else:
            report.is_next_from_candidates = False
            # Если получена матрица размерности 1, то заканчиваем вычисления

            if current_step_v == include_evaluation:
                # Если оптимальным является включение пути в результат, то
                # в следующий шаг передаем просто модифицированную матрицу
                next_step_matrix = include_matrix
                hanging_matrix = exclude_matrix
                hanging_v = exclude_evaluation
                report.is_included = True
                add_candidate(
                    candidates=candidates,
                    tree_level=tree_level, excluded_paths=deepcopy(excluded_paths) + [worse_tau[0]],
                    included_paths=deepcopy(included_paths),
                    matrix=hanging_matrix,
                    v=hanging_v,
                    paths_way=paths_way + [(worse_tau[0], False)])
                paths_way.append((worse_tau[0], True))
                included_paths.append(worse_tau[0])
            else:
                # Если оптимальным является исключение пути из результата, то
                # в следующий шаг передаем матрицу, где в элементе (k, l)
                # ставим бесконечность, а из строки и столбца вычитаем максимальные элементы в них
                next_step_matrix = exclude_matrix
                hanging_matrix = include_matrix
                hanging_v = include_evaluation
                report.is_included = False
                add_candidate(
                    candidates=candidates,
                    tree_level=tree_level, excluded_paths=deepcopy(excluded_paths),
                    included_paths=deepcopy(included_paths) + [worse_tau[0]],
                    matrix=hanging_matrix,
                    v=hanging_v,
                    paths_way=paths_way + [(worse_tau[0], True)])
                paths_way.append((worse_tau[0], False))
                excluded_paths.append(worse_tau[0])

            report_data.append(report)
            return self._step(
                tree_level=tree_level + 1, start_matrix=next_step_matrix, excluded_paths=excluded_paths,
                previous_evaluation=current_step_v,
                included_paths=included_paths, candidates=candidates, paths_way=paths_way,
                report_data=report_data
            )

    def _solve(self, is_min, report_data=None):
        tsp_city_matrix = TSPCityMatrix(self.list_matrix, is_min=is_min)
        if report_data is None:
            report_data = []

        terms = tsp_city_matrix.make_zeroing()

        h = sum(terms)
        zero_step_v = h
        report_zero = TSPReportDataMinimal(
            tree_level=-1,
            zeroing_matrix=tsp_city_matrix,
            h_terms=terms
        )
        report_data.append(report_zero)
        result = self._step(tree_level=0, start_matrix=tsp_city_matrix, previous_evaluation=zero_step_v,
                            excluded_paths=[], included_paths=[], candidates={},
                            report_data=report_data, paths_way=[])
        return result
