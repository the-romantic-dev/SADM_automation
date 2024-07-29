from tasks.task2_1_st.solvers.moments.moments_solvers import DynamicalMomentsSolver


def t_latex(i, is_local_min):
    if is_local_min:
        return f"t^{{*}}_{i}"
    else:
        return f"t^{{**}}_{i}"


class DynamicalMomentsLatex:
    def __init__(self, dynamical_moments_solver: DynamicalMomentsSolver):
        self.dynamical_moments_solver: DynamicalMomentsSolver = dynamical_moments_solver

    def get_moments_T_calculation_latex(self):
        last_node = self.dynamical_moments_solver.scheduling_data.last_node
        T = self.dynamical_moments_solver.total_time
        return f"T = {t_latex(last_node, is_local_min=True)} = {t_latex(last_node, is_local_min=False)} = {T}"

    def get_min_moments_formulas_latex(self) -> list[str]:
        return self._latex_dynamical_t_calculations(is_min=True)

    def get_max_moments_formulas_latex(self) -> list[str]:
        return self._latex_dynamical_t_calculations(is_min=False)

    def _latex_dynamical_t_calculations(self, is_min):
        if is_min:
            data = self.dynamical_moments_solver.min_calculation_data
        else:
            data = self.dynamical_moments_solver.max_calculation_data

        def variant_latex(i, weight):
            if is_min:
                return f"{t_latex(i, is_min)} + {weight}"
            else:
                return f"{t_latex(i, is_min)} - {weight}"

        def row_latex(i, nodes, variants, weights, result):
            step_1 = t_latex(i, is_min)
            step_2_vector_parts = []
            for j in range(len(nodes)):
                step_2_vector_parts.append(
                    variant_latex(nodes[j], weights[j])
                )
            if is_min:
                aggr_function = "max"
            else:
                aggr_function = "min"
            step_2_vector = " \\\\ ".join(step_2_vector_parts)
            step_2 = f"{aggr_function} \\left( \\begin{{matrix}} {step_2_vector} \\end{{matrix}}\\right)"
            step_3_vector = " \\\\ ".join([str(elem) for elem in variants])
            step_3 = f"{aggr_function} \\left( \\begin{{matrix}} {step_3_vector} \\end{{matrix}}\\right)"
            step_4 = f"{result}"
            steps = [step_1, step_2, step_3, step_4]
            return " = ".join(steps)

        if is_min:
            rows = [f"{t_latex(1, is_min)} = 0"]
        else:
            M = max(self.dynamical_moments_solver.min_moments.keys())
            last_t_min = self.dynamical_moments_solver.min_moments[M]
            rows = [f"{t_latex(M, is_min)} = {t_latex(M, is_local_min=True)} = {last_t_min}"]

        if is_min:
            data_keys = sorted(data.keys())
            skip_node = 1
        else:
            data_keys = reversed(sorted(data.keys()))
            M = max(self.dynamical_moments_solver.min_moments.keys())
            skip_node = M
        for i in data_keys:
            if i == skip_node:
                continue
            variants = data[i]["variants"]
            if is_min:
                nodes_name = "incoming_nodes"
            else:
                nodes_name = "outcoming_nodes"
            nodes = data[i][nodes_name]
            weights = data[i]["weights"]
            result = data[i]["result"]
            rows.append(
                row_latex(i, nodes, variants, weights, result)
            )
        return rows
