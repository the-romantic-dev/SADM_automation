import math

from tasks.task2_1_st.scheduling_data import SchedulingData
from tasks.task2_1_st.solvers.moments.reserves_calculator import ReservesCalculator


def Phi(x):
    from scipy.special import erf
    return round(erf(x / 2 ** 0.5) / 2, 5)


class ProbabilisticModelSolver:
    def __init__(self, scheduling_data: SchedulingData, reserves_calculator: ReservesCalculator):
        self.scheduling_data = scheduling_data
        self.critical_paths = reserves_calculator.calc_critical_paths()
        self.critical_paths_weights = [
            [self.scheduling_data.get_edge_weight((path[i], path[i + 1])) for i in range(len(path) - 1)]
            for path in self.critical_paths
        ]

    def average_edge_weight(self):
        return round(sum(self.critical_paths_weights[0]) / len(self.critical_paths_weights[0]), 3)

    def average_deviation(self):
        average = self.average_edge_weight()
        return round(average * self.scheduling_data.standard_deviation, 3)

    def expected_value(self):
        return [sum(path) for path in self.critical_paths_weights]

    def dispersion(self):
        def term(square_path): return round(sum(square_path) * self.scheduling_data.standard_deviation ** 2, 5)
        squares = [[elem ** 2 for elem in path] for path in self.critical_paths_weights]
        return [term(square_path) for square_path in squares]

    def epsilon(self):
        return round(self.expected_value()[0] * self.scheduling_data.overtime_limit, 5)

    def not_overtime_probability(self, path_index):
        epsilon = self.epsilon()
        D = self.dispersion()[path_index]
        result = round(0.5 + Phi(epsilon / math.sqrt(D)), 5)
        if result == 1.0:
            result = 0.99999
        return result


    def result_not_overtime_probability(self):
        result = 1
        for i in range(len(self.critical_paths)):
            result *= self.not_overtime_probability(i)
        result = round(result, 5)
        if result == 1.0:
            result = 0.99999
        return result
