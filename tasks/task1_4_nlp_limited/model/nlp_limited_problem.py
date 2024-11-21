from tasks.task1_3_nlp_unlimited.model import NLPObjective
from tasks.task1_4_nlp_limited.model.nlp_constraints import NLPConstraint


class NLPLimitedProblem:
    def __init__(self, objective: NLPObjective, constraints: list[NLPConstraint]):
        self.objective = objective
        self.constraints = constraints

