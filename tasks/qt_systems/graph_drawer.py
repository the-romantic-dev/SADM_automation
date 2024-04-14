import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from netgraph import Graph
from sympy import Rational


def generate_nodes_positions(nodes, nodes_distance):
    return {i: (1 + i * nodes_distance, 1) for i, _ in enumerate(nodes)}


def build_curved_edge(start: tuple, end: tuple, direction: int, steps: int):
    x1, y1 = start
    x2, y2 = end

    # Середина отрезка
    xc = (x1 + x2) / 2
    yc = (y1 + y2) / 2

    # Радиус
    radius = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 2

    # Начальный и конечный угол (в радианах)
    if direction > 0:
        start_angle = 0
        end_angle = math.pi
    elif direction < 0:
        start_angle = math.pi
        end_angle = 2 * math.pi
    else:
        start_angle = 0
        end_angle = 2 * math.pi

    # Шаг угла (в радианах)
    angle_step = math.pi / steps

    # Генерация точек
    points = []
    angle = start_angle
    while angle <= end_angle:
        x = xc + radius * math.cos(angle)
        y = yc + radius * math.sin(angle)
        points.append((x, y))
        angle += angle_step

    return points


def split_edges(edges):
    loop_edges = []
    for edge in edges:
        if edge[0] == edge[1]:
            loop_edges.append(edge)
    solo_edges = []
    for edge in edges:
        if (edge[1], edge[0]) not in solo_edges and abs(edge[0] - edge[1]) == 1:
            solo_edges.append(edge)
        elif (edge[1], edge[0]) in solo_edges:
            solo_edges.remove((edge[1], edge[0]))

    parallel_edges = [edge for edge in edges if edge not in solo_edges and edge not in loop_edges]
    return loop_edges, solo_edges, parallel_edges


def build_loop_edge_path(node_pos, node_distance):
    end_pos = (node_pos[0] - 0.5 * node_distance, node_pos[1])
    return np.array(
        build_curved_edge(start=node_pos, end=end_pos, direction=0, steps=180)
    )


def build_solo_edge_path(start_node_pos, end_node_pos):
    return np.array([start_node_pos, end_node_pos])


def build_parallel_edge_path(start_node_pos, end_node_pos, steps, direction):
    distance = abs(start_node_pos[0] - end_node_pos[0])
    points_per_distance = 180
    path = build_curved_edge(start_node_pos, end_node_pos, direction=direction, steps=points_per_distance * steps)
    # Обработка странного бага. В Netgraph проверяется соответствие координат пути (а, b) и (b, a)
    # я так понимаю это нужно для обработки параллельных граней. Но там нет проверки на несоответствие размерностей
    # этих путей. Так что я ручками подгоняю длину последовательностей
    if len(path) == points_per_distance * steps:
        path.append(path[-1])
    return np.array(
        path
    )


def generate_edges_paths(edges, nodes_positions, node_distance):
    loop_edges, solo_edges, parallel_edges = split_edges(edges)
    result = {}
    for edge in loop_edges:
        node_pos = nodes_positions[edge[0]]
        result[edge] = build_loop_edge_path(node_pos, node_distance)
    for edge in solo_edges:
        start_node_pos = nodes_positions[edge[0]]
        end_node_pos = nodes_positions[edge[1]]
        result[edge] = build_solo_edge_path(start_node_pos, end_node_pos)
    for edge in parallel_edges:
        start_node_pos = nodes_positions[edge[0]]
        end_node_pos = nodes_positions[edge[1]]
        steps = abs(edge[0] - edge[1])
        direction = np.sign(edge[0] - edge[1])
        result[edge] = build_parallel_edge_path(start_node_pos, end_node_pos, steps, direction)
    return result


def transmission_matrix_to_edges(transmission_matrix: list[list[Rational]]):
    result = {}
    for i, row in enumerate(transmission_matrix):
        for j, elem in enumerate(row):
            result[(i, j)] = str(elem)
    result = {k: v for k, v in result.items() if v != '0'}
    return result


class GraphDrawer:
    def __init__(self, nodes: list, transmission_matrix: list[list[Rational]], nodes_distance):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        nodes_positions = generate_nodes_positions(nodes, nodes_distance)
        nodes_names = {i: name for i, name in enumerate(nodes)}
        edges_names = transmission_matrix_to_edges(transmission_matrix)
        edges_paths = generate_edges_paths(edges_names, nodes_positions, nodes_distance)
        self.graph = Graph(
            list(edges_names.keys()), edge_width=4, arrows=True,
            edge_layout=edges_paths,
            node_labels=nodes_names,
            edge_labels=edges_names,
            edge_alpha=1,
            node_layout=nodes_positions,
            node_size=16,
            edge_label_rotate=False,
            edge_label_fontdict=dict(size=16),
            node_label_fontdict=dict(size=16),
            ax=self.ax
        )

    def show(self):
        plt.show()

    def save(self, path: Path):
        self.fig.canvas.draw()
        self.fig.savefig(path.as_posix(), dpi=300)
