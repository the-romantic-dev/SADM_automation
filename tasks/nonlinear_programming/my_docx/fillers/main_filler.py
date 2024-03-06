from my_docx.docx_output import latex2omml, sympy2omml
from my_docx.latex_helper import latex_limit, latex_expr_degree_decision
from task import Task
from util import gradient, gesse


def _create_lim1():
    return latex2omml(latex_limit(Task.lim1234[0], lim_type='le'))


def _create_lim2():
    return latex2omml(latex_limit(Task.lim1234[1], lim_type='le'))


def _create_lim3():
    return latex2omml(latex_limit(Task.lim1234[2], lim_type='le'))


def _create_lim4():
    return latex2omml(latex_limit(Task.lim1234[3], lim_type='le'))


def _create_lim5():
    return latex2omml(latex_limit(Task.lim5, lim_type='eq'))


def _create_lim6():
    return latex2omml(latex_limit(Task.lim67[0], lim_type='le'))


def _create_lim7():
    try:
        return latex2omml(latex_limit(Task.lim67[1], lim_type='le'))
    except IndexError:
        return ''


def _create_mainfunction():
    return latex2omml(latex_expr_degree_decision(Task.f))


def _create_grad():
    return sympy2omml(gradient())


def _create_gesse():
    return sympy2omml(gesse())


main_data_producers = {
    'mainfunction': _create_mainfunction,
    'lim1': _create_lim1,
    'lim2': _create_lim2,
    'lim3': _create_lim3,
    'lim4': _create_lim4,
    'lim5': _create_lim5,
    'lim6': _create_lim6,
    'lim7': _create_lim7,
    'grad': _create_grad,
    'gesse': _create_gesse
}
