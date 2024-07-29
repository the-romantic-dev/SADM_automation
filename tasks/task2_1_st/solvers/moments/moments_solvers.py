from pulp import LpVariable, LpProblem, LpMinimize, LpMaximize, PULP_CBC_CMD

from tasks.task2_1_st.scheduling_data import SchedulingData


class DynamicalMomentsSolver:
    def __init__(self, scheduling_data: SchedulingData):
        self.scheduling_data = scheduling_data

        levels = self.scheduling_data.graph_levels
        self.min_calculation_data = {}
        self.min_moments = self._calc_min_moments(levels, self.min_calculation_data)
        self.total_time = self.min_moments[scheduling_data.last_node]
        self.max_calculation_data = {}
        self.max_moments = self._calc_max_moments(levels, self.max_calculation_data)


    def _calc_max_moments(self, levels: list[list], calculation_data: dict):
        def min_of_outcoming(node: int):
            outcoming_nodes = self.scheduling_data.get_outcoming_nodes(node)
            variants = []
            weights = []
            for i_node in outcoming_nodes:
                edge = (node, i_node)
                weight = self.scheduling_data.get_edge_weight(edge)
                weights.append(weight)
                variants.append(result[i_node] - weight)

            moment = min(variants, default=self.min_moments[node])
            calculation_data[node] = {
                "outcoming_nodes": outcoming_nodes,
                "weights": weights,
                "variants": variants,
                "result": moment
            }
            return moment

        result = {}
        for lvl in reversed(levels):
            for node in lvl:
                result[node] = min_of_outcoming(node)
        return result

    def _calc_min_moments(self, levels: list[list], calculation_data: dict):
        def max_of_incoming(node: int):
            incoming_nodes = self.scheduling_data.get_incoming_nodes(node)

            variants = []
            weights = []
            for i_node in incoming_nodes:
                edge = (i_node, node)
                weight = self.scheduling_data.get_edge_weight(edge)
                weights.append(weight)
                variants.append(result[i_node] + weight)

            moment = max(variants, default=0)
            calculation_data[node] = {
                "incoming_nodes": incoming_nodes,
                "weights": weights,
                "variants": variants,
                "result": moment
            }
            return moment

        result = {}
        for lvl in levels:
            for node in lvl:
                result[node] = max_of_incoming(node)
        return result


class MathMomentsSolver:
    def __init__(self, scheduling_data: SchedulingData):
        self.scheduling_data = scheduling_data
        self.min_moments = self._calc_math_moments(is_min=True)
        self.max_moments = self._calc_math_moments(is_min=False)

    def _calc_math_moments(self, is_min=True):
        if is_min:
            problem = LpProblem(name="Найти наиболее ранние моменты начала работ", sense=LpMinimize)
        else:
            problem = LpProblem(name="Найти наиболее поздние моменты начала работ", sense=LpMaximize)

        def generate_variables():
            result = {}
            nodes = self.scheduling_data.nodes
            for node in nodes:
                v = LpVariable(name=f"t_{node}", lowBound=0, cat="Integer")
                result[node] = v
            return result

        def generate_objective():
            return sum(variables.values())

        def generate_constraints():
            result = []
            edges = self.scheduling_data.get_edges()
            for j, i in edges:
                t_i = variables[i]
                t_j = variables[j]
                edge = (j, i)
                weight = self.scheduling_data.get_edge_weight(edge)
                if is_min:
                    constraint = t_i >= t_j + weight
                else:
                    constraint = t_j <= t_i - weight
                result.append(constraint)
            if is_min:
                t_1 = variables[1]
                result.append(t_1 == 0)
            else:
                M = self.scheduling_data.last_node
                t_M = variables[M]
                result.append(t_M == self.min_moments[M])
            return result

        variables = generate_variables()
        objective = generate_objective()
        constraints = generate_constraints()

        problem += objective
        for c in constraints:
            problem += c

        problem.solve(PULP_CBC_CMD(msg=False))

        result = {}
        for var in variables:
            result[var] = variables[var].value()
        return result

