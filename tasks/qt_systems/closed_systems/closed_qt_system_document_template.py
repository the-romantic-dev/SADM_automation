import math
from pathlib import Path
import tasks.qt_systems.closed_systems.data as data
import sympy as sp
from report.docx.objects.document_template import DocumentTemplate
from report.docx.omml import latex2omml
from tasks.qt_systems.closed_systems.solver import ClosedQSSystemSolver
from tasks.qt_systems.open_systems.solver import OpenQSSystemSolver


def min_latex(coefficients):
    a = sp.latex(coefficients[0])
    b = sp.latex(coefficients[1])
    c = sp.latex(coefficients[2])
    d = sp.latex(coefficients[3])
    g = sp.latex(min(coefficients))
    sign = "<" if min(coefficients) < data.lambda_0 else ">"
    return f"\\min\\left( {a},{b},{c},{d} \\right) = {g} {sign} \\lambda_0"


def verdict_text(coefficients):
    return "не соблюдается" if min(coefficients) < data.lambda_0 else "соблюдается"


def min_rho_node(rhos):
    current = -1
    current_value = math.inf
    for i in range(len(rhos)):
        if rhos[i] < current_value:
            current_value = rhos[i]
            current = i
    result = [current]
    for i in range(len(rhos)):
        if i != current and rhos[i] == rhos[current]:
            result.append(i)
    return ",".join([str(i + 1) for i in result])


def max_rho_node(rhos):
    current = -1
    current_value = -1
    for i in range(len(rhos)):
        if rhos[i] > current_value:
            current_value = rhos[i]
            current = i
    result = [current]
    for i in range(len(rhos)):
        if i != current and rhos[i] == rhos[current]:
            result.append(i)
    return ",".join([str(i + 1) for i in result])


def normalized_float_latex(f_num: float):
    def normalize():
        if f_num == 0:
            return 0, 0
        # Определяем порядок (степень 10)
        e = int(math.floor(math.log10(abs(f_num))))

        # Вычисляем мантиссу
        m = f_num / (10 ** e)

        return m, e

    mantissa, exponent = normalize()
    mantissa = round(float(mantissa), 4)
    if exponent == 0:
        result = f"{mantissa}"
    else:
        result = f"{mantissa} \\cdot 10^{{ {exponent} }}"
    return result


def generate_probabilities_table_data(probabilities_indices, probabilities):
    def probability_name_latex(index):
        return f"P_{{ {index} }}"
    result = []
    for i in range(len(probabilities)):
        result.append([
            latex2omml(probability_name_latex(probabilities_indices[i])),
            latex2omml(normalized_float_latex(probabilities[i]))
        ])
    return result

def states_num_latex(states_num, N, M):
    return f"\\left| S\\left( {N},{M} \\right) \\right| = \\mathrm{{C}}_{{ {N+M-1} }}^{{ {M-1} }} = {states_num}"

class ClosedQTSystemDocumentTemplate(DocumentTemplate):
    def __init__(self, template_path: Path):
        super().__init__(template_path)

    def fill_input(self, picture_path: Path):
        self._fill_text(key="variant", text=f"{data.variant}")
        self._fill_formula(key="transmission_matrix", formula_latex=sp.latex(sp.Matrix(data.transmission_matrix)))
        for i in range(len(data.nodes)):
            self._fill_text(key=f"node_{i + 1}_channel_count", text=f"{data.nodes[i].channels_count}")
        for i in range(len(data.nodes)):
            self._fill_formula(key=f"mu_{i + 1}", formula_latex=f"{data.nodes[i].mu}")
        self._fill_picture(key="graph", picture_path=picture_path)

    def fill_solution(self, solver: ClosedQSSystemSolver):
        for i in range(len(solver.equations)):
            self._fill_formula(key=f"eq_{i + 1}", formula_latex=sp.latex(solver.equations[i]))
        for i in range(len(solver.omegas)):
            self._fill_formula(key=f"omega_{i + 1}", formula_latex=sp.latex(solver.omegas[i]))
        for i in range(len(solver.properties)):
            prop = solver.properties[i]
            self._fill_formula(key=f"j_{i + 1}", formula_latex=normalized_float_latex(prop.j))
            self._fill_formula(key=f"n_{i + 1}", formula_latex=normalized_float_latex(prop.n_o))
            self._fill_formula(key=f"t_sys_{i + 1}", formula_latex=normalized_float_latex(prop.t_sys))
            self._fill_formula(key=f"t_wait_{i + 1}", formula_latex=normalized_float_latex(prop.t_wait))

        self._fill_formula(key=f"j_total", formula_latex=normalized_float_latex(solver.total_property.j))
        self._fill_formula(key=f"n_total", formula_latex=normalized_float_latex(solver.total_property.n_o))
        self._fill_formula(key=f"t_wait_total", formula_latex=normalized_float_latex(solver.total_property.t_wait))
        self._fill_formula(key=f"t_sys_total", formula_latex=normalized_float_latex(solver.total_property.t_sys))
        self._fill_formula(key="states_num", formula_latex=states_num_latex(
            states_num=len(solver.probabilities),
            N=data.requests_number,
            M=4
        ))
        self._fill_table(
            key="state_probabilities_table",
            table_data=generate_probabilities_table_data(solver.probabilities_indices, solver.probabilities)
        )
