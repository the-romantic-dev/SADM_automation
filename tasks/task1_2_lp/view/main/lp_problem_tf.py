from __future__ import annotations

import os
from pathlib import Path

from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import template_filler
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import root_tf
from tasks.task1_2_lp.model.basis_solution.basis_solution import BasisSolution
from tasks.task1_2_lp.model.solvers.reverse_symplex_solver.new_constraint_generator import generate_new_constraint
from tasks.task1_2_lp.view.auxiliary_task.auxiliary_task_tf import AuxiliaryTaskTF
from tasks.task1_2_lp.view.bruteforce_solution.bruteforce_solution_tf import BruteforceSolutionTF
from tasks.task1_2_lp.view.canonical_problem.canonical_problem_tf import CanonicalProblemTF
from tasks.task1_2_lp.view.conjugate_opt_point_search.cops_search_tf import COPSSearchTF
from tasks.task1_2_lp.view.dual_problem.dual_problem_tf import DualProblemTF
from tasks.task1_2_lp.view.geometric_solution.geometric_solution_tf import GeometricSolutionTF
from tasks.task1_2_lp.view.problem.problem_tf import ProblemTF
from tasks.task1_2_lp.view.reverse_symplex.reverse_symplex_tf import ReverseSymplexTF
from tasks.task1_2_lp.view.symplex.matrix_symplex_solution.matrix_symplex_solution_tf import MatrixSymplexSolutionTF
from tasks.task1_2_lp.model.lp_problem.lp_problem import LPProblem
from tasks.task1_2_lp.model.solvers.bruteforce_solver.bruteforce_solver import BruteforceSolver
from tasks.task1_2_lp.model.solvers.symplex_solver.symplex_solver import SymplexSolver
from tasks.task1_2_lp.view.symplex.table_symplex_solution.modified_task_symplex.modified_symplex_solution_tf import \
    ModifiedSymplexSolutionTF
from tasks.task1_2_lp.view.symplex.table_symplex_solution.table_symplex_solution_tf import TableSymplexSolutionTF
from tasks.task1_2_lp.viewmodel.lp_problem_viewmodel import LPProblemViewModel
from tasks.teacher import Teacher

package_path = Path(os.path.dirname(os.path.abspath(__file__)))
sabonis_template_path = Path(package_path, "sabonis_main.docx")
sidnev_template_path = Path(package_path, "sidnev_main.docx")


@root_tf
class LPProblemTF(TemplateFiller):
    def __init__(self, variant: int, lpp: LPProblem, teacher: Teacher):
        self.variant = variant
        self.teacher = teacher
        self.lpp = lpp
        self.lpp_vm = LPProblemViewModel(lpp)
        bruteforce_solver = BruteforceSolver(lp_problem=lpp)
        self.bruteforce_solution, self.best_bruteforce_solution_index = bruteforce_solver.solve()
        self.symplex_start_basis_index = 0
        symplex_solver = SymplexSolver(lpp)
        self.auxiliary_solution: list[BasisSolution] | None = None
        self.auxiliary_swaps: list[tuple[int, int]] | None = None
        self.modified_solution: list[BasisSolution] | None = None
        self.modified_swaps: list[tuple[int, int]] | None = None

        if self.lpp.has_simple_start_basis:
            start_basis = self.lpp.start_basis
        else:
            self.modified_solution, self.modified_swaps = symplex_solver.modified_solve()

            self.auxiliary_solution, self.auxiliary_swaps = symplex_solver.auxiliary_solve()
            start_basis = self.auxiliary_solution[-1].basis
            self.symplex_start_basis_index = len(self.auxiliary_solution) - 1

        self.symplex_solution, self.symplex_swaps = symplex_solver.solve(start_basis)

        curr_path = sabonis_template_path
        if teacher == Teacher.SIDNEV:
            curr_path = sidnev_template_path
        template = DocumentTemplate(curr_path)
        super().__init__(template)
        self.root_tf = self

    @template_filler
    def _fill_problem(self):
        return ProblemTF(variant=self.variant, lpp_vm=self.lpp_vm, teacher=self.teacher)

    @template_filler
    def _fill_canonical_problem_part(self):
        return CanonicalProblemTF(lpp_vm=self.lpp_vm)

    @template_filler
    def _fill_geometric_solution_part(self):
        opt_solution = self.symplex_solution[-1]
        return GeometricSolutionTF(solutions=self.bruteforce_solution, opt_sol=opt_solution)

    @template_filler
    def _fill_bruteforce_solution_part(self):
        return BruteforceSolutionTF(all_solutions=self.bruteforce_solution,
                                    opt_solution_index=self.best_bruteforce_solution_index)

    @template_filler
    def _fill_auxiliary_task_part(self):
        if self.auxiliary_solution is None:
            return None
        return AuxiliaryTaskTF(self.lpp_vm, auxiliary_solution=self.auxiliary_solution,
                               auxiliary_swaps=self.auxiliary_swaps)

    @template_filler
    def _fill_matrix_symplex_solution_part(self):
        return MatrixSymplexSolutionTF(lpp=self.lpp, solutions=self.symplex_solution, swaps=self.symplex_swaps,
                                       start_basis_index=self.symplex_start_basis_index)

    @template_filler
    def _fill_modified_symplex_solution_part(self):
        return ModifiedSymplexSolutionTF(solutions=self.modified_solution, swaps=self.modified_swaps)

    @template_filler
    def _fill_table_symplex_solution_part(self):
        return TableSymplexSolutionTF(solutions=self.symplex_solution, swaps=self.symplex_swaps,
                                      start_basis_index=self.symplex_start_basis_index)

    @template_filler
    def _fill_reverse_symplex_part(self):
        new_constraint = generate_new_constraint(self.bruteforce_solution)
        return ReverseSymplexTF(opt_sol=self.symplex_solution[-1], new_constraint=new_constraint)

    @template_filler
    def _fill_dual_problem_part(self):
        return DualProblemTF(lpp=self.lpp)

    @template_filler
    def _fill_conjugate_opt_point_search(self):
        if self.teacher == Teacher.SABONIS:
            return None
        return COPSSearchTF(self.symplex_solution[-1])
