from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model.methods.abstract.quasi_newtonian_method import QuasiNewtonianMethod


class BroydenMethod(QuasiNewtonianMethod):
    def step_correction(self, point_delta: Matrix, grad_delta: Matrix):
        return point_delta - self.prev_inv_gesse_approximation * grad_delta

    def gradient_correction(self, point_delta: Matrix, grad_delta: Matrix):
        return self.step_correction(point_delta, grad_delta)
