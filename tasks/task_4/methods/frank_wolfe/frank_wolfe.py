from sympy import linear_eq_to_matrix, pretty, Rational
from docx import Document
from my_docx import docx_output
from tabulate import tabulate
from ..npp_method import NPPMethod
from util import recalculate_symplex_table, merge_symplex_table_and_vars
from .frank_wolfe_util import *
from my_io import io

x1, x2 = symbols("x1 x2")
v1, v2, lambda1, lambda2, y1, y2, k1, k2 = symbols("v1 v2 λ1 λ2 y1 y2 k1 k2")


class FrankWolfe(NPPMethod):
    """Метод Франка-Вульфа через квадратичную форму"""

    def __init__(self) -> None:
        super().__init__()
        self.solution = {}
        self.A = None
        self.b = None
        self.H = None
        self.p = None
        self.AEOO_HOEAT = None
        self.bp = None
        self.kk_free_track = []
        self.kk_base_track = []
        self.kk_symplex_track = []
        self.Z_expr_track = []
        self.Z_track = []
        self.tilda_Z_track = []
        self.fw_free_track = []
        self.fw_base_track = []
        self.fw_symplex_track = []
        self.t_default_track = []
        self.t_track = []
        self.kk_opt_col_track = []
        self.kk_opt_row_track = []
        self.fw_opt_col_track = []
        self.fw_opt_row_track = []

    def solve(self, f, limitations):
        self._solve(f, limitations)

    def _solve(self, f, limitations):
        self.f = f
        self.limits = limitations
        # Подготовка данных для метода
        self.p, self.H = build_quadratic_form_matrices(f)
        self.A, self.b = linear_eq_to_matrix(limitations[:2], (x1, x2))
        # Построение матрицы ограничений
        self.AEOO_HOEAT = build_AEOO_HOOEAT(self.A, self.H)
        self.bp = build_bp(self.b, self.p)
        # Построение симплекс-таблицы для нахождения начального базиса без kk
        kk_symplex_table = build_kk_symplex_table(
            self.AEOO_HOEAT, self.bp
        )
        self.kk_symplex_track.append(kk_symplex_table)
        free = [x1, x2, v1, v2, lambda1, lambda2]
        self.kk_free_track.append(free)
        base = [y1, y2, k1, k2]
        self.kk_base_track.append(base)
        self.track.append(get_current_point(kk_symplex_table, free, base))
        while not is_symplex_table_opt(kk_symplex_table):
            opt_col, opt_row = find_opt_column_and_row(kk_symplex_table)
            self.kk_opt_col_track.append(opt_col)
            self.kk_opt_row_track.append(opt_row)
            kk_symplex_table = recalculate_symplex_table(kk_symplex_table, opt_col, opt_row)
            base, free = recalculate_base_and_free(base, free, opt_col, opt_row)
            self.kk_free_track.append(free)
            self.kk_base_track.append(base)
            self.kk_symplex_track.append(kk_symplex_table)
            self.track.append(get_current_point(kk_symplex_table, free, base))

        current_Z_tilda = build_Z(kk_symplex_table, base=base, is_tilda=True)
        current_Z = build_Z(kk_symplex_table, base=base, is_tilda=False)
        current_Z_expr = build_Z_expr(kk_symplex_table, free=free, base=base)
        self.Z_expr_track.append(current_Z_expr)
        self.tilda_Z_track.append(current_Z_tilda)
        self.Z_track.append(current_Z)
        fw_symplex_table, free = build_fw_symplex_table(free, base, kk_symplex_table, self.Z_expr_track[0], self.tilda_Z_track[0])
        current_Z_value = fw_symplex_table[-1][-1]
        self.fw_free_track.append([free])
        self.fw_base_track.append([base])
        self.fw_symplex_track.append([fw_symplex_table])
        self.track.append(get_current_point(fw_symplex_table, free, base))
        self.fw_opt_col_track.append([])
        self.fw_opt_row_track.append([])
        while True:
            if fw_symplex_table[-1][-1] == 0:
                break
            if fw_symplex_table[-1][-1] <= Rational("1/2") * current_Z_value:
                K = build_Z(fw_symplex_table, base, is_tilda=False) - current_Z
                tilda_K = build_Z(fw_symplex_table, base, is_tilda=True) - current_Z_tilda
                t_default = - (K.T * current_Z_tilda).det() / (K.T * tilda_K).det()
                self.t_default_track.append(t_default)
                t = min(t_default, 1)
                self.t_track.append(t)
                new_Z_expr = current_Z_expr + t * (
                            build_Z_expr(fw_symplex_table, free=free, base=base) - current_Z_expr)
                new_Z = current_Z + t * K
                fw_symplex_table = rebuild_fw_symplex_table(free=free, base=base,new_Z_expr=new_Z_expr, new_Z=new_Z)
                current_Z = new_Z
                current_Z_expr = new_Z_expr
                current_Z_tilda = Z2tilda_Z(new_Z)
                self.Z_expr_track.append(current_Z_expr)
                self.tilda_Z_track.append(current_Z_tilda)
                self.Z_track.append(current_Z)
                self.fw_free_track.append([free])
                self.fw_base_track.append([base])
                self.fw_symplex_track.append([fw_symplex_table])
                self.track.append(get_current_point(fw_symplex_table, free, base))
                self.fw_opt_col_track.append([])
                self.fw_opt_row_track.append([])
                if fw_symplex_table[-1][-1] == 0:
                    break
            if is_symplex_table_opt(fw_symplex_table, isMax=False):
                break
            opt_col, opt_row = find_opt_column_and_row(fw_symplex_table, isMax=False)
            self.fw_opt_col_track[-1].append(opt_col)
            self.fw_opt_row_track[-1].append(opt_row)
            fw_symplex_table = recalculate_symplex_table(fw_symplex_table, opt_col, opt_row)
            base, free = recalculate_base_and_free(base, free, opt_col, opt_row)
            self.fw_free_track[-1].append(free)
            self.fw_base_track[-1].append(base)
            self.fw_symplex_track[-1].append(fw_symplex_table)
            self.track.append(get_current_point(fw_symplex_table, free, base))

        self.solution['x1'] = fw_symplex_table[base.index(symbols('x1'))][-1]
        self.solution['x2'] = fw_symplex_table[base.index(symbols('x2'))][-1]
        self.solution['f'] = f.subs({
            symbols('x1'): self.solution['x1'],
            symbols('x2'): self.solution['x2'],
        })

    def get_report(self):
        """Формирует строку с отчетом по работе метода"""
        header = """
        |---------------------------------------------------------|
        |--------------ОТЧЕТ ПО МЕТОДУ ФРАНКА ВУЛЬФА--------------|
        |---------------------------------------------------------|
        """
        table_len = len(self.track)
        tables = []
        for i in range(len(self.kk_symplex_track)):
            if i < len(self.kk_symplex_track):
                for j in range(len(self.kk_symplex_track[i])):
                    if j < len(self.kk_base_track[i]):
                        self.kk_symplex_track[i][j] = [self.kk_base_track[i][j]] + self.kk_symplex_track[i][j]
                    else:
                        k1, k2 = symbols('k1 k2')
                        self.kk_symplex_track[i][j] = [pretty(-k1 - k2)] + self.kk_symplex_track[i][j]
                tabular_data = [
                                   self.kk_free_track[i] + ['b']
                               ] + [[pretty(elem) for elem in row] for row in self.kk_symplex_track[i]]
                tables.append(tabulate(
                    tabular_data,
                    headers='firstrow',
                    tablefmt="grid",
                    floatfmt=('.3f' for i in range(table_len)),
                    colalign=('center' for i in range(table_len))
                ))
        old_i = -1
        for i in range(len(self.fw_symplex_track)):
            for j in range(len(self.fw_symplex_track[i])):
                for k in range(len(self.fw_symplex_track[i][j])):
                    if k < len(self.fw_base_track[i][j]):
                        self.fw_symplex_track[i][j][k] = [self.fw_base_track[i][j][k]] + \
                                                             self.fw_symplex_track[i][j][k]
                    else:
                        self.fw_symplex_track[i][j][k] = ["ZZ"] + self.fw_symplex_track[i][j][k]
                tabular_data = [
                                   self.fw_free_track[i][j] + ['b']
                               ] + [[pretty(elem) for elem in row] for row in self.fw_symplex_track[i][j]]
                table = tabulate(
                    tabular_data,
                    headers='firstrow',
                    tablefmt="grid",
                    floatfmt=('.3f' for i in range(table_len)),
                    colalign=('center' for i in range(table_len))
                )
                pre_table_text = ""
                if old_i != i:
                    old_i = i

                    if i != 0:
                        pre_table_text += f"Предыдущее Z = Z({i-1}) = \n{pretty(self.Z_track[i-1].T)}\n"
                        pre_table_text += "t = min(1, t*)\n"
                        pre_table_text += f"t* = {self.t_default_track[i-1]}\n"
                        pre_table_text += f"result_t = {self.t_track[i-1]}\n"
                    pre_table_text += f"Текущее Z = Z({i}) = \n{pretty(self.Z_track[i].T)}\n"

                tables.append(pre_table_text + "\n" + table)

        result = '\n\n'.join([
                                 header,
                                 "A:",
                                 pretty(self.A),
                                 "b:",
                                 pretty(self.b),
                                 f'H:\n{pretty(self.H)}',
                                 f'p:\n{pretty(self.p)}',
                                 f'left_limit:\n{pretty(self.AEOO_HOEAT)}',
                                 f'right limit:\n{pretty(self.bp)}',
                                 "Таблицы:"
                             ] + tables + [str(i) for i in self.track])
        return result

    def create_doc(self, name: str):
        doc = Document()
        for i in range(len(self.kk_symplex_track)):
            data = merge_symplex_table_and_vars(
                symplex_table=self.kk_symplex_track[i],
                free=self.kk_free_track[i],
                base=self.kk_base_track[i] + [pretty(-k1 - k2)]
            )
            docx_output.create_table_filled(
                document=doc,
                data=data,
                header=f"Франк Вульф шаг №{i}"
            )

        io.save_doc(doc=doc, name=name)
