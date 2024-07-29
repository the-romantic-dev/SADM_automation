from typing import List
import matplotlib.pyplot as plt

from igraph import Graph, plot, Vertex
from matplotlib.axes import Axes


def _index_to_name(index: int, graph: Graph):
    return graph.vs['name'][index]


def _indices_to_names(indices: List[int], graph: Graph) -> List:
    names = graph.vs['name']
    result = []
    for i in indices:
        result.append(names[i])
    return result


def _get_step_by_start(steps: list, start):
    for step in steps:
        if step['start'] == start:
            return step
    raise ValueError(f"Нет шага с началом в узле ({start}) в steps")


def _get_path_from_steps(steps: list, start, end) -> list:
    current_end = start
    result = [start]

    while current_end != end:
        step = _get_step_by_start(steps, current_end)
        result.append(step["opt_out"])
        current_end = step["opt_out"]
    return result


def _find_path(graph: Graph, start: int, end: int, steps: List, is_max=True):
    if start == end:
        return 0
    for data in steps:
        if data["start"] == start:
            return data["opt_path_size"]

    start_index = graph.vs['name'].index(start)
    outs = graph.neighbors(start_index, mode='out')
    if is_max:
        current_path_size = -1
    else:
        current_path_size = 2 ** 64
    current_out = -1
    path_sizes = []
    for o in outs:
        out_name = _index_to_name(o, graph)
        edge_weight = list(graph.es.select(_from=start_index, _to=o)['weight'])[0]
        new_path_size = _find_path(graph, start=out_name, end=end, steps=steps, is_max=is_max) + edge_weight
        path_sizes.append(new_path_size)
        if (is_max and current_path_size < new_path_size) or (not is_max and current_path_size > new_path_size):
            current_path_size = new_path_size
            current_out = out_name
    steps.append({
        "start": start,
        "end": end,
        "outs": _indices_to_names(outs, graph),
        "path_sizes": path_sizes,
        "opt_out": current_out,
        "opt_path_size": current_path_size
    })
    # steps.append(((start, end), _indices_to_names(outs, graph), path_sizes , current_out, current_path_size))
    return current_path_size


def _split_graph(graph: Graph):
    incoming_vertices_dict = {}
    for vertex in graph.vs:
        vertex: Vertex = vertex
        incoming_vertices: list = graph.neighbors(vertex.index, mode='in')
        incoming_vertices = list(map(lambda x: graph.vs['name'][x], incoming_vertices))
        incoming_vertices_dict[vertex["name"]] = incoming_vertices
    first_set = list(filter(lambda x: len(incoming_vertices_dict[x]) == 0, incoming_vertices_dict))
    vertices_sets = [first_set]
    _remove_keys(incoming_vertices_dict, first_set)
    while len(incoming_vertices_dict.keys()) != 0:
        flatten_sets = [item for sublist in vertices_sets for item in sublist]
        next_set = list(filter(lambda x: all(vert in flatten_sets for vert in incoming_vertices_dict[x]),
                               incoming_vertices_dict.keys()))
        vertices_sets.append(next_set)
        _remove_keys(incoming_vertices_dict, next_set)
    return vertices_sets


def _remove_keys(dictionary: dict, keys: list):
    for i in keys:
        dictionary.pop(i)


class GraphSolver:

    def __init__(self, edges):
        self.graph: Graph = Graph.TupleList(directed=True, edges=edges, weights=True)

    def get_min_path(self, start, end):
        """
        Считает минимальный путь на графе

        :returns: (длина пути, шаги решения, путь)

        """
        steps = []
        path_size = _find_path(graph=self.graph, start=start, end=end, steps=steps, is_max=False)
        path = _get_path_from_steps(steps, start, end)
        return path_size, steps, path

    def get_max_path(self, start, end):
        """
        Считает максимальный путь на графе

        :returns: (длина пути, шаги решения, путь)

        """
        steps = []
        path_size = _find_path(graph=self.graph, start=start, end=end, steps=steps, is_max=True)
        path = _get_path_from_steps(steps, start, end)
        return path_size, steps, path

    def get_vertices_levels(self):
        return _split_graph(self.graph)

    def show_graph(self):
        _plt, _ = self._prepare_plot()
        _plt.show()

    def save_graph(self, path: str):
        _, _fig = self._prepare_plot()
        _fig.savefig(path)
    def _prepare_plot(self):
        layout = self.graph.layout("auto")
        visual_style = {
            "vertex_size": 40,
            "vertex_label": self.graph.vs['name'],
            "layout": layout,
            "edge_arrow_width": 10,
            "edge_arrow_size": 10,
            "edge_width": 1,
            "edge_label": self.graph.es["weight"]

        }
        fig, ax = plt.subplots()
        ax: Axes = ax
        plot(self.graph, target=ax, margin=0, **visual_style)
        return plt, fig
