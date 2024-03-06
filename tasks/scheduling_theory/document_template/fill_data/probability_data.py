from tasks.scheduling_theory.solvers.probabilistic.probabilistic_model_solver import ProbabilisticModelSolver


def P_TM_latex(overtime_limit, crit_path_index, is_result: bool = False):
    if not is_result:
        return f"P\\left( T_{{crit_{crit_path_index+1}}} \\le \\left( 1 + {overtime_limit} \\right)M\left[ T \\right] \\right)"
    else:
        return f"P\\left( T_{{\\Sigma}} \\le \\left( 1 + {overtime_limit} \\right)M\left[ T \\right] \\right)"


def Phi_latex(x):
    return f"\\Phi\\left( {x} \\right)"


def frac_latex(top, bottom): return f"\\frac{{ {top} }}{{ {bottom} }}"


def sqrt_latex(x): return f"\\sqrt{{ {x} }}"


def sum_latex(arg): return f"\\sum {{{arg}}}"


class ProbabilityData:
    def __init__(self, probability_solver: ProbabilisticModelSolver):
        self.probability_solver = probability_solver

    def average_deviation_calculation(self):
        average = self.probability_solver.average_edge_weight()
        sigma = self.probability_solver.scheduling_data.standard_deviation
        return f"{average} \\cdot {sigma} = {self.probability_solver.average_deviation()}"

    def double_sigma_value(self):
        return 2 * self.probability_solver.average_deviation()

    def expected_value_latex(self):
        result = []
        M_ij_latex = f"M_{{ij}}"
        paths_num = len(self.probability_solver.critical_paths_weights)
        for i in range(paths_num):
            path = self.probability_solver.critical_paths_weights[i]
            latex = (f"M\\left[ T_{{crit_{i+1}}} \\right] = {sum_latex(M_ij_latex)} = "
                     f"{'+'.join([str(w) for w in path])} = "
                     f"{self.probability_solver.expected_value()[i]}")
            result.append(latex)
        return result

    def dispersion_latex(self):
        result = []
        standard_deviation = self.probability_solver.scheduling_data.standard_deviation
        D_ij_latex = f"D_{{ij}}"
        paths_num = len(self.probability_solver.critical_paths_weights)
        for i in range(paths_num):
            path = self.probability_solver.critical_paths_weights[i]
            latex = (f"D\\left[ T_{{crit_{i+1}}} \\right] = {sum_latex(D_ij_latex)} = "
                     f"{standard_deviation}^2 \\cdot ({'+'.join([f'{w}^2' for w in path])}) = "
                     f"{self.probability_solver.dispersion()[i]}")
            result.append(latex)
        return result

    def _get_overtime_probability_formula(self, crit_path_index):
        overtime_limit = self.probability_solver.scheduling_data.overtime_limit
        D = self.probability_solver.dispersion()[crit_path_index]
        epsilon_latex = "\\varepsilon"
        sigma_T_latex = f"\\sigma_{{T_{{crit_{crit_path_index+1}}}}}"
        arg_latex = f"{frac_latex(top=epsilon_latex, bottom=sigma_T_latex)}"
        infinity_latex = "- \\infty "

        sqrt_dispersion_value_latex = sqrt_latex(D)
        arg_value_latex = frac_latex(top=self.probability_solver.epsilon(), bottom=sqrt_dispersion_value_latex)

        result = (f"{P_TM_latex(overtime_limit, crit_path_index)} = {Phi_latex(arg_latex)} - {Phi_latex(infinity_latex)} = "
                  f"{Phi_latex(arg_value_latex)} + 0.5 = "
                  f"{round(self.probability_solver.not_overtime_probability(crit_path_index) - 0.5, 5)} + 0.5 = "
                  f"{self.probability_solver.not_overtime_probability(crit_path_index)}")

        return result

    def get_overtime_probability_formulas(self):
        result = []
        multiply_latexs = []
        overtime_limit = self.probability_solver.scheduling_data.overtime_limit
        paths_num = len(self.probability_solver.critical_paths_weights)
        for i in range(paths_num):
            result.append(self._get_overtime_probability_formula(i))
            multiply_latexs.append(P_TM_latex(overtime_limit, i))

        if paths_num > 1:
            multiplication_latex = ' \\cdot '.join(multiply_latexs)
            result_probability_latex = (f"{P_TM_latex(overtime_limit, 0, is_result=True)} = "
                                        f"{multiplication_latex} = {self.probability_solver.result_not_overtime_probability()}")
            result.append(result_probability_latex)
        return result