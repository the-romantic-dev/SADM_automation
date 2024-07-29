import math

from tasks.task2_4_qt_sys.closed_systems.data import Node

nodes = [
    Node(channels_count=1, mu=40),
    Node(channels_count=1, mu=70),
    Node(channels_count=1, mu=120),
    Node(channels_count=1, mu=130)
]


def generate_probabilities_indices(n, length, current_sum=0, current_index=[], result=[]):
    if length == 0:
        if current_sum == n:
            result.append(tuple(current_index))
        return

    for num in range(n - current_sum + 1):
        generate_probabilities_indices(n, length - 1, current_sum + num, [*current_index, num], result)

    return result


def calculate_probabilities(probabilities_indices: list[tuple], omegas: list):
    total = sum([state_z(n, omegas) for n in probabilities_indices])
    result = [float(state_z(n, omegas) / total) for n in probabilities_indices]
    return result


def state_z(n: tuple, omegas: list):
    requests_per_node = n
    result = math.prod([z_i(i=i, n_i=requests_per_node[i], omegas=omegas) for i in range(len(requests_per_node))])
    return result


def mu_i(i, k):
    return nodes[i].mu * min(k, nodes[i].channels_count)


def z_i(i, n_i, omegas):
    if n_i == 0:
        return 1
    result = 1
    result *= omegas[i] ** n_i
    result /= math.prod([mu_i(i, k) for k in range(1, n_i + 1)])
    return result


indices = generate_probabilities_indices(n=15, length=4)
probabilities = calculate_probabilities(probabilities_indices=indices, omegas=[0.25, 0.25, 0.25, 0.25])

prob_sum = 0
for i in range(len(indices)):
    if indices[i][0] == 0:
        prob_sum += probabilities[i]
        print(f"{indices[i]} = {probabilities[i]}")
print(prob_sum)