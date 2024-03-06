"""Формирует отчет метода сопряженных градиентов"""

from sympy import Rational
import reports.iteration_methods_reports.iteration_report as iteration_report
from other.const import expr
from methods.iteration_methods.conjugate_gradient import ConjugateGradientMethod

def report(start):
    """Формирует отчет метода сопряженных градиентов"""
    method = ConjugateGradientMethod(start, expr)
    iteration_report.report(
        header="МЕТОД СОПРЯЖЕННЫХ ГРАДИЕНТОВ",
        method_obj=method,
        plot_name="Метод сопряженных градиентов",
        file="conjugate_gradient"
    )
