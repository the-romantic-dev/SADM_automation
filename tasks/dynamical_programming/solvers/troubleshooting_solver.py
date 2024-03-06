from typing import List
from itertools import combinations
import matplotlib.pyplot as plt
from igraph import Graph, plot
from matplotlib.axes import Axes


def is_all_equal(elements: list):
    for i in range(1, len(elements)):
        if elements[i] != elements[i - 1]:
            return False
    return True


def _split_r_by_test(r, test):
    set_tested = list(filter(lambda elem: test[elem - 1], r))
    set_not_tested = list(filter(lambda elem: not test[elem - 1], r))
    return set_tested, set_not_tested


def is_graph_complete(set_tested, set_not_tested):
    if len(set_tested) > 1 or set_not_tested > 1:
        return False
    return True

def find_comb(combs, r):
    for c in combs:
        if c[0] == tuple(r):
            return c
    raise ValueError(f'No such R={r} in combs={combs}')
class TroubleshootingSolver:
    def __init__(self, st: List[List[bool]], c: List[int], p: List[float]):
        self.p = p
        self.c = c
        self.st = st

    def get_test_graph(self, graph: Graph, r, combs, parent_vertex=None, is_tested=None, test_num=None):
        name = ",".join([f"S{i}" for i in r])
        # if len(graph.vs) == 0:
        vertex = graph.add_vertex(name)
        if parent_vertex is not None:
            if is_tested:
                label = f"1 (T{test_num})"
            else:
                label = f"0 (T{test_num})"
            graph.add_edge(parent_vertex, vertex, label=label)
        if len(r) == 1:
            return r

        solution = find_comb(combs, r)
        test_num = solution[2]
        test = self.get_test_by_num(test_num)
        set_tested, set_not_tested = _split_r_by_test(r, test)
        # tested_name = ",".join([f"S{i}" for i in self.get_test_graph(graph, set_tested, combs)])
        self.get_test_graph(graph, set_tested, combs, vertex, is_tested=True, test_num=test_num)
        # tested_vertex = graph.add_vertex(tested_name)
        # graph.add_edge(source=parent_vertex, target=tested_vertex)
        # graph.add_vertex(",".join([f"S{i}" for i in self.get_test_graph(graph, set_not_tested, combs)]))
        self.get_test_graph(graph, set_not_tested, combs, vertex, is_tested=False, test_num=test_num)
        return r

    def _prepare_plot(self, graph: Graph):
        layout = graph.layout("tree")
        visual_style = {
            "vertex_size": 120,
            "vertex_color": "pink",
            "vertex_label": graph.vs['name'],
            "layout": layout,
            "edge_arrow_width": 10,
            "edge_arrow_size": 10,
            "edge_width": 1,
            "edge_label": graph.es["label"]

        }
        fig, ax = plt.subplots()
        ax: Axes = ax
        plot(graph, target=ax, margin=0, **visual_style)
        return plt, fig

    def get_optimal_average_losses_combinations_data(self, vars_num):
        result = []
        for i in range(1, vars_num):
            test_combinations = combinations([j + 1 for j in range(vars_num)], i + 1)
            for comb in test_combinations:
                losses = self.get_optimal_average_losses(comb)
                result.append(
                    [comb, losses[0], losses[1]]
                )
        return result

    def get_optimal_average_losses(self, r: List[int]):
        if len(r) == 1:
            return 0, None
        test_variants = self._get_test_variants(r)
        average_losses_variants = {}
        diff_tests = []
        for i in range(len(test_variants)):
            test = test_variants[i]
            if not is_all_equal(test):
                diff_tests.append(i + 1)
                average_losses_variants[i + 1] = self.c[i] + self._get_summary_previous_average_losses(r=r, test=test)
        min_average_loss = 2 ** 64
        min_average_loss_test = -1
        for key in average_losses_variants.keys():
            variant = average_losses_variants[key]
            if variant < min_average_loss:
                min_average_loss_test = key
                min_average_loss = variant
        return min_average_loss, min_average_loss_test

    def _get_summary_previous_average_losses(self, r: List[int], test: List[bool]):
        set_tested = list(filter(lambda elem: test[r.index(elem)], r))
        set_not_tested = list(filter(lambda elem: not test[r.index(elem)], r))
        r_probability = sum([self.p[i - 1] for i in r])
        tested_probability = sum([self.p[i - 1] for i in set_tested])
        not_tested_probability = sum([self.p[i - 1] for i in set_not_tested])
        p1 = tested_probability / r_probability
        f1 = self.get_optimal_average_losses(set_tested)[0]
        p2 = not_tested_probability / r_probability
        f2 = self.get_optimal_average_losses(set_not_tested)[0]
        return round(p1 * f1 + p2 * f2, 1)

    def _get_test_variants(self, r: List[int]):
        result = [[] for i in self.st[0]]
        for i in r:
            row = self.st[i - 1]
            for j in range(len(row)):
                result[j].append(row[j])
        return result

    def get_test_by_num(self, num):
        result = []
        for row in self.st:
            result.append(row[num - 1])
        return result
