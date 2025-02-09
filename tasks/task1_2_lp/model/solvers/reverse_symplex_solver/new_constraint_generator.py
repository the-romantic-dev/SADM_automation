from sympy import Rational, gcd, sqrt, Matrix

from tasks.task1_2_lp.model import BasisSolution, ObjectiveType
from tasks.task1_2_lp.model import Constraint


# def __constraint_value(coeffs, sol):
#     x_values = sol.solution
#     return sum([c * x for c, x in zip(coeffs, x_values)])

# def is_basis_neighbors(basis_1: list[int], basis_2: list[int]) -> bool:
#     """
#     Проверяет, являются ли базисы соседними, т.е. имеют ли общее ограничение
#     :param basis_1: Первый базис
#     :param basis_2: Второй базис
#     :return: True - базисы соседние, иначе False
#     """
#     if len(basis_1) != len(basis_2):
#         return False
#     basis_2 = set(basis_2)
#     diff_count = 0
#     for b1 in basis_1:
#         if b1 in basis_2:
#             diff_count += 1
#         if diff_count > 1:
#             return False
#     return diff_count == 1
def __round_rational_to_decimal(rat: Rational, decimals=0):
    mult = 10 ** decimals
    result = Rational(round(rat * mult), mult)
    return result


def __neighbor_edge_center(var_count: int, opt: BasisSolution, neighbor: BasisSolution):
    opt_value = opt.solution[:var_count]
    neighbor_value = neighbor.solution[:var_count]
    center = [(o + n) / 2 for o, n in zip(opt_value, neighbor_value)]
    return center


def get_neighbor_solutions(curr_sol: BasisSolution, all_solutions: list[BasisSolution]) -> list[BasisSolution]:
    """
    Возвращает все допустимые соседние базисы для текущего
    :param curr_sol: Текущий базис
    :param all_solutions: Все базисы
    :return: Список соседних базисов
    """
    neighbors = []
    constraints = set(curr_sol.active_constraints)
    for sol in all_solutions:
        if curr_sol.is_neighbor(sol) and sol.is_acceptable:
            common_constraint = constraints.intersection(sol.active_constraints)
            if len(common_constraint) > 1:
                raise ValueError('Больше одного пересечения в базисе')
            if len(common_constraint) == 0:
                raise ValueError('Нет пересечений в базисе')
            constraints.remove(list(common_constraint)[0])
            neighbors.append(sol)

    if len(constraints) > 0:
        point = Matrix(curr_sol.solution[:2])
        distance = curr_sol.distance(neighbors[0])
        constraint = list(constraints)[0]
        active = curr_sol.active_constraints
        active.remove(constraint)
        other_constraint = active[0]
        norm = Matrix(other_constraint.norm)
        norm_length = norm.norm()
        unit = norm / norm_length

        def offset(factor=1):
            delta = factor * distance * unit
            return point + unit

        new_point = offset()
        if other_constraint.accept(new_point):
            neighbors.append(new_point)
        else:
            neighbors.append(offset(-1))
    return neighbors


def get_acceptable_and_opt_solutions(solutions: list[BasisSolution]):
    opt_sol = None
    acceptable_sols = []
    for sol in solutions:
        if sol.is_opt:
            opt_sol = sol
        elif sol.is_acceptable:
            acceptable_sols.append(sol)
    return acceptable_sols, opt_sol


def generate_constraint_coeffs(var_count: int):
    result = [Rational(0) for _ in range(var_count)]
    centers = [__neighbor_edge_center(var_count, opt, neigh) for neigh in opt_neighbors]


def __new_coeffs_and_const(var_count: int, opt: BasisSolution, opt_neighbors: list[BasisSolution]):
    if var_count != 2:
        raise ValueError('ПОШЕЛ НАХУЙ, ТОЛЬКО ДЛЯ ПЛОСКОСТИ СТРОИМ ДОП. ОГРАНИЧЕНИЕ')
    new_constraint_coeffs = [Rational(0) for _ in range(var_count)]
    new_constraint_value = Rational(0)

    centers = [__neighbor_edge_center(var_count, opt, neigh) for neigh in opt_neighbors]

    new_constraint_coeffs[0] = Rational(centers[1][1] - centers[0][1])
    new_constraint_coeffs[1] = Rational(centers[0][0] - centers[1][0])
    new_constraint_value = new_constraint_coeffs[0] * centers[0][0] + new_constraint_coeffs[1] * centers[0][1]

    opt_value = new_constraint_coeffs[0] * opt.solution[0] + new_constraint_coeffs[1] * opt.solution[1]

    is_max = True if opt.lp_problem.objective.type == ObjectiveType.MAX else False
    is_opt_less = True if opt_value < new_constraint_value else False

    factor = -1 if (is_max and is_opt_less) or (not is_max and not is_opt_less) else 1

    new_constraint_coeffs[0] *= factor
    new_constraint_coeffs[1] *= factor
    new_constraint_value *= factor
    return new_constraint_coeffs, new_constraint_value


def generate_new_constraint(opt_sol: BasisSolution, solutions: list[BasisSolution]):
    # acceptable_sols, opt_sol = get_acceptable_and_opt_solutions(solutions)
    var_count = opt_sol.lp_problem.var_count
    active_constraints = opt_sol.active_constraints
    neighbors = get_neighbor_solutions(curr_sol=opt_sol, all_solutions=solutions)

    coeffs, const = __new_coeffs_and_const(var_count=var_count, opt=opt_sol, opt_neighbors=neighbors)

    for i, coeff in enumerate(coeffs):
        coeffs[i] = __round_rational_to_decimal(coeff)

    const = __round_rational_to_decimal(const)
    _gcd = gcd([*coeffs, const])

    coeffs = [c / _gcd for c in coeffs]
    const /= _gcd
    if coeffs[0] == 0:
        const = const / coeffs[1]
        coeffs[1] = 1
    elif coeffs[1] == 0:
        const = const / coeffs[0]
        coeffs[0] = 1
    return Constraint(coeffs=coeffs, const=const)
