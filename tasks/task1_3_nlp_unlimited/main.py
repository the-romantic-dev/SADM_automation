from sympy import Rational

from tasks.task1_3_nlp_unlimited.env import report_path
from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective
from tasks.task1_3_nlp_unlimited.model.util import UnivariateMethod
from tasks.task1_3_nlp_unlimited.view.main.main_tf import MainTF
from tasks.teacher import Teacher


def nlp_unlimited_main(teacher: Teacher, objective: NLPObjective, variant: int,
                       start_X: tuple[int, int], univariate_method: UnivariateMethod):
    # objective = NLPObjective(coeffs=[
    #     Rational(-14), Rational(-26), Rational(16), Rational(84), Rational(252)
    # ])
    tf = MainTF(teacher=teacher, variant=variant, objective=objective,
                start_X=(Rational(start_X[0]), Rational(start_X[1])), univariate_method=univariate_method)
    tf.fill()

    tf.template.save(report_path, add_pdf=False)
