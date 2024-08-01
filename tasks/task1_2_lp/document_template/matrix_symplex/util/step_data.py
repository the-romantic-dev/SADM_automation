from tasks.task1_2_lp.models.basis_solution.basis_solution import BasisSolution


def basis_different(basis_1, basis_2):
    for i in range(len(basis_1)):
        if basis_1[i] != basis_2[i]:
            return basis_1[i], basis_2[i]
    return None


class MatrixSymplexStepData:
    def __init__(self, current_solution: BasisSolution, current_index: int, next_solution: BasisSolution):
        self.current_solution = current_solution
        self.current_index = current_index
        self.next_solution = next_solution

    @property
    def out_var(self):
        return basis_different(self.current_solution.basis, self.next_solution.basis)[0]

    @property
    def in_var(self):
        return basis_different(self.current_solution.basis, self.next_solution.basis)[1]
