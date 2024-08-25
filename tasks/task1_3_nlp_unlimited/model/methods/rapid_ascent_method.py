from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model.methods import IterativeMethod


class RapidAscentMethod(IterativeMethod):
    def step_direction(self, point: Matrix, prev_point: Matrix | None, step_num: int) -> Matrix:
        return Matrix(self.objective.grad(point))
