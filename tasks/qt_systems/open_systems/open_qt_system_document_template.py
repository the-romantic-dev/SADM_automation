import math
from pathlib import Path
from sympy.core.numbers import NaN
import numpy as np

import tasks.qt_systems.open_systems.data as data
import sympy as sp
from report.docx.objects.document_template import DocumentTemplate
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


def property_latex(prop: float):
    if isinstance(prop, NaN):
        return "\\infty"

    def normalize():
        if prop == 0:
            return 0, 0
        # Определяем порядок (степень 10)
        e = int(math.floor(math.log10(abs(prop))))

        # Вычисляем мантиссу
        m = prop / (10 ** e)

        return m, e

    mantissa, exponent = normalize()
    mantissa = round(float(mantissa), 4)
    if exponent == 0:
        result = f"{mantissa}"
    else:
        result = f"{mantissa} \\cdot 10^{{ {exponent} }}"
    return result


class OpenQTSystemDocumentTemplate(DocumentTemplate):
    def __init__(self, template_path: Path):
        super().__init__(template_path)

    def fill_input(self, picture_path: Path):
        self._fill_text(key="variant", text=f"{data.variant}")
        self._fill_formula(key="lambda_0", formula_latex=f"{float(data.lambda_0)}")
        self._fill_formula(key="transmission_matrix", formula_latex=sp.latex(sp.Matrix(data.transmission_matrix)))
        for i in range(len(data.nodes)):
            self._fill_text(key=f"node_{i + 1}_channel_count", text=f"{data.nodes[i].channels_count}")
        for i in range(len(data.nodes)):
            self._fill_formula(key=f"mu_{i + 1}", formula_latex=f"{data.nodes[i].mu}")
        self._fill_picture(key="graph", picture_path=picture_path)

    def fill_solution(self, solver: OpenQSSystemSolver):
        for i in range(len(solver.equations)):
            self._fill_formula(key=f"eq_{i + 1}", formula_latex=sp.latex(solver.equations[i]))
        for i in range(len(solver.lambdas)):
            self._fill_formula(key=f"lambda_{i + 1}", formula_latex=sp.latex(solver.lambdas[i]))
        for i in range(len(solver.alphas)):
            self._fill_formula(key=f"alpha_{i + 1}", formula_latex=sp.latex(solver.alphas[i]))
        self._fill_formula(key=f"min_eq", formula_latex=min_latex(solver.coefficients))
        self._fill_text(key="condition_verdict", text=verdict_text(solver.coefficients))
        for i in range(len(solver.rhos)):
            self._fill_formula(key=f"rho_{i + 1}", formula_latex=sp.latex(solver.rhos[i]))
        self._fill_text(key="min_rho_node", text=min_rho_node(solver.rhos))
        self._fill_text(key="max_rho_node", text=max_rho_node(solver.rhos))
        for i in range(len(solver.properties)):
            prop = solver.properties[i]
            self._fill_formula(key=f"j_{i + 1}", formula_latex=property_latex(prop.j))
            self._fill_formula(key=f"n_{i + 1}", formula_latex=property_latex(prop.n_o))
            self._fill_formula(key=f"t_sys_{i + 1}", formula_latex=property_latex(prop.t_sys))
            self._fill_formula(key=f"t_wait_{i + 1}", formula_latex=property_latex(prop.t_wait))

        self._fill_formula(key=f"j_total", formula_latex=property_latex(solver.total_property.j))
        self._fill_formula(key=f"n_total", formula_latex=property_latex(solver.total_property.n_o))
        self._fill_formula(key=f"t_wait_total", formula_latex=property_latex(solver.total_property.t_wait))
        self._fill_formula(key=f"t_sys_total", formula_latex=property_latex(solver.total_property.t_sys))
