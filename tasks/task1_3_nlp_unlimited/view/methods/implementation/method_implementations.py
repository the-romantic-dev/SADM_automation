from pathlib import Path
from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model import NLPObjective
from tasks.task1_3_nlp_unlimited.model.methods import RelaxationMethod, RapidAscentMethod, ConjugateGradientMethod, \
    BroydenMethod, NewtonMethod, DFPMethod
from tasks.task1_3_nlp_unlimited.view.methods.abstract.method_tf import MethodTF
from tasks.teacher import Teacher


class RelaxationMethodTF(MethodTF):
    def __init__(self, objective: NLPObjective, start_point: Matrix, is_step_univariate: bool):
        method = RelaxationMethod(objective)
        # is_step_univariate = False
        # if teacher == Teacher.SIDNEV:
        #     is_step_univariate = True
        description_path = Path(Path(__file__).parent, "descriptions/relaxation_method_description.docx")
        super().__init__(method, start_point, description_path, is_step_univariate=is_step_univariate)


class RapidAscentMethodTF(MethodTF):
    def __init__(self, objective: NLPObjective, start_point: Matrix, is_step_univariate: bool):
        method = RapidAscentMethod(objective)
        # is_step_univariate = False
        # if teacher == Teacher.SIDNEV:
        #     is_step_univariate = True
        description_path = Path(Path(__file__).parent, "descriptions/rapid_ascent_method_description.docx")
        super().__init__(method, start_point, description_path, is_step_univariate=is_step_univariate)


class ConjugateGradientMethodTF(MethodTF):
    def __init__(self, objective: NLPObjective, start_point: Matrix, is_step_univariate: bool):
        method = ConjugateGradientMethod(objective)
        # is_step_univariate = False
        # if teacher == Teacher.SIDNEV:
        #     is_step_univariate = True
        description_path = Path(Path(__file__).parent, "descriptions/conjugate_gradient_method_description.docx")
        super().__init__(method, start_point, description_path, is_step_univariate=is_step_univariate)


class BroydenMethodTF(MethodTF):
    def __init__(self, objective: NLPObjective, start_point: Matrix, is_step_univariate: bool):
        method = BroydenMethod(objective)
        # is_step_univariate = False
        # if teacher == Teacher.SIDNEV:
        #     is_step_univariate = True
        description_path = Path(Path(__file__).parent, "descriptions/broyden_method_description.docx")
        super().__init__(method, start_point, description_path, is_step_univariate=is_step_univariate)


class DFPMethodTF(MethodTF):
    def __init__(self, objective: NLPObjective, start_point: Matrix, is_step_univariate: bool):
        method = DFPMethod(objective)
        # is_step_univariate = False
        # if teacher == Teacher.SIDNEV:
        #     is_step_univariate = True
        description_path = Path(Path(__file__).parent, "descriptions/dfp_method_description.docx")
        super().__init__(method, start_point, description_path, is_step_univariate=is_step_univariate)


class NewtonMethodTF(MethodTF):
    def __init__(self, objective: NLPObjective, start_point: Matrix):
        method = NewtonMethod(objective)
        description_path = Path(Path(__file__).parent, "descriptions/newton_method_description.docx")
        super().__init__(method, start_point, description_path, is_step_univariate=False)
