from pathlib import Path

from igraph import Graph

from tasks.scheduling_theory.scheduling_data import SchedulingData
from tasks.scheduling_theory.solvers.scheduling_problem.rule import RuleType
from util.graph import GraphFacade

graph_edges = [
    (1, 2, 18), (1, 3, 8), (1, 4, 14),
    (2, 7, 15),
    (3, 6, 12), (3, 9, 1),
    (4, 5, 11), (4, 6, 5), (4, 8, 16),
    (5, 6, 16),
    (6, 7, 10), (6, 9, 19),
    (7, 8, 9),
    (8, 9, 7)
]
variant = 83

is_sidnev = False

folder = Path(r"D:\Убежище\Университет\6 семестр\САПР\1\Сабонис\Шамаро")

graph_img_path = Path(folder, "graph_img.png")

chart_folder = Path(Path.cwd(), "img")

chart_filename = "gantt_chart.png"
performers_number = 2

intensity_limit = 0.6

standard_deviation = 0.05

overtime_limit = 0.16

# time_limit_probability_percent = 18

rule_types = [RuleType.MIN_DURATION, RuleType.MAX_DURATION, RuleType.MIN_RESERVE]

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
