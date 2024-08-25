from abc import ABC, abstractmethod

from sympy import Matrix

from tasks.task1_3_nlp_unlimited.model import NLPObjective
from tasks.task1_3_nlp_unlimited.model.dataclasses.solution_step import SolutionStep


class IterativeMethod(ABC):
    def __init__(self, objective: NLPObjective):
        self.objective = objective

    def is_stop(self, point: Matrix):
        grad = self.objective.grad(point)
        tol = 1e-1
        return Matrix(grad).norm() <= tol

    def solution_step(self, point: Matrix) -> SolutionStep:
        return SolutionStep(
            x1=point[0, 0],
            x2=point[1, 0],
            value=self.objective.value(point)
        )

    def solve(self, start_point: Matrix) -> list[SolutionStep]:
        point = start_point
        step_num = 0
        direction = self.step_direction(point, None, step_num)
        size = self.step_size(point, direction)
        result = [self.solution_step(point)]
        while not self.is_stop(point):
            step_num += 1
            next_point = point + size * direction
            result.append(self.solution_step(point))
            direction = self.step_direction(next_point, point, step_num)
            size = self.step_size(next_point, direction)
            point = next_point

        return result

    @abstractmethod
    def step_direction(self, point: Matrix, prev_point: Matrix | None, step_num: int) -> Matrix:
        ...

    def step_size(self, point: Matrix, direction: Matrix) -> float:
        grad = Matrix(self.objective.grad(point))
        gesse = Matrix(self.objective.gesse())
        a = (grad.T * direction)[0, 0]
        b = (direction.T * gesse * direction)[0, 0]
        result = -a / b
        return result
