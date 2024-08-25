from abc import abstractmethod, ABC

from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model import NLPObjective
from tasks.task1_3_nlp_unlimited.model.methods.abstract.iterative_method import IterativeMethod


class QuasiNewtonianMethod(IterativeMethod, ABC):
    def __init__(self, objective: NLPObjective):
        super().__init__(objective)
        self.prev_inv_gesse_approximation = -Matrix.eye(2, 2)

    def step_direction(self, point: Matrix, prev_point: Matrix | None, step_num: int) -> Matrix:
        def delta_inv_gesse_approximation():
            if step_num == 0:
                return self.prev_inv_gesse_approximation
            point_delta = point - prev_point
            grad = Matrix(self.objective.grad(point))
            prev_grad = Matrix(self.objective.grad(prev_point))
            grad_delta = grad - prev_grad

            Y = self.step_correction(point_delta, grad_delta)
            Z = self.gradient_correction(point_delta, grad_delta)

            A = point_delta * Y.T / (Y.T * grad_delta)[0, 0]
            B = self.prev_inv_gesse_approximation * grad_delta * Z.T / (Z.T * grad_delta)[0, 0]
            return A - B

        approx = self.prev_inv_gesse_approximation + delta_inv_gesse_approximation()
        self.prev_inv_gesse_approximation = approx
        return -approx * Matrix(self.objective.grad(point))

    @abstractmethod
    def step_correction(self, point_delta: Matrix, grad_delta: Matrix):
        ...

    @abstractmethod
    def gradient_correction(self, point_delta: Matrix, grad_delta: Matrix):
        ...
