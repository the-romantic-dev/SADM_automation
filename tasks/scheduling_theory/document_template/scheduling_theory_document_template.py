from pathlib import Path

from tasks.scheduling_theory import task_data as td
from report.docx.objects.document_template import DocumentTemplate
from tasks.scheduling_theory.document_template.fill_data.binary_math_model_data import BinaryMathModelData, \
    ChangedBinaryMathModelData
from tasks.scheduling_theory.document_template.fill_data.dynamical_moments_data import DynamicalMomentsLatex
from tasks.scheduling_theory.document_template.fill_data.math_model_data import MathModelConstraintsLatex, \
    DefaultModelSolutionTableData, IntensiveModelSolutionTableData
from tasks.scheduling_theory.document_template.fill_data.math_moments_data import MathMomentsConstraintsLatex, \
    MathMomentsResultTables
from tasks.scheduling_theory.document_template.fill_data.probability_data import ProbabilityData
from tasks.scheduling_theory.document_template.fill_data.reserves_data import ReservesLatex
from tasks.scheduling_theory.document_template.fill_data.scheduling_problem_data import SchedulingProblemData
from tasks.scheduling_theory.scheduling_data import SchedulingData
from tasks.scheduling_theory.solvers.diagrams.gantt_chart_creator import GanttChartCreator
from tasks.scheduling_theory.solvers.math.math_moments_constraints_data import MathModelConstraintsData
from tasks.scheduling_theory.solvers.math.math_solver import DefaultMathModelSolver, IntensiveMathModelSolver, \
    BinaryMathModelSolver, ChangedBinaryMathModelSolver
from tasks.scheduling_theory.solvers.moments.moments_solvers import DynamicalMomentsSolver, MathMomentsSolver
from tasks.scheduling_theory.solvers.moments.reserves_calculator import ReservesCalculator
from tasks.scheduling_theory.solvers.probabilistic.probabilistic_model_solver import ProbabilisticModelSolver
from tasks.scheduling_theory.solvers.scheduling_problem.rule import Rule
from tasks.scheduling_theory.solvers.scheduling_problem.scheduling_problem_solver import SchedulingProblemSolver


