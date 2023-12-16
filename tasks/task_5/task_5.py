from docx import Document

from solvers.graph_solver import GraphSolver

if __name__ == '__main__':
    edges = [
        (1, 2, 5), (1, 3, 3),
        (2, 7, 15), (2, 6, 5), (2, 5, 17), (2, 3, 3),
        (3, 4, 8), (3, 5, 15), (3, 9, 13),
        (4, 6, 10), (4, 5, 6),
        (5, 7, 3),
        (6, 9, 11), (6, 7, 12),
        (7, 8, 4),
        (8, 9, 1)
    ]
    graph_solver = GraphSolver(edges)
    print(graph_solver.get_vertices_levels())
    print(f"Минмальная длина пути: {graph_solver.get_min_path(1, 9)[0]}")
    print(f"Минимальный путь: {graph_solver.get_min_path(1, 9)[2]}")
    graph_solver.show_graph()

    template = Document('template.docx')