from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model.methods import QuasiNewtonianMethod


class DFPMethod(QuasiNewtonianMethod):
    def step_correction(self, point_delta: Matrix, grad_delta: Matrix):
        return point_delta

    def gradient_correction(self, point_delta: Matrix, grad_delta: Matrix):
        return self.prev_inv_gesse_approximation * grad_delta
