"""Формирует отчет метода Бройдена"""

from sympy import Rational
import reports.iteration_methods_reports.iteration_report as iteration_report
from other.const import expr
from methods.iteration_methods.quasi_newtonian_methods.broiden import BroidenMethod

def report(start):
    """Формирует отчет метода Бройдена"""
    method = BroidenMethod(start, expr)
    iteration_report.report(
        header="МЕТОД БРОЙДЕНА",
        method_obj=method,
        plot_name="Метод Бройдена",
        file="broiden"
    )
