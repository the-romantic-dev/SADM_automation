from report.docx.omml import latex2omml
from tasks.scheduling_theory.scheduling_data import SchedulingData
from tasks.scheduling_theory.solvers.moments.moments_solvers import MathMomentsSolver


def latex_min_t_i(i): return f"t_{i}^*"


def latex_max_t_i(i): return f"t_{i}^{{**}}"


class MathMomentsConstraintsLatex:
    def __init__(self, scheduling_data: SchedulingData, min_moments):
        self.scheduling_data = scheduling_data
        self.last_min_moment = min_moments[scheduling_data.last_node]

    def get_moments_constraints_latex(self, is_min: bool):
        result = []
        if is_min:
            result.append(
                f"{latex_min_t_i(1)} = 0"
            )
        else:
            result.append(
                f"{latex_max_t_i(self.scheduling_data.last_node)} = {self.last_min_moment}"
            )

        edges = self.scheduling_data.get_edges()
        sorted_edges = sorted(edges, key=lambda elem: elem[1], reverse=not is_min)
        for edge in sorted_edges:
            j, i = edge
            if is_min:
                result.append(
                    f"{latex_min_t_i(i)} \\ge {latex_min_t_i(j)} + {self.scheduling_data.get_edge_weight(edge)}"
                )
            else:
                result.append(
                    f"{latex_max_t_i(i)} \\ge {latex_max_t_i(j)} - {self.scheduling_data.get_edge_weight(edge)}"
                )
        return result


class MathMomentsResultTables:
    def __init__(self, scheduling_data: SchedulingData, math_moments_solver: MathMomentsSolver):
        self.scheduling_data = scheduling_data
        self.math_moments_solver = math_moments_solver

    def get_result_table(self, is_min: bool):
        values = []
        variables = []
        nodes = self.scheduling_data.nodes

        for i in nodes:
            if is_min:
                variables.append(latex2omml(latex_min_t_i(i)))
                values.append(self.math_moments_solver.min_moments[i])
            else:
                variables.append(latex2omml(latex_max_t_i(i)))
                values.append(self.math_moments_solver.max_moments[i])
        return [variables, values]