class SchedulingTheoryDocumentTemplate(DocumentTemplate):
    def __init__(self, template_path: Path):
        super().__init__(template_path)

    def fill_task_data(self):
        self._fill_text(key="variant", text=str(td.variant))
        self._fill_text(key="performers_n", text=str(td.performers_number))
        self._fill_picture(key="graph_img", picture_path=td.graph_img_path)
        if td.is_sidnev:
            self._fill_text(key="rule", text=Rule(td.scheduling_data.rule_types[0]).rule_text())
        else:
            self._fill_text(key="rule_1", text=Rule(td.scheduling_data.rule_types[0]).rule_text())
            self._fill_text(key="rule_2", text=Rule(td.scheduling_data.rule_types[1]).rule_text())
            self._fill_text(key="rule_3", text=Rule(td.scheduling_data.rule_types[2]).rule_text())
            self._fill_text(key="intensity_limit", text=str(td.intensity_limit))

    def fill_dynamical_moments(self, dynamical_moments_solver: DynamicalMomentsSolver):
        dynamical_moments_latex = DynamicalMomentsLatex(dynamical_moments_solver)

        min_moments_formulas_key = "dynamical_min_t_calculations"
        min_moments_formulas = dynamical_moments_latex.get_min_moments_formulas_latex()
        self._fill_formulas_list(
            key=min_moments_formulas_key,
            latex_formulas_list=min_moments_formulas
        )

        max_moments_formulas_key = "dynamical_max_t_calculations"
        max_moments_formulas = dynamical_moments_latex.get_max_moments_formulas_latex()
        self._fill_formulas_list(
            key=max_moments_formulas_key,
            latex_formulas_list=max_moments_formulas
        )

        moments_T_calculation_key = "moments_T_calculation"
        moments_T_calculation_data = dynamical_moments_latex.get_moments_T_calculation_latex()
        self._fill_formula(key=moments_T_calculation_key, formula_latex=moments_T_calculation_data)

    def fill_math_moments(self, scheduling_data: SchedulingData, math_moments_solver: MathMomentsSolver):
        constraints_latex_generator = MathMomentsConstraintsLatex(scheduling_data, math_moments_solver.min_moments)
        min_constraints_key = "math_min_t_constraints"
        max_constraints_key = "math_max_t_constraints"

        min_constraints_data = constraints_latex_generator.get_moments_constraints_latex(is_min=True)
        max_constraints_data = constraints_latex_generator.get_moments_constraints_latex(is_min=False)

        self._fill_formulas_list(key=min_constraints_key, latex_formulas_list=min_constraints_data)
        self._fill_formulas_list(key=max_constraints_key, latex_formulas_list=max_constraints_data)

        result_table_generator = MathMomentsResultTables(scheduling_data, math_moments_solver)

        min_result_table_key = "math_min_t_values_table"
        max_result_table_key = "math_max_t_values_table"

        min_result_table_data = result_table_generator.get_result_table(is_min=True)
        max_result_table_data = result_table_generator.get_result_table(is_min=False)

        self._fill_table(key=min_result_table_key, table_data=min_result_table_data)
        self._fill_table(key=max_result_table_key, table_data=max_result_table_data)

    def fill_math_models_constraints(self, math_model_constraints_data: MathModelConstraintsData,
                                     default_math_model_solver: DefaultMathModelSolver):
        data_generator = MathModelConstraintsLatex(constraints_data=math_model_constraints_data,
                                                                 default_math_model_solver=default_math_model_solver)

        tw_value_key = "Tw_value"
        tw_value_data = data_generator.default_math_model_time * data_generator.intensity_limit
        self._fill_formula(key=tw_value_key, formula_latex=str(round(tw_value_data, 3)))


        default_constraints_formulas_key = "default_math_constraints"
        default_constraints_formulas = data_generator.get_default_constraints_formulas_latex()
        self._fill_formulas_list(
            key=default_constraints_formulas_key,
            latex_formulas_list=default_constraints_formulas
        )

        intensive_constraints_formulas_key = "intensive_math_constraints"
        intensive_constraints_formulas = data_generator.get_intensive_constraints_formulas_latex()
        self._fill_formulas_list(
            key=intensive_constraints_formulas_key,
            latex_formulas_list=intensive_constraints_formulas
        )

    def fill_default_math_model_result(self, default_math_model_solver: DefaultMathModelSolver):
        table_data = DefaultModelSolutionTableData(default_math_model_solver).get_result_table()
        key = "default_math_result_table"
        self._fill_table(key=key, table_data=table_data)

    def fill_intensive_math_model_result(self, intensive_math_model_solver: IntensiveMathModelSolver):
        solution = IntensiveModelSolutionTableData(intensive_math_model_solver)
        t_table_data = solution.get_t_table()
        t_table_key = "intensive_math_result_t_table"
        self._fill_table(key=t_table_key, table_data=t_table_data)

        m_table_data = solution.get_m_table()
        m_table_key = "intensive_math_result_m_table"
        self._fill_table(key=m_table_key, table_data=m_table_data)

    def fill_reserves(self, reserves_calculator: ReservesCalculator):
        reserves_latex_generator = ReservesLatex(reserves_calculator)

        full_reserves_key = "full_reserves_calculations"
        full_reserves_data = reserves_latex_generator.get_full_reserves_formulas_latex()
        self._fill_formulas_list(key=full_reserves_key, latex_formulas_list=full_reserves_data)

        reserves_matrix_key = "reserves_matrix"
        reserves_matrix_data = reserves_latex_generator.get_reserves_matrix()
        self._fill_table(key=reserves_matrix_key, table_data=reserves_matrix_data)


        critical_paths_key = "critical_paths"
        critical_paths_data = reserves_latex_generator.get_ciritcal_path_latexs()
        self._fill_formulas_list(key=critical_paths_key, latex_formulas_list=critical_paths_data)

        ir1_key = "ir1_calculations"
        ir1_data = reserves_latex_generator.get_ir1_formulas_latex()
        self._fill_formulas_list(key=ir1_key, latex_formulas_list=ir1_data)

        ir2_key = "ir2_calculations"
        ir2_data = reserves_latex_generator.get_ir2_formulas_latex()
        self._fill_formulas_list(key=ir2_key, latex_formulas_list=ir2_data)

        free_key = "fr_calculations"
        free_data = reserves_latex_generator.get_free_reserves_formulas_latex()
        self._fill_formulas_list(key=free_key, latex_formulas_list=free_data)

    def fill_binary_math_model(self, binary_math_model_solver: BinaryMathModelSolver):
        binary_math_model_latex_generator = BinaryMathModelData(binary_math_model_solver)

        tasks_allocation_key = "binary_performers_tasks_allocation"
        tasks_allocation_data = binary_math_model_latex_generator.task_allocations_latex()
        self._fill_formulas_list(key=tasks_allocation_key, latex_formulas_list=tasks_allocation_data)

        binary_constraints_num_key = "binary_constraints_num"
        binary_constraints_num_data = binary_math_model_latex_generator.constraints_num_latex()
        self._fill_formula(key=binary_constraints_num_key, formula_latex=binary_constraints_num_data)

        binary_variables_num_key = "binary_variables_num"
        binary_variables_num_data = binary_math_model_latex_generator.variables_num_latex()
        self._fill_formula(key=binary_variables_num_key, formula_latex=binary_variables_num_data)

    def fill_changed_binary_math_model(self, changed_binary_math_model_solver: ChangedBinaryMathModelSolver):
        data_generator = ChangedBinaryMathModelData(changed_binary_math_model_solver)

        task_allocation_key = "changed_binary_performers_tasks_allocation"
        task_allocation_data = data_generator.get_allocation_latex()
        self._fill_formula(key=task_allocation_key, formula_latex=task_allocation_data)

        variables_num_key = "changed_binary_variables_num"
        variables_num_data = data_generator.get_variables_num_latex()
        self._fill_formula(key=variables_num_key, formula_latex=variables_num_data)

        constraints_num_key = "changed_binary_constraints_num"
        constraints_num_data = data_generator.get_constraints_num_latex()
        self._fill_formula(key=constraints_num_key, formula_latex=constraints_num_data)

        constraints_key = "changed_binary_constraints"
        constraints_data = data_generator.get_constraints_latex()
        self._fill_formulas_list(key=constraints_key, latex_formulas_list=constraints_data)

        t_result_table_key = "changed_binary_result_t_table"
        t_result_table_data = data_generator.get_result_t_table()
        self._fill_table(key=t_result_table_key, table_data=t_result_table_data)

        Y_result_table_key = "changed_binary_result_Y_table"
        Y_result_table_data = data_generator.get_result_Y_table()
        self._fill_table(key=Y_result_table_key, table_data=Y_result_table_data)

        tasks_order_key = "changed_binary_tasks_order"
        tasks_order_data = data_generator.get_tasks_order_latex()
        self._fill_formula(key=tasks_order_key, formula_latex=tasks_order_data)

    def fill_probabilistic_model(self, probability_solver: ProbabilisticModelSolver):
        data_generator = ProbabilityData(probability_solver)

        overtime_probability_formula_key = "overtime_probability_formula"
        overtime_probability_formula_data = data_generator.get_overtime_probability_formulas()

        self._fill_formulas_list(key=overtime_probability_formula_key, latex_formulas_list=overtime_probability_formula_data)

        expected_value_key = "expected_value_calculation"
        expected_value_data = data_generator.expected_value_latex()
        self._fill_formulas_list(key=expected_value_key, latex_formulas_list=expected_value_data)

        dispersion_key = "dispersion_calculation"
        dispersion_data = data_generator.dispersion_latex()
        self._fill_formulas_list(key=dispersion_key, latex_formulas_list=dispersion_data)

        average_edge_weight_key = "average_edge_weight"
        average_edge_weight_data = data_generator.probability_solver.average_edge_weight()
        self._fill_text(key=average_edge_weight_key, text=str(average_edge_weight_data))

        standard_deviation_key = "standard_deviation"
        standard_deviation_data = data_generator.probability_solver.scheduling_data.standard_deviation
        self._fill_formula(key=standard_deviation_key, formula_latex=str(standard_deviation_data))

        standard_deviation_percent_key = "standard_deviation_percent"
        standard_deviation_percent_data = f"{int(standard_deviation_data * 100)}%"
        self._fill_text(key=standard_deviation_percent_key, text=standard_deviation_percent_data)

        average_deviation_calculation_key = "average_deviation_calculation"
        average_deviation_calculation_data = data_generator.average_deviation_calculation()
        self._fill_formula(key=average_deviation_calculation_key, formula_latex=average_deviation_calculation_data)

        double_sigma_key = "double_sigma_value"
        double_sigma_data = data_generator.double_sigma_value()
        self._fill_text(key=double_sigma_key, text=str(double_sigma_data))

        overtime_limit_key = "overtime_limit"
        overtime_limit_data = data_generator.probability_solver.scheduling_data.overtime_limit
        self._fill_formula(key=overtime_limit_key, formula_latex=f"{overtime_limit_data}")

        overtime_limit_percent_key = "overtime_limit_percent"
        overtime_limit_percent_data = f"{int(overtime_limit_data * 100)}%"
        self._fill_text(key=overtime_limit_percent_key, text=f"{overtime_limit_percent_data}")

        overtime_probability_percent_key = "overtime_probability_percent"
        overtime_probability_percent_data = f"{data_generator.probability_solver.result_not_overtime_probability() * 100}%"
        self._fill_text(key=overtime_probability_percent_key, text=overtime_probability_percent_data)

    def fill_scheduling_problem(self, scheduling_problem_solver: SchedulingProblemSolver):
        data_generator = SchedulingProblemData(scheduling_problem_solver)
        schedule_problem_calculation_table_key = "schedule_problem_calculation_table"
        time_key = "scheduling_problem_time"
        chart_key = "chart_img"
        downtimes_key = "resources_downtimes"

        if td.is_sidnev:
            schedule_problem_calculation_table_data = data_generator.get_calculation_table(solution_index=0)
            self._fill_table(key=schedule_problem_calculation_table_key,
                             table_data=schedule_problem_calculation_table_data)

            time_data = str(data_generator.scheduling_problem_solver.total_times[0])
            self._fill_text(key=time_key, text=time_data)

            chart_data = Path(td.chart_folder, td.chart_filename)
            chart_creator = GanttChartCreator(scheduling_problem_solver)
            chart_creator.make_diagram(is_compact=False, rule_index=0).savefig(chart_data.as_posix(),
                                                                              bbox_inches='tight')
            self._fill_picture(key=chart_key, picture_path=chart_data)
        else:
            for i in range(len(td.rule_types)):
                schedule_problem_calculation_table_data = data_generator.get_calculation_table(solution_index=i)
                self._fill_table(key=schedule_problem_calculation_table_key + f"_{i + 1}",
                                 table_data=schedule_problem_calculation_table_data)

                time_data = str(data_generator.scheduling_problem_solver.total_times[i])
                self._fill_text(key=time_key + f"_{i + 1}", text=time_data)

                chart_data = Path(td.chart_folder, f"gantt_chart_{i + 1}.png")
                chart_creator = GanttChartCreator(scheduling_problem_solver)
                chart_creator.make_diagram(is_compact=True, rule_index=i).savefig(chart_data.as_posix(),
                                                                                  bbox_inches='tight')
                self._fill_picture(key=chart_key + f"_{i + 1}", picture_path=chart_data)

                downtimes_data = data_generator.get_downtimes_formulas(rule_index=i)
                self._fill_formulas_list(key=downtimes_key + f"_{i + 1}", latex_formulas_list=downtimes_data)

            best_time_key = "best_time"
            best_time_data = min(scheduling_problem_solver.total_times)
            self._fill_text(key=best_time_key, text=str(best_time_data))

            best_rule_key = "best_rule"
            best_rule_data = scheduling_problem_solver.rules[
                scheduling_problem_solver.total_times.index(best_time_data)]
            self._fill_text(key=best_rule_key, text=best_rule_data.rule_text())
