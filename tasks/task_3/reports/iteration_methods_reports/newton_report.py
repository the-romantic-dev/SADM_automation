"""Формирует отчет метода Ньютона"""

from sympy import Rational
import reports.iteration_methods_reports.iteration_report as iteration_report
from other.const import expr
from methods.iteration_methods.newton import NewtonMethod

def report(start):
    """Формирует отчет метода Ньютона"""
    method = NewtonMethod(start, expr)
    iteration_report.report(
        header="МЕТОД НЬЮТОНА",
        method_obj=method,
        plot_name="Метод Ньютона",
        file="newton"
    )
