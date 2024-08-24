from time import time
from typing import Callable

from tasks.task1_2_lp.env import report_path
from tasks.task1_2_lp.view.main.lp_problem_tf import LPProblemTF
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.teacher import Teacher


def lpp_main(teacher: Teacher, problem: LPProblem, variant: int, callback: Callable):
    start_time = time()

    template_filler = LPProblemTF(variant=variant, lpp=problem, teacher=teacher)
    template_filler.fill()

    end_time = time()
    template_filler.save(report_path, add_pdf=False)

    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")
    callback()
