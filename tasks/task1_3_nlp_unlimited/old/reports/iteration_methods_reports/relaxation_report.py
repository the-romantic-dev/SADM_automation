"""Формирует отчет метода релаксации"""

from sympy import Rational
import reports.iteration_methods_reports.iteration_report as iteration_report
from other.const import expr
from methods.iteration_methods.relaxation import RelaxationMethod

def report(start):
    """Формирует отчет метода релаксации"""
    iteration_report.report(
        header="РЕЛАКСАЦИОННЫЙ МЕТОД",
        method_obj=RelaxationMethod(start, expr),
        plot_name="Метод релаксации",
        file="relaxation"
    )
