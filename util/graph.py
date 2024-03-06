from igraph import Graph, Vertex
from .common import remove_dict_keys


class GraphFacade:
    def __init__(self, graph: Graph):
        self.graph = graph

    def get_last_node(self):
        return max(self.graph.vs['name'])

    def get_all_nodes_names(self):
        return self.graph.vs['name']

    def get_edge_weight(self, start_node, end_node, by_name=True):
        if by_name:
            start_node = self.get_index_by_name(start_node)
            end_node = self.get_index_by_name(end_node)

        edge = self.graph.get_eid(start_node, end_node, directed=True)
        if edge != -1:
            return self.graph.es[edge].attributes()['weight']
        else:
            raise Exception(f"get_edge_weight(): Не существует ребра c индексами ({start_node}, {end_node})")

    def get_index_by_name(self, name):
        return self.graph.vs.find(name=name).index

    def get_node_name(self, index: int):
        return self.graph.vs['name'][index]

    def get_nodes_names(self, indices: list[int]) -> list:
        names = self.graph.vs['name']
        result = []
        for i in indices:
            result.append(names[i])
        return result

    def get_incoming_nodes(self, node: Vertex | int) -> list:
        if isinstance(node, int):
            node = self.graph.vs.find(name=node)
        return self.graph.neighbors(node.index, mode='in')

    def get_outcoming_nodes(self, node: Vertex | int):
        if isinstance(node, int):
            node = self.graph.vs.find(name=node)
        return self.graph.neighbors(node.index, mode="out")

    def get_all_edges_names(self):
        result = []
        for edge in self.graph.es:
            result.append((self.get_node_name(edge.source), self.get_node_name(edge.target)))
        return result

    def get_all_outcoming_nodes_names_dict(self):
        return self._get_all_neighbors_nodes_names_dict(mode="out")

    def get_all_incoming_nodes_names_dict(self):
        return self._get_all_neighbors_nodes_names_dict(mode="in")

    def _get_all_neighbors_nodes_names_dict(self, mode):
        result = {}
        nodes = self.graph.vs
        for node in nodes:
            if mode == "in":
                neighbors = self.get_incoming_nodes(node)
            else:
                neighbors = self.get_outcoming_nodes(node)
            neighbors_names = self.get_nodes_names(neighbors)
            result[node["name"]] = neighbors_names
        return result

    def get_levels(self):
        incoming_nodes_names_dict = self.get_all_incoming_nodes_names_dict()
        first_set = list(filter(lambda x: len(incoming_nodes_names_dict[x]) == 0, incoming_nodes_names_dict))
        vertices_sets = [first_set]
        remove_dict_keys(incoming_nodes_names_dict, first_set)
        while len(incoming_nodes_names_dict.keys()) != 0:
            flatten_sets = [item for sublist in vertices_sets for item in sublist]
            next_set = list(filter(lambda x: all(vert in flatten_sets for vert in incoming_nodes_names_dict[x]),
                                   incoming_nodes_names_dict.keys()))
            vertices_sets.append(next_set)
            remove_dict_keys(incoming_nodes_names_dict, next_set)
        return vertices_sets
