import matplotlib.pyplot as plt
import numpy as np

from netgraph import Graph, ArcDiagram, get_circular_layout, get_curved_edge_paths, get_sugiyama_layout

edges = {
    (1, 2): "1/2",
    (2, 3): "lol"
    # (1, 3): "13/14",
    # (2, 1): "17/18  "
}
nodes_positions = {
    1: (1, 1),
    2: (2, 1),
    3: (3, 1),
}

edges_paths = {
    (1, 2): np.array([(1, 1), (1.5, 1.2), (2, 1)]),
    (2, 3): np.array([(2, 1), (2.5, 1.2), (3, 1)]),
}
# layout_nodes = get_sugiyama_layout(edges=list(edges.keys()))
# layout_edges = get_curved_edge_paths(
#     edges=list(edges.keys()),
#     node_positions=nodes_positions,
#     k=10, selfloop_radius=0.3,
#     bundle_parallel_edges=False,
#     origin=[0, 0],
#     scale=[5, 5]
#
# )
graph = Graph(
    list(edges.keys()), edge_width=2, arrows=True,
    edge_layout=edges_paths,
    node_labels={1 : 'a', 2 : 'b', 3: 'c'},
    edge_labels=edges,
    edge_alpha=1,
    node_layout=nodes_positions,
    node_size=7,
    edge_label_rotate=False,
    edge_label_fontdict=dict(size=16),
    node_label_fontdict=dict(size=16)
)
plt.show()