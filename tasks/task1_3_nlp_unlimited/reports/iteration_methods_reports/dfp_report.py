"""Формирует отчет метода Дэвида-Флетчера-Пауэла"""

from sympy import Rational
import reports.iteration_methods_reports.iteration_report as iteration_report
from other.const import expr
from methods.iteration_methods.quasi_newtonian_methods.dfp import DFPMethod

def report(start):
    """Формирует отчет метода Дэвидена-Флетчера-Пауэла"""
    
    method = DFPMethod(start, expr)
    iteration_report.report(
        header="МЕТОД Дэвидена-Флетчера-Пауэла",
        method_obj=method,
        plot_name="Метод Дэвидена-Флетчера-Пауэла",
        file="dfp"
    )