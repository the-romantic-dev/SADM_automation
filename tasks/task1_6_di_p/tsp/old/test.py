def build_cycle_order(edges):
    graph = {}
    for edge in edges:
        if edge[0] not in graph:
            graph[edge[0]] = edge[1]

    cycle_order = []

    def dfs(node):
        while graph[node]:
            next_node = graph[node].pop()
            dfs(next_node)
        cycle_order.append(node)

    # Начнем с любой вершины (можно выбрать первую из списка ребер)
    start_node = edges[0][0]
    dfs(start_node)

    # Результат будет в обратном порядке, так как мы добавляем вершины в конец списка
    cycle_order.reverse()

    return cycle_order


edges = [(1, 2), (4, 5), (5, 1), (2, 6)]
cycle_order = build_cycle_order(edges)

print("Порядок соединения вершин в цикле:", cycle_order)
