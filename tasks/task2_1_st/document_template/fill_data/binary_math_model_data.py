import math

from report.docx.omml import latex2omml
from tasks.task2_1_st.solvers.math.math_solver import BinaryMathModelSolver, ChangedBinaryMathModelSolver
from util.common import transpose


def comb_latex(n): return f"C^2_{n}"


def t_ij(i, j): return f"t_{{ {i}{j} }}"


def allocation_latex(index, tasks_list):
    tasks_list_latexs = [t_ij(i, j) for i, j in tasks_list]
    return f"{index}: \\left[ {','.join(tasks_list_latexs)} \\right]"


def Y_latex(i, j, l, m): return f"Y_{{ {i}{j}, {l}{m} }}"


def binary_constraints_latex(i, j, l, m, weight_ij, weight_lm):
    weight = {
        (i, j): weight_ij,
        (l, m): weight_lm
    }

    def pair_constraint_latex(i, j, l, m):
        return (f"\\left(M + {weight[(l, m)]} \\right) {Y_latex(i, j, l, m)} +"
                f"\\left({t_ij(i, j)} - {t_ij(l, m)} \\right) \\ge {weight[(l, m)]}")

    norm_constraint = f"{Y_latex(i, j, l, m)} + {Y_latex(l, m, i, j)} = 1"
    return [pair_constraint_latex(i, j, l, m), pair_constraint_latex(l, m, i, j), norm_constraint]


def comb(n):
    k = 2
    return math.comb(n, k)


class BinaryMathModelData:
    def __init__(self, binary_math_model_solver: BinaryMathModelSolver):
        self.binary_math_model_solver = binary_math_model_solver

    def _comb_sum_latex(self):
        allocation = self.binary_math_model_solver.task_allocation
        lengthens = [len(i) for i in allocation]
        combs = [comb_latex(l) for l in lengthens]
        return f"\\left( {'+'.join(combs)} \\right)"

    def _comb_values_sum_latex(self):
        allocation = self.binary_math_model_solver.task_allocation
        combs_values = [str(self.binary_math_model_solver.comb(i)) for i in range(len(allocation))]
        return f"\\left( {'+'.join(combs_values)} \\right)"

    def _num_latex(self, num, result):
        return f"{num} \\cdot {self._comb_sum_latex()} = {num} \\cdot {self._comb_values_sum_latex()} = {result}"

    def constraints_num_latex(self):
        return self._num_latex(num=3, result=self.binary_math_model_solver.constraints_num())

    def variables_num_latex(self):
        return self._num_latex(num=2, result=self.binary_math_model_solver.variables_num())

    def task_allocations_latex(self):
        result = []
        task_allocation = self.binary_math_model_solver.task_allocation

        for i in range(len(task_allocation)):
            result.append(
                allocation_latex(index=i + 1, tasks_list=task_allocation[i])
            )
        return result


class ChangedBinaryMathModelData:
    def __init__(self, changed_binary_math_model_solver: ChangedBinaryMathModelSolver):
        self.changed_binary_math_model_solver = changed_binary_math_model_solver

    def get_allocation_latex(self):
        ta = self.changed_binary_math_model_solver.task_allocation
        result = []
        for i in range(len(ta)):
            result.append(
                allocation_latex(index=i + 1, tasks_list=ta[i])
            )
        return result
        # return allocation_latex(1, )

    def get_variables_num_latex(self):
        ta = self.changed_binary_math_model_solver.task_allocation
        comb_latexs = []
        combs = []
        for i in range(len(ta)):
            comb_latexs.append(comb_latex(len(ta[i])))
            combs.append(2 * comb(len(ta[i])))
        return f"2 \\cdot ({'+'.join(comb_latexs)}) = {sum(combs)}"

    def get_constraints_num_latex(self):
        ta = self.changed_binary_math_model_solver.task_allocation
        comb_latexs = []
        combs = []
        for i in range(len(ta)):
            comb_latexs.append(comb_latex(len(ta[i])))
            combs.append(3 * comb(len(ta[i])))
        return f"3 \\cdot ({'+'.join(comb_latexs)}) = {sum(combs)}"

    def get_constraints_latex(self):
        result = []
        ta = self.changed_binary_math_model_solver.task_allocation
        for curr_allocation in ta:
            allocation_size = len(curr_allocation)
            for a in range(allocation_size):
                for b in range(a + 1, allocation_size):
                    i, j = curr_allocation[a]
                    l, m = curr_allocation[b]
                    weight_ij = self.changed_binary_math_model_solver.scheduling_data.get_edge_weight((i, j))
                    weight_lm = self.changed_binary_math_model_solver.scheduling_data.get_edge_weight((l, m))
                    triple = binary_constraints_latex(i, j, l, m, weight_ij, weight_lm)
                    result.append(triple[0])
                    result.append(triple[1])
                    result.append(triple[2])
        return result

    def get_result_t_table(self):
        variables = []
        values = []
        t_solution = self.changed_binary_math_model_solver.t_solution
        for t in t_solution:
            if t.i != t.j:
                latex = t_ij(t.i, t.j)
            else:
                latex = f"T_{t.i}"
            variables.append(latex2omml(latex))
            values.append(str(int(t.value)))
        return [variables, values]

    def get_result_Y_table(self):
        variables = []
        values = []
        y_solution = self.changed_binary_math_model_solver.y_solution
        for Y in y_solution:
            i, j = Y.task_1
            l, m = Y.task_2
            variables.append(latex2omml(Y_latex(i, j, l, m)))
            values.append(str(int(Y.value)))
        return [variables, values]

    def get_tasks_order_latex(self):
        orders = self.changed_binary_math_model_solver.tasks_order()
        result = []
        for perf in range(len(orders)):
            result.append(f"{perf + 1}: " + f"\\longrightarrow ".join([t_ij(i, j) for i, j in orders[perf]]))
        return result