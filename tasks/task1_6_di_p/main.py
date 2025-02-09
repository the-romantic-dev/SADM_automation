from copy import deepcopy
from pathlib import Path

from tasks.task1_6_di_p.tsp.model.solver import TSPSolver

from tasks.task1_6_di_p.tsp.view.main.main_tf import MainTF
if __name__ == "__main__":
    variant = "2.1, 5.14"
    task_table = [
        [r"\infty", 31, 15, 19, 8, 55],
        [19, r"\infty", 22, 31, 7, 35],
        [25, 43, r"\infty", 53, 57, 16],
        [5, 50, 49, r"\infty", 39, 9],
        [24, 24, 33, 5, r"\infty", 14],
        [34, 26, 6, 3, 36, r"\infty"],
    ]

    tsp_solver = TSPSolver(list_matrix=deepcopy(task_table))
    report_data = []
    tsp_solver.solve_min(report_data=report_data)

    tf = MainTF(variant=variant, task_table=task_table, solution_data=report_data)
    tf.fill()
    tf.template.save(Path(r"D:\Desktop\test"), add_pdf=False)



    #
    # result_doc: DocumentType = Document()
    # last_step = len(report_data) - 1
    # for step, data in enumerate(report_data):
    #     if data.tree_level == -1:
    #         tsp_filler = TSPZeroStepDocxFiller(step_report_data=data)
    #         step: DocumentType = Document("tsp/zero_step.docx")
    #     elif step != last_step:
    #         tsp_filler = TSPStepDocxFiller(step_report_data=data, step_number=step)
    #         step: DocumentType = Document("tsp/step.docx")
    #     else:
    #         tsp_filler = TSPLastStepDocxFiller(step_report_data=data, step_number=step)
    #         step: DocumentType = Document("tsp/last_step.docx")
    #     paragraph = result_doc.add_paragraph("{{step}}")
    #     fill_template(template=step, data_producers=tsp_filler.get_data_producers())
    #     fill_paragraph_template(paragraph, data_producers={"step": lambda: step})
    #
    # result_doc.save("tsp.docx")
