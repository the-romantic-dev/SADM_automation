import math
from copy import deepcopy
from typing import List, Dict, Tuple

INFINITE = 2 ** 32


# def calculate_taus(zeros: list, matrix, is_min):
#     taus = []
#     for coord in zeros:
#         tau_value, terms = tau(matrix=matrix, row_index=coord[0], column_index=coord[1], is_min=is_min)
#         taus.append((coord, tau_value, terms))
#     return taus


# def calculate_u(taus: list, is_min):
#     if is_min:
#         return max(taus, key=lambda elem: elem[1])
#     else:
#         return min(taus, key=lambda elem: elem[1])


# def key_of_max_or_min(arr: dict[int, float | int], is_min) -> int:
#     result_key = -1
#     if is_min:
#         result = INFINITE * 2
#     else:
#         result = -INFINITE * 2
#     for i in arr.keys():
#         if (not is_min and arr[i] > result) or (is_min and arr[i] < result):
#             result = arr[i]
#             result_key = i
#     return result_key


# def get_matrix_column(matrix: dict[int, dict[int, float | int]], column_key: int):
#     result = {}
#     for row_key in matrix.keys():
#         result[row_key] = matrix[row_key][column_key]
#     return result


# def rows_without_zeros(matrix: dict[int, dict[int, float | int]]):
#     result = []
#     for i in matrix.keys():
#         if 0 not in matrix[i].values():
#             result.append(i)
#     return result


# def columns_without_zeros(matrix: dict[int, dict[int, float | int]]):
#     columns_keys = matrix[list(matrix.keys())[0]].keys()
#     columns = {}
#     for column_key in columns_keys:
#         columns[column_key] = get_matrix_column(matrix=matrix, column_key=column_key)
#     result = []
#     for i in columns.keys():
#         if 0 not in columns[i].values():
#             result.append(i)
#     return result


# def zeroing_row(matrix: dict[int, dict[int, float | int]], is_min: bool, row_index: int):
#     if is_min:
#         curr_element = min(matrix[row_index].values())
#     else:
#         curr_element = max(matrix[row_index].values())
#     for j in matrix[row_index].keys():
#         matrix[row_index][j] = matrix[row_index][j] - curr_element
#     return curr_element
#
#
# def zeroing_column(matrix: dict[int, dict[int, float | int]], is_min, column_key: int):
#     column = get_matrix_column(matrix=matrix, column_key=column_key)
#     if is_min:
#         curr_element = min(column.values())
#     else:
#         curr_element = max(column.values())
#     for j in matrix.keys():
#         matrix[j][column_key] = matrix[j][column_key] - curr_element
#     return curr_element


# def make_zeroing_matrix(matrix, is_min) -> list[float | int]:
#     result = deepcopy(matrix)
#     terms = []
#     for i in rows_without_zeros(result):
#         terms.append(zeroing_row(matrix=result, is_min=is_min, row_index=i))
#     for i in columns_without_zeros(result):
#         terms.append(zeroing_column(matrix=result, is_min=is_min, column_key=i))
#     return terms, result


# def find_zeros_in_matrix(matrix):
#     result = []
#
#     for i in matrix.keys():
#         for j in matrix[i].keys():
#             if matrix[i][j] == 0:
#                 result.append((i, j))
#     return result


# def tau(matrix: dict[int, dict[int, float | int]], row_index: int, column_index: int, is_min: bool):
#     row = matrix[row_index].copy()
#     del row[column_index]
#     in_column_index = key_of_max_or_min(arr=row, is_min=is_min)
#
#     column = {}
#     for i in matrix.keys():
#         column[i] = matrix[i][column_index]
#     del column[row_index]
#     in_row_index = key_of_max_or_min(arr=column, is_min=is_min)
#
#     in_row_element = matrix[row_index][in_column_index]
#     in_column_element = matrix[in_row_index][column_index]
#
#     return in_row_element + in_column_element, (in_row_element, in_column_element)


# def remove_row_and_column(matrix: dict[int, dict[int, float | int]], cords):
#     result = deepcopy(matrix)
#     removing_row = cords[0]
#     removing_column = cords[1]
#     del result[removing_row]
#
#     for row in result:
#         del result[row][removing_column]
#     return result


def find_segments(edges: list[tuple[int, int]]):
    def dfs(node, visited, segment):
        segment.append(node)
        if node in graph and not visited.get(node, False):
            visited[node] = True
            dfs(node=graph[node], visited=visited, segment=segment)

    def get_segments(_graph):
        segments = []
        visited = {node: False for node in _graph}
        for node in _graph:
            if not visited[node]:
                segment = []
                dfs(node=node, visited=visited, segment=segment)
                segments.append(segment)
        return segments

    def merge_segments(segments):
        for i in range(len(segments)):
            for j in range(len(segments)):
                if i != j and len(segments[i]) > 0 and len(segments[j]) > 0:
                    if segments[i][-1] == segments[j][0]:
                        segments[i].extend(segments[j][1:])
                        segments[j].clear()
        result = list(filter(lambda elem: len(elem) > 0, segments))
        return result

    graph = {}
    for edge in edges:
        if edge[0] not in graph:
            graph[edge[0]] = edge[1]
    return merge_segments(get_segments(graph))


# def filter_incomplete_paths(matrix, cords: tuple[int, int], current_path: list[tuple[int, int]], is_min):
#     result = deepcopy(matrix)
#     edges = current_path + [cords]
#     excluded_paths = []
#     segments = find_segments(edges=edges)
#     for segment in segments:
#         if len(segment) > 1:
#             _to = segment[0]
#             _from = segment[-1]
#             excluded_paths.append((_from, _to))
#     for path in excluded_paths:
#         if is_min:
#             infinite = INFINITE
#         else:
#             infinite = -INFINITE
#         result[path[0]][path[1]] = infinite
#     return result


def add_candidate(candidates, tree_level: int, excluded_paths: list, included_paths: list,
                  matrix: dict[int, dict[int, float | int]], v, paths_way):
    if tree_level not in candidates:
        candidates[tree_level] = []

    candidates[tree_level].append(
        {
            "ex_paths": excluded_paths,
            "in_paths": included_paths,
            "v": v,
            "matrix": matrix,
            "paths_way": paths_way
        }
    )


def get_better_candidate(candidates, current_evaluation, is_min):
    result = None
    if len(candidates) > 0:
        for step in sorted(candidates.keys(), reverse=True):
            if len(candidates[step]) > 0:
                if is_min:
                    available_vertex = min(candidates[step], key=lambda vertex: vertex["v"])
                    if current_evaluation > available_vertex['v']:
                        result = (step, available_vertex)
                        break
                else:
                    available_vertex = max(candidates[step], key=lambda vertex: vertex["v"])
                    if current_evaluation < available_vertex['v']:
                        result = (step, available_vertex)
                        break
    return result
