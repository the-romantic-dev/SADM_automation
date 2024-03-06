from tasks.scheduling_theory.scheduling_data import SchedulingData


class ReservesCalculator:

    def __init__(self, min_moments, max_moments, scheduling_data: SchedulingData):
        self.min_moments = min_moments
        self.max_moments = max_moments
        self.scheduling_data: SchedulingData = scheduling_data
        self.full_reserves = self._full_reserves()

    def _full_reserves(self):
        result = {}
        edges = self.scheduling_data.get_edges()
        for edge in edges:
            result[edge] = self.calc_full_reserve(edge[0], edge[1])
        return result

    def calc_full_reserve(self, i, j):
        t_j = self.max_moments[j]
        t_i = self.min_moments[i]
        edge = (i, j)
        weight = self.scheduling_data.get_edge_weight(edge)
        return t_j - (t_i + weight)

    def calc_independent_reserve_I(self, j):
        t_max = self.max_moments[j]
        t_min = self.min_moments[j]
        return t_max - t_min

    def calc_independent_reserve_II(self, i, j):
        t_j = self.min_moments[j]
        t_i = self.max_moments[i]
        edge = (i, j)
        weight = self.scheduling_data.get_edge_weight(edge)
        return t_j - (t_i + weight)

    def calc_free_reserve(self, i, j):
        t_j = self.min_moments[j]
        t_i = self.min_moments[i]
        edge = (i, j)
        weight = self.scheduling_data.get_edge_weight(edge)
        return t_j - (t_i + weight)

    def calc_critical_paths(self) -> list[list]:

        def dfs(current_path: list, current_node: int):
            if current_node == last_node:
                result.append(current_path.copy())
                return

            neighbors = self.scheduling_data.get_outcoming_nodes(current_node)
            for next_node in neighbors:
                edge = (current_node, next_node)
                if self.full_reserves[edge] == 0 and next_node not in current_path:
                    dfs(current_path + [next_node], next_node)

        result = []
        last_node = self.scheduling_data.last_node
        dfs(current_path=[1], current_node=1)
        return result
