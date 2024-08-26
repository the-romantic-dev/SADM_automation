from sympy import Rational

from tasks.task1_3_nlp_unlimited.env import report_path
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective
from tasks.task1_3_nlp_unlimited.view.main.main_tf import MainTF
from tasks.teacher import Teacher

if __name__ == '__main__':
    objective = NLPObjective(coeffs=[
        Rational(-14), Rational(-26), Rational(16), Rational(84), Rational(252)
    ])
    tf = MainTF(teacher=Teacher.SIDNEV, variant=4, objective=objective, nickname="TheRomantic20")
    tf.fill()

    tf.template.save(report_path, add_pdf=False)
