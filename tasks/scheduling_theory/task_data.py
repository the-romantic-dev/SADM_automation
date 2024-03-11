from pathlib import Path

from igraph import Graph

from tasks.scheduling_theory.scheduling_data import SchedulingData
from tasks.scheduling_theory.solvers.scheduling_problem.rule import RuleType
from util.graph import GraphFacade

graph_edges = [
    (1, 2, 7), (1, 3, 7), (1, 5, 4),
    (2, 4, 7), (2, 5, 4),
    (3, 5, 5),
    (4, 7, 5),
    (5, 7, 4), (5, 6, 7),
    (6, 7, 7), (6, 8, 6), (6, 9, 7),
    (7, 8, 7), (7, 9, 3),
    (8, 9, 3)
]
variant = 3

is_sidnev = True

folder = Path(r"C:\Labs\САПР\Заказы\Довлатов")

graph_img_path = Path(folder, "graph_img.png")

chart_folder = Path(Path.cwd(), "img")

chart_filename = "gantt_chart.png"
performers_number = 2

intensity_limit = 0.75

standard_deviation = 0.05

overtime_limit = 0.1

# time_limit_probability_percent = 18

rule_types = [RuleType.MIN_RESERVE, RuleType.MAX_DURATION, RuleType.MIN_RESERVE]

graph: Graph = Graph.TupleList(directed=True, edges=graph_edges, weights=True)
graph_facade: GraphFacade = GraphFacade(graph)
scheduling_data: SchedulingData = SchedulingData(
    graph_facade=graph_facade,
    performers_number=performers_number,
    rule_types=rule_types,
    overtime_limit=overtime_limit,
    # time_limit_probability_percent=time_limit_probability_percent,
    standard_deviation=standard_deviation,
    intensity_limit=intensity_limit
)
