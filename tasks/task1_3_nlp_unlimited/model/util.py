import hashlib
import random

from sympy import Rational, Matrix, Eq, solve, sign

from tasks.task1_3_nlp_unlimited.model.nlp_objective import NLPObjective


def start_X(objective: NLPObjective, hash_string: str) -> tuple[Rational, Rational]:
    hash_obj = hashlib.sha256(hash_string.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    random.seed(hash_int)
    random_x1 = random.randint(10, 20) * random.choice([1, -1])
    random_x2 = random.randint(10, 20) * random.choice([1, -1])
    opt_X = solution_matrix(objective).T.tolist()[0]

    return Rational(int(opt_X[0] * sign(random_x1) + random_x1)), Rational(int(opt_X[0] * sign(random_x2) + random_x2))


def solution_matrix(objective: NLPObjective) -> Matrix:
    grad = objective.grad()
    equations = (Eq(grad[0], 0), Eq(grad[1], 0))
    solution = solve(equations, objective.variables)
    return Matrix([solution[x] for x in objective.variables])
