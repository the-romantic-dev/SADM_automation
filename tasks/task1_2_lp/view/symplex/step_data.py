from dataclasses import dataclass

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution


@dataclass
class SymplexStepData:
    current_solution: BasisSolution
    current_index: int
    out_var: int | None
    in_var: int | None
