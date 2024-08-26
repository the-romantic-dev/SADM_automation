from pathlib import Path
from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model import NLPObjective
from tasks.task1_3_nlp_unlimited.model.methods import RelaxationMethod
from tasks.task1_3_nlp_unlimited.view.methods.method.method_tf import MethodTF
from tasks.teacher import Teacher

description_path = Path(Path(__file__).parent, "relaxation_method_description.docx")


class RelaxationMethodTF(MethodTF):
    def __init__(self, objective: NLPObjective, start_point: Matrix, teacher: Teacher):
        method = RelaxationMethod(objective)
        is_step_univariate = False
        if teacher == Teacher.SIDNEV:
            is_step_univariate = True
        super().__init__(method, start_point, description_path, is_step_univariate=is_step_univariate)
