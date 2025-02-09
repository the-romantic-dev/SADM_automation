from graphviz import Digraph
import os

from tasks.task1_6_di_p.tsp.model.report_dataclasses import TSPReportData, TSPReportDataMinimal, TSPReportDataLast

os.environ["PATH"] += os.pathsep + r'D:\Apps\Graphviz-12.2.1-win64\bin'


# def build_graph(solution_data: list):
#     dot = Digraph(format='png')  # Инициализируем направленный граф
#
#     for i, step in enumerate(solution_data):
#         node_id = f"Step_{i + 1}"
#         evaluation = getattr(step, 'previous_evaluation', 'N/A')  # Значение оценочной функции
#         dot.node(node_id, label=f"V = {evaluation}")
#         # Определяем родителя (если это не корневой узел)
#         if step.tree_level >= 0:
#             parent_id = f"Step_{i}"  # Узел-родитель
#             # Метка ребра (путь, который добавляется или исключается)
#             paths_way = getattr(step, 'paths_way', [])
#             if paths_way:
#                 last_path, is_included = paths_way[-1]  # Последний добавленный/исключенный путь
#                 edge_label = f"{'Include' if is_included else 'Exclude'}: {last_path}"
#             else:
#                 edge_label = "No Path"
#
#             # Добавляем ребро с меткой
#             dot.edge(parent_id, node_id, label=edge_label)
#     dot.render('branch_and_bound_graph', view=True)

def build_graph(solution_data: list):
    dot = Digraph(format='png', graph_attr={'rankdir': 'TB'})  # Инициализируем направленный граф
    dot.attr(splines='false')
    last_V = None
    is_last = isinstance(solution_data[-1], TSPReportDataLast)
    for i in range(1, len(solution_data)):
        if i == len(solution_data) - 1 and is_last:
            break
        step = solution_data[i]
        # paths_way = [((path[0] + 1, path[0] + 1), is_include) for path, is_include in step.paths_way]
        curr_node = f"{step.paths_way}"

        next_path = (step.worst_tau[0][0], step.worst_tau[0][1])
        include_node = f"{step.paths_way + [(next_path, True)]}"
        exclude_node = f"{step.paths_way + [(next_path, False)]}"

        dot.node(curr_node, label=f"V = {step.previous_evaluation}")
        dot.node(include_node, label=f"V = {step.include_evaluation}")
        dot.node(exclude_node, label=f"V = {step.exclude_evaluation}")

        last_V = min(step.include_evaluation, step.exclude_evaluation)
        dot.edge(curr_node, include_node, label=f"+ {(next_path[0] + 1, next_path[1] + 1)}", minlen='2')
        dot.edge(curr_node, exclude_node, label=f"- {(next_path[0] + 1, next_path[1] + 1)}", minlen='2')

    # path_way = solution_data[-1].paths_way
    if is_last:
        last_step = solution_data[-1]
        two_last_nodes = last_step.result_path[-2:]
        # path_way += [(two_last_nodes[0], True), (two_last_nodes[1], True)]

        curr = f"{last_step.paths_way}"
        first = f"{last_step.paths_way + [(two_last_nodes[0], True)]}"
        second = f"{last_step.paths_way + [(two_last_nodes[1], True)]}"
        dot.node(first, f'V = {last_V}')
        dot.node(second, f'V = {last_V}')
        dot.edge(curr, first, f'+ {(two_last_nodes[0][0] + 1, two_last_nodes[0][1] + 1)}')
        dot.edge(first, second, f'+ {(two_last_nodes[1][0] + 1, two_last_nodes[1][1] + 1)}')
    return dot
    # dot.render('branch_and_bound_graph', view=True)


    # tree = Digraph(format='png', graph_attr={'rankdir': 'TB'})  # TB = сверху вниз
    # zero_step: TSPReportDataMinimal = solution_data[0]
    #
    # tree.node(f"root", f"V = {sum(zero_step.h_terms)}")
    # parent = "root"
    # for i in range(1, len(solution_data)):
    #     current_include = f"{parent} + {}"
    #     current_exclude = f"{parent} + {}"
    #     tree.node()
    #     node, _ = step_data.paths_way[i]
    #     tree.node(f"{node}")
    #     print(node, is_excluded)

# tree = Digraph(format='png', graph_attr={'rankdir': 'TB'})  # TB = сверху вниз
#
# # Добавляем узлы
# tree.node("1", "Root")
# tree.node("2", "Child 1")
# tree.node("3", "Child 2")
# tree.node("4", "Grandchild 1")
# tree.node("5", "Grandchild 2")

# Добавляем связи

# Добавляем рёбра с подписями
# tree.edge("1", "2", label="(1, 2)")
# tree.edge("1", "3", label="Edge 1-3")
# tree.edge("2", "4", label="Edge 2-4")
# tree.edge("2", "5", label="Edge 2-5")

# Визуализация
# tree.render("tree", view=True)  # Сохранить и открыть файл
