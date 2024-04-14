from pathlib import Path

import tasks.qt_systems.closed_systems.data as data
from tasks.qt_systems.closed_systems.closed_qt_system_document_template import ClosedQTSystemDocumentTemplate
from tasks.qt_systems.closed_systems.solver import ClosedQSSystemSolver
from tasks.qt_systems.graph_drawer import GraphDrawer

if __name__ == '__main__':
    closed_system_solver = ClosedQSSystemSolver()
    graph_drawer = GraphDrawer(
        nodes=[i + 1 for i, _ in enumerate(data.nodes)],
        transmission_matrix=data.transmission_matrix,
        nodes_distance=1,
    )
    graph_drawer.show()
    picture_path = Path(data.working_directory, "graph_2.png")
    graph_drawer.save(path=picture_path)
    template_path = Path(Path.cwd().parent, "templates", "closed_system_template.docx")
    document_template = ClosedQTSystemDocumentTemplate(template_path)

    document_template.fill_input(picture_path)
    document_template.fill_solution(closed_system_solver)

    document_template.save(data.working_directory, document_name="output_2.docx")
