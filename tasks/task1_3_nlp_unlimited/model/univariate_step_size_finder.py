from math import sqrt

from sympy import Matrix
from tasks.task1_3_nlp_unlimited.model import NLPObjective

golden_section = (1 + sqrt(5)) / 2


class UnivariateStepSizeFinder:
    def __init__(self, objective: NLPObjective, point: Matrix, direction: Matrix):
        self.point = point
        self.objective = objective
        self.direction = direction

    def f(self, t):
        next_point = self.point + t * self.direction
        return self.objective.value(next_point)

    @property
    def start_interval_steps(self) -> list[float]:
        t0 = 0
        t1 = 1
        t2 = t1 + golden_section * (t1 - t0)

        f0 = self.f(t0)
        f1 = self.f(t1)
        f2 = self.f(t2)
        result = [t0, t1, t2]
        while f1 <= f2:
            t0 = t1
            t1 = t2
            t2 = t1 + golden_section * (t1 - t0)
            result.append(t2)
            f1 = f2
            f2 = self.f(t2)
        return result

    def golden_section_method_steps(self, start_interval: tuple[float, float]) -> list[tuple[float, float]]:
        tol = 1e-3

        def step(interval):
            a, b = interval
            delta = (b - a) / golden_section
            x1 = b - delta
            x2 = a + delta
            f1 = self.f(x1)
            f2 = self.f(x2)
            if f1 <= f2:
                a = x1
            else:
                b = x2
            return a, b

        steps = []
        curr_interval = start_interval
        steps.append(curr_interval)
        while abs(curr_interval[0] - curr_interval[1]) >= tol:
            curr_interval = step(curr_interval)
            steps.append(curr_interval)
        return steps
