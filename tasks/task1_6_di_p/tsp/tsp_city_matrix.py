from copy import deepcopy

from tasks.task1_6_di_p.tsp.util import find_segments

INFINITE = 2 ** 32


class TSPCityMatrix:
    def __init__(self,
                 matrix: list[list] | dict[int, dict[int, float | int]],
                 is_min: bool):
        if isinstance(matrix, list):
            indexed_matrix = {}
            replace_inf(matrix, is_min=is_min)
            for i in range(len(matrix)):
                indexed_matrix[i] = {}
                for j in range(len(matrix[i])):
                    indexed_matrix[i][j] = matrix[i][j]
            self.matrix = indexed_matrix
        else:
            self.matrix = matrix
        self.is_min = is_min

    def column(self, index: int) -> dict:
        result = {}
        for row_index in self.matrix.keys():
            result[row_index] = self.matrix[row_index][index]
        return result.copy()

    def size(self):
        return len(self.matrix)

    def row(self, index: int) -> dict:
        return self.matrix[index].copy()

    def delete_row(self, index: int):
        del self.matrix[index]

    def delete_column(self, index: int):
        for row in self.matrix:
            del self.matrix[row][index]

    def delete_cross(self, element_cords: (int, int)):
        self.delete_row(element_cords[0])
        self.delete_column(element_cords[1])

    def get_optimal_in_row(self, index: int):
        return self.get_optimal_in_dict(data=self.row(index))

    def get_optimal_in_column(self, index: int):
        return self.get_optimal_in_dict(data=self.column(index))

    def _get_rows_without_zeros(self):
        result = []
        for i in self.matrix.keys():
            if 0 not in self.matrix[i].values():
                result.append(i)
        return result

    def _get_columns_without_zeros(self):
        columns_keys = self.matrix[list(self.matrix.keys())[0]].keys()
        # columns = {}
        # for column_key in columns_keys:
        #     columns[column_key] = get_matrix_column(matrix=matrix, column_key=column_key)
        result = []
        for i in columns_keys:
            if 0 not in self.column(i).values():
                result.append(i)
        return result

    def _make_zeroing_row(self, index: int):
        if self.is_min:
            curr_element = min(self.matrix[index].values())
        else:
            curr_element = max(self.matrix[index].values())
        for j in self.matrix[index].keys():
            self.matrix[index][j] = self.matrix[index][j] - curr_element
        return curr_element

    def _make_zeroing_column(self, index):
        column = self.column(index)
        if self.is_min:
            curr_element = min(column.values())
        else:
            curr_element = max(column.values())
        for j in self.matrix.keys():
            self.matrix[j][index] = self.matrix[j][index] - curr_element
        return curr_element

    def make_zeroing(self):
        terms = []
        for i in self._get_rows_without_zeros():
            terms.append(self._make_zeroing_row(index=i))
        for i in self._get_columns_without_zeros():
            terms.append(self._make_zeroing_column(index=i))
        return terms

    def copy(self):
        matrix_copy = deepcopy(self.matrix)
        return TSPCityMatrix(matrix=matrix_copy, is_min=self.is_min)

    def find_zeros(self):
        result = []

        for i in self.matrix.keys():
            for j in self.matrix[i].keys():
                if self.matrix[i][j] == 0:
                    result.append((i, j))
        return result

    def _tau(self, row_index: int, column_index: int):
        row = self.row(row_index)
        del row[column_index]
        opt_column_index = self.get_optimal_in_dict(data=row)

        column = self.column(column_index)
        del column[row_index]
        opt_row_index = self.get_optimal_in_dict(data=column)

        opt_row_element = self.matrix[row_index][opt_column_index]
        opt_column_element = self.matrix[opt_row_index][column_index]

        return opt_row_element + opt_column_element, (opt_row_element, opt_column_element)

    def calculate_taus_and_worse_tau(self):
        taus = []
        zeros = self.find_zeros()
        for coord in zeros:
            tau_value, terms = self._tau(row_index=coord[0], column_index=coord[1])
            taus.append((coord, tau_value, terms))

        if self.is_min:
            worse_tau = max(taus, key=lambda elem: elem[1])
        else:
            worse_tau = min(taus, key=lambda elem: elem[1])
        return taus, worse_tau

    def get_optimal_in_dict(self, data: dict[int, float | int]) -> int:
        result_key = -1
        if self.is_min:
            result = INFINITE * 2
        else:
            result = -INFINITE * 2
        for i in data.keys():
            if (not self.is_min and data[i] > result) or (self.is_min and data[i] < result):
                result = data[i]
                result_key = i
        return result_key

    def filter_incomplete_paths(self, cords: tuple[int, int], current_path: list[tuple[int, int]]):
        edges = current_path + [cords]
        excluded_paths = []
        segments = find_segments(edges=edges)
        for segment in segments:
            if len(segment) > 1:
                _to = segment[0]
                _from = segment[-1]
                excluded_paths.append((_from, _to))
        for path in excluded_paths:
            if self.is_min:
                infinite = INFINITE
            else:
                infinite = -INFINITE
            self.matrix[path[0]][path[1]] = infinite

    def exclude_path(self, path: tuple[int, int]):
        if self.is_min:
            infinite = INFINITE
        else:
            infinite = -INFINITE
        _from = path[0]
        _to = path[1]
        self.matrix[_from][_to] = infinite
        self._make_zeroing_row(_from)
        self._make_zeroing_column(_to)
        # zeroing_row(matrix=exclude_matrix, is_min=is_min, row_index=u[0][0])
        # zeroing_column(matrix=exclude_matrix, is_min=is_min, column_key=u[0][1])


# ---- class end ----
def replace_inf(matrix: list[list], is_min: bool):
    infinite = -INFINITE
    if is_min:
        infinite = INFINITE
    for row in matrix:
        for j in range(len(row)):
            if isinstance(row[j], str):
                row[j] = infinite
