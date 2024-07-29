from tasks.task2_1_st.solvers.scheduling_problem.rule import RuleType
from util.graph import GraphFacade


class SchedulingData:
    def __init__(self, graph_facade, performers_number, rule_types: list[RuleType], overtime_limit,
                 standard_deviation: float, intensity_limit):
        self._graph_facade: GraphFacade = graph_facade
        self.performers_number = performers_number
        self.overtime_limit = overtime_limit
        self.rule_types: list[RuleType] = rule_types
        # self.time_limit_probability_percent = time_limit_probability_percent
        self.graph_levels = self._graph_facade.get_levels()
        self.last_node = self._graph_facade.get_last_node()
        self.nodes = sorted(list(self._graph_facade.get_all_nodes_names()))
        self.edges_num = len(self.get_edges())
        self.standard_deviation = standard_deviation
        self.intensity_limit = intensity_limit

    def get_edge_weight(self, edge: tuple[int, int]):
        return self._graph_facade.get_edge_weight(start_node=edge[0], end_node=edge[1], by_name=True)

    def get_node_level(self, node):
        for i in range(len(self.graph_levels)):
            level = self.graph_levels[i]
            if node in level:
                return i + 1
        raise ValueError("Невозможно определить уровень узла. Нет такого узла в графе.")

    def get_edges(self):
        return self._graph_facade.get_all_edges_names()

    def get_incoming_nodes(self, node):
        return self._graph_facade.get_nodes_names(self._graph_facade.get_incoming_nodes(node))

    def get_outcoming_nodes(self, node):
        return self._graph_facade.get_nodes_names(self._graph_facade.get_outcoming_nodes(node))
