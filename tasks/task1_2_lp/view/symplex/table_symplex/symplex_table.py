from sympy import latex

from report.model.elements.formula import Formula
from report.model.elements.table import Table
from report.model.report_prettifier import rational_latex
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution

in_col_color = "BDD6EE"
out_row_color = "FFE599"
cross_cell_color = "DEDEC4"
black_color = "000000"


class SymplexTable:
    def __init__(self, basis_solution: BasisSolution, swap: tuple[int, int]):
        self.sol = basis_solution
        self.swap = swap

    @property
    def _header_row(self) -> list[str | Formula]:
        header_row = [""]
        header_row.extend([Formula(f"x_{i + 1}") for i in self.sol.free])
        header_row.append(Formula("b"))
        if self.swap is not None:
            header_row.append(Formula("-\\frac{b_i}{a_i}"))
        return header_row

    def _expr_row(self, basis_index: int) -> list[str | Formula]:
        basis_var = self.sol.basis_variables[basis_index]
        row = [Formula(latex(basis_var))]
        coeffs = self.sol.basis_coeffs[basis_index]
        b = self.sol.basis_values[basis_index]
        row.extend([Formula(rational_latex(c)) for c in coeffs])
        row.append(Formula(rational_latex(b)))
        if self.swap is not None:
            in_var_index = self.sol.free.index(self.swap[1])
            a = coeffs[in_var_index]
            row.append(Formula(rational_latex(-b / a)))
        return row

    @property
    def _f_row(self):
        row = [Formula("f")]
        coeffs = self.sol.objective_coeffs
        value = self.sol.objective_value
        row.extend([Formula(rational_latex(c)) for c in coeffs])
        row.append(Formula(rational_latex(value)))
        if self.swap is not None:
            row.append("")
        return row

    @property
    def _color_fills(self):
        result = {(0, 0): black_color}
        if self.swap is not None:
            rows_count = 2 + len(self.sol.basis)
            cols_count = 3 + len(self.sol.free)
            result[(rows_count - 1, cols_count - 1)] = black_color

            out_var_row = self.sol.basis.index(self.swap[0]) + 1
            in_var_col = self.sol.free.index(self.swap[1]) + 1
            for col_i in range(cols_count):
                if col_i != in_var_col:
                    result[(out_var_row, col_i)] = out_row_color
            for row_i in range(rows_count):
                if row_i != out_var_row:
                    result[(row_i, in_var_col)] = in_col_color
            result[(out_var_row, in_var_col)] = cross_cell_color
        return result

    @property
    def table(self) -> Table:
        table_data = [self._header_row]
        for i in range(len(self.sol.basis)):
            table_data.append(self._expr_row(i))
        table_data.append(self._f_row)
        color_fills = self._color_fills
        return Table(table_data, color_fills)
