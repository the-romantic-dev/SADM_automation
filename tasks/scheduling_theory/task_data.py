import json

from igraph import Graph
import config
from tasks.scheduling_theory.scheduling_data import SchedulingData
from tasks.scheduling_theory.solvers.scheduling_problem.rule import RuleType
from util.graph import GraphFacade

# Загружаем данные из JSON-файла
with open(f'{config.folder.as_posix()}/data.json', 'r') as file:
    data = json.load(file)

# Извлекаем данные из словаря
graph_edges = [(edge[0], edge[1], edge[2]) for edge in data['graph_edges']]
variant = data['variant']
is_sidnev = data['is_sidnev']
performers_number = data['performers_number']
intensity_limit = data['intensity_limit'] if data['intensity_limit'] is not None else 0.75
standard_deviation = data['standard_deviation'] if data['standard_deviation'] is not None else 0.05
overtime_limit = data['overtime_limit'] if data['overtime_limit'] is not None else 0.1
rule_types = [RuleType[rule] for rule in data['rule_types']]
# folder = Path(r"D:\Убежище\Университет\6 семестр\САПР\1\Сабонис\Кузичева")
#
# graph_img_path = Path(folder, "graph_img.png")
#
# chart_folder = Path(Path.cwd(), "img")
#
# chart_filename = "gantt_chart.png"
# performers_number = 2
#
# intensity_limit = 0.8
#
# standard_deviation = 0.05
#
# overtime_limit = 0.12

# rule_types = [RuleType.MAX_DURATION, RuleType.MIN_DURATION, RuleType.MIN_RESERVE]

graph: Graph = Graph.TupleList(directed=True, edges=graph_edges, weights=True)
graph_facade: GraphFacade = GraphFacade(graph)
scheduling_data: SchedulingData = SchedulingData(
    graph_facade=graph_facade,
    performers_number=performers_number,
    rule_types=rule_types,
    overtime_limit=overtime_limit,
    standard_deviation=standard_deviation,
    intensity_limit=intensity_limit
)
