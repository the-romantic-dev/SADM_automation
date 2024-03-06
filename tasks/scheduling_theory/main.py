import os
from pathlib import Path

from tasks.scheduling_theory import task_data as td
from tasks.scheduling_theory.document_template.scheduling_theory_document_template import \
    SchedulingTheoryDocumentTemplate
from tasks.scheduling_theory.solvers.diagrams.gantt_chart_creator import GanttChartCreator
from tasks.scheduling_theory.solvers.math.math_moments_constraints_data import MathModelConstraintsData
from tasks.scheduling_theory.solvers.math.math_solver import DefaultMathModelSolver, IntensiveMathModelSolver, \
    BinaryMathModelSolver, ChangedBinaryMathModelSolver
from tasks.scheduling_theory.solvers.moments.moments_solvers import DynamicalMomentsSolver, MathMomentsSolver
from tasks.scheduling_theory.solvers.moments.reserves_calculator import ReservesCalculator
from tasks.scheduling_theory.solvers.probabilistic.probabilistic_model_solver import ProbabilisticModelSolver
from tasks.scheduling_theory.solvers.scheduling_problem.scheduling_problem_solver import SchedulingProblemSolver

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":

    scheduling_data = td.scheduling_data
    if td.is_sidnev:
        template_file = "Шаблон Сиднев.docx"
    else:
        template_file = "Шаблон Сабонис.docx"
    template_path = Path(ROOT_DIR, "templates", template_file)
    document_template = SchedulingTheoryDocumentTemplate(template_path)

    dynamical_moments_solver = DynamicalMomentsSolver(scheduling_data)
    math_model_constraints_data = MathModelConstraintsData(scheduling_data)
    default_math_model_solver = DefaultMathModelSolver(
        scheduling_data, constraints_data=math_model_constraints_data)
    intensive_math_model_solver = IntensiveMathModelSolver(scheduling_data, default_math_model_solver,
                                                           is_sidnev=td.is_sidnev)
    math_moments_solver = MathMomentsSolver(scheduling_data)
    reserves_calculator = ReservesCalculator(
        min_moments=math_moments_solver.min_moments,
        max_moments=math_moments_solver.max_moments,
        scheduling_data=scheduling_data)
    binary_math_model_solver = BinaryMathModelSolver(scheduling_data)
    changed_binary_math_model_solver = ChangedBinaryMathModelSolver(scheduling_data, default_math_model_solver)
    probabilistic_model_solver = ProbabilisticModelSolver(scheduling_data, reserves_calculator)

    scheduling_problem_solver = SchedulingProblemSolver(scheduling_data, reserves_calculator)
    # scheduling_problem_solver.get_solution_steps()

    document_template.fill_task_data()
    document_template.fill_dynamical_moments(dynamical_moments_solver)
    document_template.fill_math_models_constraints(math_model_constraints_data, default_math_model_solver)
    document_template.fill_default_math_model_result(default_math_model_solver)
    document_template.fill_intensive_math_model_result(intensive_math_model_solver)
    document_template.fill_math_moments(scheduling_data, math_moments_solver)
    document_template.fill_reserves(reserves_calculator)
    document_template.fill_binary_math_model(binary_math_model_solver)
    document_template.fill_changed_binary_math_model(changed_binary_math_model_solver)
    document_template.fill_probabilistic_model(probabilistic_model_solver)
    document_template.fill_scheduling_problem(scheduling_problem_solver)

    document_template.save(save_path=td.folder)
