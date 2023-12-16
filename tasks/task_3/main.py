"""Главный файл"""
from sympy import pretty, Matrix, Rational
from reports import analytic_report
from reports.iteration_methods_reports import relaxation_report
from reports.iteration_methods_reports import rapid_ascent_report
from reports.iteration_methods_reports import newton_report
from reports.iteration_methods_reports import conjugate_gradient_report
from reports.iteration_methods_reports import broiden_report
from reports.iteration_methods_reports import dfp_report

import other.my_io as io
from other.const import x1, x2, expr

io.clear_output()
analytic_report.report()
start = [Rational(-12), Rational(13)]
io.output("\n-----НАЧАЛЬНЫЕ ДАННЫЕ-----\n")
io.output("Начальная точка:")
io.output(f"{pretty(Matrix(start))}\n")
io.output("Значение функции в начальной точке:")
io.output(f"{round(float(expr.subs({x1: start[0], x2: start[1]})), 3)}\n")
rapid_ascent_report.report(start)
newton_report.report(start)
conjugate_gradient_report.report(start)
relaxation_report.report(start)
broiden_report.report(start)
dfp_report.report(start)
