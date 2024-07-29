from report.docx.omml import latex2omml
from tasks.task2_1_st.solvers.math.math_moments_constraints_data import MathModelConstraintsData
from tasks.task2_1_st.solvers.math.math_solver import IntensiveMathModelSolver, DefaultMathModelSolver
import tasks.task2_1_st.task_data as td

def latex_t_ij(i, j):
    return f"t_{{{i}{j}}}"


def latex_m_ij(i, j):
    return f"m_{{{i}{j}}}"


def latex_T_M(M):
    return f"T_{M}"


def latex_default_total_time_constraint(l, M, weight):
    return f"{latex_T_M(M)} \\ge {latex_t_ij(l, M)} + {weight}"


def latex_intensive_total_time_constraint(l, M, weight):
    return f"{latex_T_M(M)} \\ge {latex_t_ij(l, M)} + \\frac {{{weight}}} {{{latex_m_ij(l, M)}}}"


def latex_default_task_time_constraint(l, i, j, weight):
    return f"{latex_t_ij(i, j)} \\ge {latex_t_ij(l, i)} + {weight}"


def latex_intensive_task_time_constraint(l, i, j, weight):
    return f"{latex_t_ij(i, j)} \\ge {latex_t_ij(l, i)} + \\frac {{{weight}}} {{{latex_m_ij(l, i)}}}"


def latex_intensive_objective_limit_constraint(limit_value, intensity_limit, is_sidnev, last_node):
    if is_sidnev:
        return f"\\sum_{{(ij)}}{{m_{{ij}}}}\\le {intensity_limit} \\cdot {limit_value}"
    else:
        return f"T_{last_node}\\le {intensity_limit} \\cdot {limit_value} = {round(intensity_limit * limit_value, 3)}"


def latex_math_constraints(
        constraints_data: MathModelConstraintsData,
        task_time_constraint_latex_producer,
        total_time_constraint_latex_producer):
    result = []
    task_time_constraints_data = constraints_data.task_time_constraints_data
    total_time_constraints_data = constraints_data.total_time_constraints_data

    for constraint in task_time_constraints_data:
        latex = task_time_constraint_latex_producer(
            l=constraint.l, i=constraint.i, j=constraint.j, weight=constraint.li_weight
        )
        result.append(latex)

    for constraint in total_time_constraints_data:
        latex = total_time_constraint_latex_producer(
            l=constraint.l, M=constraint.M, weight=constraint.lM_weight
        )
        result.append(latex)
    return result


class MathModelConstraintsLatex:
    def __init__(self, constraints_data: MathModelConstraintsData, default_math_model_solver: DefaultMathModelSolver):
        self.constraints_data = constraints_data
        self.intensity_limit = constraints_data.scheduling_data.intensity_limit
        self.default_math_model_time = default_math_model_solver.total_time

    def get_default_constraints_formulas_latex(self):
        return latex_math_constraints(
            constraints_data=self.constraints_data,
            task_time_constraint_latex_producer=latex_default_task_time_constraint,
            total_time_constraint_latex_producer=latex_default_total_time_constraint)

    def get_intensive_constraints_formulas_latex(self):
        result = latex_math_constraints(
            constraints_data=self.constraints_data,
            task_time_constraint_latex_producer=latex_intensive_task_time_constraint,
            total_time_constraint_latex_producer=latex_intensive_total_time_constraint)
        if td.is_sidnev:
            limit_value = self.constraints_data.scheduling_data.edges_num
        else:
            limit_value = self.default_math_model_time
        latex_objective_limit_constraint = latex_intensive_objective_limit_constraint(
            limit_value=limit_value,
            intensity_limit=self.intensity_limit,
            is_sidnev=td.is_sidnev,
            last_node=self.constraints_data.scheduling_data.last_node)
        result.append(latex_objective_limit_constraint)
        return result


class DefaultModelSolutionTableData:
    def __init__(self, default_math_model_solver: DefaultMathModelSolver):
        self.default_math_model_solver = default_math_model_solver

    def get_result_table(self):
        solution = self.default_math_model_solver.solution
        variables = []
        values = []
        for elem in solution:
            if elem.i == elem.j:
                variables.append(
                    latex2omml(
                        latex_T_M(elem.i)
                    )
                )
            else:
                variables.append(
                    latex2omml(
                        latex_t_ij(elem.i, elem.j)
                    )
                )
            values.append(str(int(elem.value)))
        table_data = [variables, values]
        transposed_table_data = [[row[i] for row in table_data] for i in range(len(table_data[0]))]
        return transposed_table_data


class IntensiveModelSolutionTableData:
    def __init__(self, intensive_math_model_solver: IntensiveMathModelSolver):
        self.intensive_math_model_solver = intensive_math_model_solver

    def get_t_table(self) -> list[list]:
        solution = self.intensive_math_model_solver.t_solution
        T_result = self.intensive_math_model_solver.T_result
        variables = []
        values = []
        for elem in solution:
            variables.append(
                latex2omml(
                    latex_t_ij(elem.i, elem.j)
                )
            )
            values.append(str(elem.value))
        variables.append(
            latex2omml(
                latex_T_M(self.intensive_math_model_solver.scheduling_data.last_node)
            )
        )
        values.append(str(T_result))

        table_data = [variables, values]
        transposed_table_data = [[row[i] for row in table_data] for i in range(len(table_data[0]))]
        return transposed_table_data

    def get_m_table(self) -> list[list]:
        solution = self.intensive_math_model_solver.m_solution
        variables = []
        values = []
        for elem in solution:
            variables.append(
                latex2omml(
                    latex_m_ij(elem.i, elem.j)
                )
            )
            values.append(str(elem.value))
        table_data = [variables, values]
        transposed_table_data = [[row[i] for row in table_data] for i in range(len(table_data[0]))]
        return transposed_table_data
