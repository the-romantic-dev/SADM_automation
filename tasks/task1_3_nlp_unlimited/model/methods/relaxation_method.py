from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model.methods import IterativeMethod


class RelaxationMethod(IterativeMethod):

    def step_direction(self, point: Matrix, prev_point: Matrix | None, step_num: int) -> Matrix:
        grad = self.objective.grad(point)
        result = Matrix([grad[0], 0])
        if step_num % 2 != 0:
            result = Matrix([0, grad[1]])
        return result
