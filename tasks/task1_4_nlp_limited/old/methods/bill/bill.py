"""Файл метода Била"""
import sympy as sp
from tabulate import tabulate
from ..npp_method import NPPMethod
from .bill_util import gag_fix, is_opt, build_start_table, build_table_2, build_table_1
from docx import Document
from docx.document import Document as DocumentType
from my_io import io
from util import merge_symplex_table_and_vars
from my_docx import docx_output

x = list(sp.symbols("x1 x2 x3 x4"))
u = []


def prepare_table_1_for_report(table, base, free):
    row_headers = [sp.pretty(var) for var in base] + ["grads", "def grads"]
    column_headers = ["-"] + [sp.pretty(var) for var in free] + ["b"]
    for i, _ in enumerate(table):
        for j, _ in enumerate(table[i]):
            table[i][j] = sp.pretty(table[i][j])
        table[i] = [row_headers[i]] + table[i]
    table = [column_headers] + table
    len_row = 3
    for i, row in enumerate(table):
        if len(row) < len_row:
            table[i] += ["-"]
    return table


def prepare_table_2_for_report(table, base, free):
    row_headers = [sp.pretty(var) for var in base]
    column_headers = ["-"] + [sp.pretty(var) for var in free] + ["b"]
    for i, _ in enumerate(table):
        for j, _ in enumerate(table[i]):
            table[i][j] = sp.pretty(table[i][j])
        table[i] = [row_headers[i]] + table[i]
    table = [column_headers] + table
    len_row = 3
    for i, row in enumerate(table):
        if len(row) < len_row:
            table[i] += ["-"]
    return table


def get_current_point(table1, free, base):
    X = []
    if x[0] in free:
        X.append(0)
    else:
        X.append(table1[base.index(x[0])][-1])

    if x[1] in free:
        X.append(0)
    else:
        X.append(table1[base.index(x[1])][-1])
    return sp.Matrix(X)


class Bill(NPPMethod):
    """Класс метода Била"""

    def __init__(self):
        super().__init__()
        self.tables_1 = []
        self.tables_2 = []
        self.all_opt_cols = []
        self.all_opt_rows = []
        self.all_free = []
        self.all_base = []
        self.u_expressions = []
        self.f_expressions = []

    def solve(self, f, limitations):
        """Решает задачу этим методом"""
        self.f = f
        self.limits = limitations
        self.f_expressions.append(f)
        gag_fix(x=x, limitations=limitations)
        new_expr = f
        table1, free, base = build_start_table(
            x=x, limitations=limitations, expr=new_expr
        )
        # table2 = None
        while not is_opt(table1):
            self.all_free.append(free)
            self.all_base.append(base)
            self.tables_1.append(table1)
            self.track.append(get_current_point(table1, free, base))
            table2, opt_col, new_u = build_table_2(table1=table1, free=free)
            self.all_opt_cols.append(opt_col)
            self.u_expressions.append(new_u)
            self.tables_2.append(table2)
            table1, free, base, new_expr, opt_row = build_table_1(
                table2=table2, opt_col=opt_col, free=free, base=base, expr=new_expr, new_u=new_u
            )
            self.all_opt_rows.append(opt_row)
            self.f_expressions.append(new_expr)
        self.solution['x1'] = table1[base.index(x[0])][-1]
        self.solution['x2'] = table1[base.index(x[1])][-1]
        self.solution['f'] = f.subs({x[0]: self.solution['x1'], x[1]: self.solution['x2']})
        self.all_free.append(free)
        self.all_base.append(base)
        self.tables_1.append(table1)
        self.track.append(get_current_point(table1, free, base))

    def report(self, output_func):
        for i, _ in enumerate(self.tables_1):
            output_header = f"Итерация {i}"
            self.tables_1[i] = prepare_table_1_for_report(
                self.tables_1[i], self.all_base[i], self.all_free[i]
            )
            output_table_1 = tabulate(
                self.tables_1[i],
                headers="firstrow",
                tablefmt="grid",
                colalign=("center", "center", "center"),
            )
            output_table_2 = ""
            if i < len(self.tables_2):
                self.tables_2[i] = prepare_table_2_for_report(
                    self.tables_2[i], self.all_base[i], self.all_free[i]
                )
                output_table_2 = tabulate(
                    self.tables_2[i],
                    headers="firstrow",
                    tablefmt="grid",
                    colalign=("center", "center", "center"),
                )

            output_func(output_header)
            output_func(self.f_expressions[i])
            output_func(output_table_1)
            if i < len(self.u_expressions):
                output_func(self.u_expressions[i])
            output_func(output_table_2)
        output_func(f'result = {self.solution["f"]}')

    def create_doc(self, name: str):
        doc: DocumentType = Document()
        for i, _ in enumerate(self.tables_1):
            pass

        for i in range(len(self.tables_1)):
            data1 = merge_symplex_table_and_vars(
                symplex_table=self.tables_1[i],
                free=self.all_free[i],
                base=self.all_base[i] + []
            )
            table1 = docx_output.create_table_filled(
                document=doc,
                data=data1
            )

            if i < len(self.tables_2):
                docx_output.paint_table_column(table1, self.all_opt_cols[i] + 1)
                data2 = merge_symplex_table_and_vars(
                    symplex_table=self.tables_2[i],
                    free=self.all_free[i],
                    base=self.all_base[i] + (['u'] if len(self.tables_2[i]) > len(self.all_base[i]) else [])
                )
                table2 = docx_output.create_table_filled(
                    document=doc,
                    data=data2
                )
                docx_output.paint_table_column(table2, self.all_opt_cols[i] + 1)
                docx_output.paint_table_row(table2, self.all_opt_rows[i] + 1)
        io.save_doc(doc=doc, name=name)
