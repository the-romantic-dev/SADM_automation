from tasks.task2_1_st.solvers.moments.reserves_calculator import ReservesCalculator


def t_min_latex(i): return f"t_{i}^{{*}}"


def r_latex(i, j): return f"r_{{{i}{j}}}"


def t_max_latex(i): return f"t_{i}^{{**}}"


def tau_latex(i, j): return f"\\tau_{{{i}{j}}}"


def path_latex(path: list):
    result = "\\longrightarrow".join([str(i) for i in path])
    return result


def F_latex(index_1, index_2):
    return f"F_{{ {index_1}, {index_2} }}"


def F_ir1(j): return F_latex("нз1", f"{j}")


def F_ir2(i, j): return F_latex("нз2", f"{i}{j}")


def F_free(i, j): return F_latex("c", f"{i}{j}")


class ReservesLatex:
    def __init__(self, reserves_calculator: ReservesCalculator):
        self.reserves_calculator = reserves_calculator

    def get_reserves_matrix(self):
        last_node = self.reserves_calculator.scheduling_data.last_node
        edges = self.reserves_calculator.scheduling_data.get_edges()
        reserves = self.reserves_calculator.full_reserves
        header = [""] + [str(i + 1) for i in range(last_node)]
        vertical_header = [[str(i + 1)] for i in range(last_node)]
        vertical_header.insert(0, header)
        for i in range(1, last_node + 1):
            for j in range(1, last_node + 1):
                edge = (i, j)
                if edge in edges:
                    vertical_header[i].append(str(int(reserves[edge])))
                else:
                    vertical_header[i].append("-")
        return vertical_header
    def get_ciritcal_path_latexs(self):
        result = []
        critical_paths = self.reserves_calculator.calc_critical_paths()
        for path in critical_paths:
            result.append(path_latex(path))
        return result

    def get_full_reserves_formulas_latex(self):
        result = []
        edges = self.reserves_calculator.scheduling_data.get_edges()
        for edge in edges:
            i, j = edge
            result.append(self._full_reserve_formula(i, j))
        return result

    def get_free_reserves_formulas_latex(self):
        result = []
        edges = self.reserves_calculator.scheduling_data.get_edges()
        for edge in edges:
            i, j = edge
            result.append(self._free_reserve_formula(i, j))
        return result

    def get_ir2_formulas_latex(self):
        result = []
        edges = self.reserves_calculator.scheduling_data.get_edges()
        for edge in edges:
            i, j = edge
            result.append(self._ir2_formula(i, j))
        return result

    def get_ir1_formulas_latex(self):
        result = []
        nodes = self.reserves_calculator.scheduling_data.nodes
        for node in nodes:
            result.append(self._ir1_formula(node))
        return result

    def _ir1_formula(self, j):
        t_max = t_max_latex(j)
        t_min = t_min_latex(j)
        t_max_value = int(self.reserves_calculator.max_moments[j])
        t_min_value = int(self.reserves_calculator.min_moments[j])
        F_value = int(self.reserves_calculator.calc_independent_reserve_I(j))

        result = f"{F_ir1(j)} = {t_max} - {t_min} = {t_max_value} - {t_min_value} = {F_value}"
        return result

    def _full_reserve_formula(self, i, j):
        r_ij = r_latex(i, j)
        t_j = t_max_latex(j)
        t_i = t_min_latex(i)
        tau = tau_latex(i, j)

        t_j_value = int(self.reserves_calculator.max_moments[j])
        t_i_value = int(self.reserves_calculator.min_moments[i])
        tau_value = int(self.reserves_calculator.scheduling_data.get_edge_weight((i, j)))

        r_ij_value = int(self.reserves_calculator.calc_full_reserve(i, j))
        return (f"{r_ij} = {t_j} - \\left ( {t_i} + {tau} \\right) ="
                f" {t_j_value} - \\left ( {t_i_value} + {tau_value} \\right) = {r_ij_value}")

    def _free_reserve_formula(self, i, j):
        F = F_free(i, j)
        t_j = t_min_latex(j)
        t_i = t_min_latex(i)
        tau = tau_latex(i, j)

        t_j_value = int(self.reserves_calculator.min_moments[j])
        t_i_value = int(self.reserves_calculator.min_moments[i])
        tau_value = int(self.reserves_calculator.scheduling_data.get_edge_weight((i, j)))

        F_value = int(self.reserves_calculator.calc_free_reserve(i, j))
        return (f"{F} = {t_j} - \\left ( {t_i} + {tau} \\right) ="
                f" {t_j_value} - \\left ( {t_i_value} + {tau_value} \\right) = {F_value}")

    def _ir2_formula(self, i, j):
        F = F_ir2(i, j)
        t_j = t_min_latex(j)
        t_i = t_max_latex(i)
        tau = tau_latex(i, j)

        t_j_value = int(self.reserves_calculator.min_moments[j])
        t_i_value = int(self.reserves_calculator.max_moments[i])
        tau_value = int(self.reserves_calculator.scheduling_data.get_edge_weight((i, j)))

        F_value = int(self.reserves_calculator.calc_independent_reserve_II(i, j))
        return (f"{F} = {t_j} - \\left ( {t_i} + {tau} \\right) ="
                f" {t_j_value} - \\left ( {t_i_value} + {tau_value} \\right) = {F_value}")
