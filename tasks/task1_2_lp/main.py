from pathlib import Path
from time import time

from sympy import Rational

from report.model.template.document_template import DocumentTemplate
from tasks.task1_2_lp.view.template_fillers.lp_problem_tf import LPProblemTF
from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.enums.objective_type import ObjectiveType
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective

if __name__ == '__main__':
    template_path = Path("_templates/sabonis/main/lp_problem.docx")
    document_template = DocumentTemplate(template_path)

    start_time = time()

    problem = LPProblem(
        constraints=[
            Constraint(coeffs=[Rational(1), Rational("0.3")], const=Rational("10.2")),
            Constraint(coeffs=[Rational(-1), Rational("0.4")], const=Rational("-1.2"))
        ],
        objective=Objective(ObjectiveType.MAX, coeffs=[Rational(1), Rational(-2)])
    )
    template_filler = LPProblemTF(variant=4, lp_problem=problem, template=document_template)
    template_filler.fill()

    end_time = time()

    save_path = Path(r"C:\Projects\test")
    template_filler.save(save_path, add_pdf=False)

    print(f"Общее время выполнения: {end_time - start_time} секунд")

