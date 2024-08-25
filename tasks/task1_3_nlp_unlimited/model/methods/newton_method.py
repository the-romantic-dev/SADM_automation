from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model.methods import IterativeMethod


class NewtonMethod(IterativeMethod):
    def step_direction(self, point: Matrix, prev_point: Matrix | None, step_num: int) -> Matrix:
        grad = Matrix(self.objective.grad(point))
        gesse = Matrix(self.objective.gesse())
        return -gesse.inv() * grad

    def step_size(self, point: Matrix, direction: Matrix) -> float:
        return 1
