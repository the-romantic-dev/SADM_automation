from pathlib import Path

from sympy import pretty
import tasks.task2_4_qt_sys.open_systems.data as data
from tasks.task2_4_qt_sys.graph_drawer import GraphDrawer
from tasks.task2_4_qt_sys.open_systems.open_qt_system_document_template import OpenQTSystemDocumentTemplate
from tasks.task2_4_qt_sys.open_systems.solver import OpenQSSystemSolver

if __name__ == '__main__':
    open_system_solver = OpenQSSystemSolver()
    graph_drawer = GraphDrawer(
        nodes=[i for i in range(len(data.nodes) + 1)],
        transmission_matrix=data.transmission_matrix,
        nodes_distance=1
    )
    graph_drawer.show()
    picture_path = Path(data.working_directory, "graph_1.png")
    graph_drawer.save(path=picture_path)

    template_path = Path(Path.cwd(), "../templates", "open_system_template.docx")
    document_template = OpenQTSystemDocumentTemplate(template_path)

    document_template.fill_input(picture_path)
    document_template.fill_solution(open_system_solver)

    document_template.save(data.working_directory, document_name="output_1.docx")
