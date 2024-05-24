from pulp import LpVariable, LpProblem, LpMinimize, PULP_CBC_CMD

all_edges = [
    (1, 2, 8), (1, 4, 7), (1, 5, 7), (1, 3, 6), (1, 6, 6),
    (2, 3, 7),
    (3, 6, 5), (3, 7, 4),
    (4, 5, 7),
    (5, 7, 5), (5, 8, 9),
    (6, 7, 9), (6, 8, 5),
    (7, 8, 9),
    (8, 9, 9)
]


def _generate_variables():
    result = {}
    for edge in all_edges:
        i, j, _ = edge
        t_var = LpVariable(name=f"t_{i}{j}", lowBound=0, cat="Integer")
        result[edge] = t_var
    nodes = set([edge[0] for edge in all_edges] + [edge[1] for edge in all_edges])
    last_node = max(nodes)
    result[(last_node, last_node)] = LpVariable(name=f"T", lowBound=0, cat="Integer")
    return result


def _generate_constraints(variables):
    result = []
    nodes = set([edge[0] for edge in all_edges] + [edge[1] for edge in all_edges])
    in_edges = lambda node: [edge for edge in all_edges if edge[1] == node]
    out_edges = lambda node: [edge for edge in all_edges if edge[0] == node]
    for node in nodes:
        for out_edge in out_edges(node):
            for in_edge in in_edges(node):
                result.append(variables[out_edge] >= variables[in_edge] + in_edge[2])
    for in_edge in in_edges(max(nodes)):
        result.append(variables[(max(nodes), max(nodes))] >= variables[in_edge] + in_edge[2])
    return result


def get_model():
    variables = _generate_variables()
    objective = sum(variables.values())
    constraints = _generate_constraints(variables)
    return variables, objective, constraints


def solve_model():
    problem = LpProblem(name="Найти наиболее ранние моменты начала работ", sense=LpMinimize)

    variables, objective, constraints = get_model()

    problem += objective
    for c in constraints:
        problem += c

    problem.solve(PULP_CBC_CMD(msg=False))

    result = []
    for var in variables:
        result.append(
            (variables[var], variables[var].value())
        )
    return result


print(solve_model())
