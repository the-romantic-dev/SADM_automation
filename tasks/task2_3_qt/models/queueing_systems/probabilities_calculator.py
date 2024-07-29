import sympy as sp


def calculate_probabilities(traffic_intensities: list):
    probabilities_names = [f"P{j}" for j in range(len(traffic_intensities) + 1)]
    probabilities_variables = sp.symbols(" ".join(probabilities_names))
    equations = []
    for j in range(1, len(probabilities_variables)):
        equations.append(
            sp.Eq(probabilities_variables[j], probabilities_variables[j - 1] * traffic_intensities[j - 1])
        )
    equations.append(sp.Eq(sum(probabilities_variables), 1))
    solution_dict = sp.solve(equations, dict=True)[0]
    return [solution_dict[variable] for variable in probabilities_variables]
