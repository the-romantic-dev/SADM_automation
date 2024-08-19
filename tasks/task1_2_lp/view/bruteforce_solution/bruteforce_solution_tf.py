from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import elements_list, formula
from tasks.task1_2_lp.model import BasisSolution
from tasks.task1_2_lp.view.bruteforce_solution.bruteforce_step.bruteforce_step_tf import BruteforceStepTF
from tasks.task1_2_lp.view.solution_tf import SolutionTF

template_path = Path(Path(__file__).parent, "bruteforce_solution.docx")


class BruteforceSolutionTF(SolutionTF):
    def __init__(self, all_solutions: list[BasisSolution], opt_solution_index: int):
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.all_solutions = all_solutions
        self.opt_solution_index = opt_solution_index

    @elements_list
    def _fill_solution_steps(self):
        filled_documents = []
        for i, sol in enumerate(self.all_solutions):
            bruteforce_step_tf = BruteforceStepTF(solution_index=i, basis_solution=sol)
            bruteforce_step_tf.fill()
            filled_documents.append(bruteforce_step_tf.template.document)
        return filled_documents

    @formula
    def _fill_result(self):
        return self.result_formula(self.all_solutions[self.opt_solution_index])
