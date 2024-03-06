from sympy import symbols, Matrix, solve, linear_eq_to_matrix, pretty, I
from scipy.optimize import linprog
from tabulate import tabulate

from my_docx import docx_output
from util import gradient, default_step, gesse
from docx import Document
from docx.document import Document as DocumentType
from my_io import io
from .npp_method import NPPMethod

x1, x2 = symbols('x1 x2')
u = symbols('u')
k1, k2 = symbols('k1 k2')
tol = 1e-4


def build_possible_directions_task(f, active_limits, X):
    """Строит из градентов активных ограничений и целевой функции новую задачу
    для метода возможных направлений"""
    new_limits = []
    K = Matrix([k1, k2])
    grad_f = gradient(X=X, expr=f)
    new_limits.append((grad_f.T * K).det() - u)
    for lim in active_limits:
        grad_lim = gradient(X=X, expr=lim)
        new_limits.append((grad_lim.T * K).det() - u)
    return new_limits


def try_round(arg, accuracy):
    try:
        return round(arg,accuracy)
    except:
        return arg

def optimize_u(limits):
    """Находит решение подзадачи метода возможных направлений"""
    C = [0, 0, -1]
    A, b = linear_eq_to_matrix(limits, (k1, k2, u))
    result = linprog(c=C, A_ub=(-A).tolist(), b_ub=(-b).tolist(), method="highs", bounds=[(-1, 1), (-1, 1), (0, None)])
    return Matrix(list(result.x))


def find_start(limits_le, active_limit_index):
    """Находит начальную точку для метода возможных направлений.
    Точка находится исходя из активного ограничения. x1 всегда 0"""
    active_ge = -limits_le[active_limit_index]
    result = solve(active_ge.subs({x1: 0}), x2)
    return Matrix([0, result[0]])


def is_opt(KU):
    """Проверяет u на оптимальность"""
    return KU[2, 0] <= tol


def calc_t(X, K, f, limits):
    """Находит шаг t"""
    default_t = default_step(X=X, K=K, expr=f)
    # univ1 = univariate_step(X,K,f)
    # univ2 = univariate_step_my(X,K,f)
    t_preds = []
    sym_t = symbols('t')
    new_X = [X[0, 0] + sym_t * K[0, 0], X[1, 0] + sym_t * K[1, 0]]
    for lim in limits:
        lim_t = lim.subs({
            x1: new_X[0],
            x2: new_X[1]
        })
        sol_t = solve(lim_t, sym_t)
        if not sol_t[0].has(I):
            t_preds.append(max(sol_t))
    return min([default_t] + t_preds)


def find_active_limits(X, limits):
    tol = 1e-4
    result = []
    for lim in limits:
        if abs(lim.subs({x1: X[0, 0], x2: X[1, 0]})) <= tol:
            result.append(lim)
    return result


def convert_limits_le_to_ge(limits_le):
    return [-lim for lim in limits_le]


class PossibleDirections(NPPMethod):
    def __init__(self):
        super().__init__()
        self.u_track = []

    def solve(self, f, limits_le):
        self.limits = limits_le
        self.f = f
        limits_ge = convert_limits_le_to_ge(limits_le)
        X = find_start(limits_le=limits_le, active_limit_index=0)
        self.track.append(X)
        self.values_track.append(f.subs({x1: X[0, 0], x2: X[1, 0]}))
        while True:
            active_limits = find_active_limits(X, limits_ge)
            K = None
            if len(active_limits) == 0:
                self.u_track.append('-')
                K = -gesse(X=X, expr=f).inv() * gradient(X=X, expr=f)
            else:
                pd_limits = build_possible_directions_task(f=f, active_limits=active_limits, X=X)
                KU = optimize_u(pd_limits)
                if is_opt(KU):
                    break
                K = KU[0:2, 0]
                self.u_track.append(KU[2, 0])
            t = calc_t(X, K, f, limits_le)
            new_X = X + t * K
            self.track.append(new_X)
            self.values_track.append(f.subs({x1: new_X[0, 0], x2: new_X[1, 0]}))
            if (new_X - X).norm() < tol:
                break
            X = new_X
        self.u_track.append(0)
        self.solution['x1'] = self.track[-1][0, 0]
        self.solution['x2'] = self.track[-1][1, 0]
        self.solution['f'] = f.subs({x1: self.track[-1][0, 0], x2: self.track[-1][1, 0]})

    def get_report(self):
        """Формирует строку с отчетом по работе метода"""
        header = """
        |---------------------------------------------------------|
        |----------ОТЧЕТ ПО МЕТОДУ ВОЗМОЖНЫХ НАПРАВЛЕНИЙ----------|
        |---------------------------------------------------------|
        """
        table_len = len(self.track)
        tabular_data = [
            ['i'] + [i for i in range(table_len)],
            [pretty(x1)] + [float(X[0, 0]) for X in self.track],
            [pretty(x2)] + [float(X[1, 0]) for X in self.track],
            ['u'] + [u for u in self.u_track],
            ['f'] + [value for value in self.values_track],
        ]
        tolerance = f"Погрешность: {tol}"
        table = tabulate(
            tabular_data,
            headers='firstrow',
            tablefmt="grid",
            floatfmt=('.3f' for i in range(table_len)),
            colalign=('center' for i in range(table_len))
        )

        result = '\n\n'.join([
            header,
            "Погрешность:",
            tolerance,
            "Таблица шагов:",
            table
        ])
        return result

    def create_doc(self, name: str):
        doc: DocumentType = Document()
        table_len = len(self.track)
        data = [
            ['i'] + [i for i in range(table_len)],
            [pretty(x1)] + [round(float(X[0, 0]), 3) for X in self.track],
            [pretty(x2)] + [round(float(X[1, 0]), 3) for X in self.track],
            ['u'] + [try_round(u, 3) for u in self.u_track],
            ['f'] + [round(value, 3) for value in self.values_track],
        ]
        docx_output.create_table_filled(
            document=doc,
            data=data
        )
        io.save_doc(doc=doc, name=name)
