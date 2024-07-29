from pathlib import Path

from sympy import Rational

from report.model.document_template import DocumentTemplate
from tasks.task1_2_lp.document_template.lp_problem_tf import LPProblemTF
from tasks.task1_2_lp.models.constraint.constraint import Constraint
from tasks.task1_2_lp.models.enums.objective_type import ObjectiveType
from tasks.task1_2_lp.models.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.models.objective.objective import Objective

if __name__ == '__main__':
    problem = LPProblem(
        constraints=[
            Constraint(coefs=[Rational(1), Rational(2)], const=Rational("5.3")),
            Constraint(coefs=[Rational(-1), Rational(2)], const=Rational("2.8"))
        ],
        objective=Objective(ObjectiveType.MAX, coefs=[Rational(1), Rational(1)])
    )

    template_path = Path("templates/sabonis/main/lp_problem.docx")
    document_template = DocumentTemplate(template_path)
    template_filler = LPProblemTF(variant=4, lp_problem=problem, template=document_template)
    template_filler.fill()

    save_path = Path(r"D:\Desktop\test")
    template_filler.save(save_path, add_pdf=False)


