from typing import List


class ResourceAllocationSolver:
    def __init__(self, c: List, g: List):
        self.c = c
        self.g = g
        self.calculation_tables = []
        self.x_columns = []
        self.f_columns = []

    def _step(self, n) -> (List[List], List, List):
        if n == 1:
            return self.c, self.g[0]
        x, f = self._step(n - 1)
        calculation_table = []
        for i in range(len(self.c)):
            calculation_table.append([])
            last_row_index = len(calculation_table) - 1
            for j in range(-1, len(self.c)):
                if j <= i:
                    if j == -1:
                        g = 0
                    else:
                        g = self.g[n - 1][j]
                    if i - j - 1 >= 0:
                        prev_f = f[i - j - 1]
                    else:
                        prev_f = 0
                    calculation_table[last_row_index].append((f"{g} + {round(prev_f, 5)}", round(g + prev_f, 5)))
        new_x = []
        new_f = []
        for row in calculation_table:
            curr_max = -1
            curr_max_index = -1
            for i in range(len(row)):
                if row[i][1] > curr_max:
                    curr_max_index = i
                    curr_max = row[i][1]
            new_x.append(curr_max_index)
            new_f.append(curr_max)
        new_x_values = []
        for i in new_x:
            if i - 1 >= 0:
                new_x_values.append(self.c[i-1])
            else:
                new_x_values.append(0)

        for row in calculation_table:
            print(row)
        print("X = ", new_x_values)
        print("F = ", new_f)
        print()
        self.calculation_tables.append(calculation_table)
        self.x_columns.append(new_x_values)
        self.f_columns.append(new_f)
        return new_x, new_f

    def solve(self):
        self._step(len(self.g))
