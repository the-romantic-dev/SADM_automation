from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model.methods import IterativeMethod


class ConjugateGradientMethod(IterativeMethod):
    def step_direction(self, point: Matrix, prev_point: Matrix | None, step_num: int) -> Matrix:
        grad = Matrix(self.objective.grad(point))
        if step_num == 0:
            return grad
        else:
            prev_grad = Matrix(self.objective.grad(prev_point))
            coeff = (grad.norm() ** 2 / prev_grad.norm() ** 2)
            return grad + coeff * prev_grad
