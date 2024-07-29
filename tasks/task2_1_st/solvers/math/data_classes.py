from dataclasses import dataclass


@dataclass
class BaseConstraintData:
    i: int
    j: int
    l: int
    weight_li: int


@dataclass
class VariableSolutionData:
    i: int
    j: int
    value: float | int
    name: str

    def __str__(self):
        return f"{self.name}_{self.i}{self.j} = {self.value}"


@dataclass
class BinaryVariableSolutionData:
    task_1: (int, int)
    task_2: (int, int)
    value: float | int
    name: str = "y"

    def __str__(self):
        return f"{self.name}_{self.task_1[0]}{self.task_1[1]}__{self.task_2[0]}{self.task_2[1]} = {self.value}"
