"""Формирует отчет метода наискорейшего подъема"""

from sympy import Rational
import reports.iteration_methods_reports.iteration_report as iteration_report
from other.const import expr
from methods.iteration_methods.rapid_ascent import RapidAscentMethod

def report(start):
    """Формирует отчет метода наискорейшего подъема"""
    rapid_ascent_method = RapidAscentMethod(start, expr)
    iteration_report.report(
        header="МЕТОД НАИСКОРЕЙШЕГО ПОДЪЕМА",
        method_obj=rapid_ascent_method,
        plot_name="Метод наискорейшего подъема",
        file="rapid_ascent"
    )
