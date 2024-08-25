# """Главный файл"""
# from sympy import pretty, Matrix, Rational
# from tasks.task1_3_nlp_unlimited.old.reports import analytic_report
# from tasks.task1_3_nlp_unlimited.old.reports import rapid_ascent_report, broiden_report, \
#     dfp_report
# from tasks.task1_3_nlp_unlimited.old.reports.iteration_methods_reports import newton_report, relaxation_report, \
#     conjugate_gradient_report
#
# import tasks.task1_3_nlp_unlimited.old.other.my_io as io
# from tasks.task1_3_nlp_unlimited.old.other import x1, x2, expr
#
# io.clear_output()
# analytic_report.report()
# start = [Rational(-3), Rational(11)]
# io.output("\n-----НАЧАЛЬНЫЕ ДАННЫЕ-----\n")
# io.output("Начальная точка:")
# io.output(f"{pretty(Matrix(start))}\n")
# io.output("Значение функции в начальной точке:")
# io.output(f"{round(float(expr.subs({x1: start[0], x2: start[1]})), 3)}\n")
# rapid_ascent_report.report(start)
# newton_report.report(start)
# conjugate_gradient_report.report(start)
# relaxation_report.report(start)
# broiden_report.report(start)
# dfp_report.report(start)
from sympy import Rational

from tasks.task1_3_nlp_unlimited.env import report_path
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective
from tasks.task1_3_nlp_unlimited.view.main.nlp_unlimited_main_tf import NLPUnlimitedMainTF
from tasks.teacher import Teacher

if __name__ == '__main__':
    objective = NLPObjective(coeffs=[
        Rational(-13), Rational(-22), Rational(12), Rational(30), Rational(40)
    ])
    tf = NLPUnlimitedMainTF(teacher=Teacher.SABONIS, variant=4, objective=objective)
    tf.fill()

    tf.template.save(report_path, add_pdf=False)
