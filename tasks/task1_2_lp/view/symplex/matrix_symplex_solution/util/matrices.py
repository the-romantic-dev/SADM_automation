from sympy import Matrix, Rational

from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution


def P(current_solution: BasisSolution) -> Matrix:
    A = current_solution.lp_problem.canonical_form.matrices[0]
    basis = list(current_solution.basis)
    return Matrix(A[:, basis])


def P_inv(current_solution: BasisSolution) -> Matrix:
    return P(current_solution).inv()


def CTB(current_solution: BasisSolution) -> Matrix:
    coeffs = current_solution.lp_problem.canonical_form.matrices[-1]
    vector = Matrix([coeffs[i] for i in current_solution.basis]).T
    return vector


def A_column(current_solution: BasisSolution, var_index: int) -> Matrix:
    return current_solution.lp_problem.canonical_form.matrices[0].col(var_index)


def C_element(current_solution: BasisSolution, var_index: int) -> float | int | Rational:
    return current_solution.lp_problem.canonical_form.matrices[2][var_index, 0]


def b(current_solution: BasisSolution):
    return current_solution.lp_problem.canonical_form.matrices[1]


def Z(current_solution: BasisSolution, var_index: int) -> Matrix:
    return P_inv(current_solution) * A_column(current_solution, var_index)
