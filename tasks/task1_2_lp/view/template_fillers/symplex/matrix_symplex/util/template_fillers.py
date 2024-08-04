from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.non_opt_part_tf import NonOptPartTF
from tasks.task1_2_lp.view.template_fillers.symplex.matrix_symplex.opt_part_tf import OptPartTF
from tasks.task1_2_lp.view.template_fillers.symplex.util.step_data import SymplexStepData
from tasks.task1_2_lp.local_definitions import TASK_DIR
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution

TEMPLATES_DIR = Path(TASK_DIR, "_templates/sabonis/matrix_symplex/")


def _opt_template(current_solution: BasisSolution) -> DocumentTemplate:
    if current_solution.is_opt:
        template_path = Path(TEMPLATES_DIR, "opt_part.docx")
    else:
        template_path = Path(TEMPLATES_DIR, "non_opt_part.docx")
    template = DocumentTemplate(template_path)
    return template


def opt_tf(step_data: SymplexStepData):
    template = _opt_template(step_data.current_solution)
    if step_data.current_solution.is_opt:
        tf = OptPartTF(template, step_data)
    else:
        tf = NonOptPartTF(template, step_data)
    return tf
