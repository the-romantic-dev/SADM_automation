import math

import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, PULP_CBC_CMD

from tasks.scheduling_theory.solvers.math.data_classes import VariableSolutionData, BinaryVariableSolutionData
from tasks.scheduling_theory.scheduling_data import SchedulingData
from tasks.scheduling_theory.solvers.math.math_moments_constraints_data import MathModelConstraintsData


class DefaultMathModelSolver:
    def __init__(self, scheduling_data: SchedulingData, constraints_data: MathModelConstraintsData):
        self.scheduling_data: SchedulingData = scheduling_data
        self.constraints_data = constraints_data
        self.solution = self.solve_model()
        self.total_time = self.solution[-1].value

    def _generate_variables(self):
        result = {}
        edges = self.scheduling_data.get_edges()
        for edge in edges:
            i, j = edge
            t_var = LpVariable(name=f"t_{i}{j}", lowBound=0, cat="Integer")
            result[edge] = t_var
        last_node = self.scheduling_data.last_node
        result[(last_node, last_node)] = LpVariable(name=f"T", lowBound=0, cat="Integer")
        return result

    def _generate_constraints(self, variables):
        result = []
        for constraint in self.constraints_data.task_time_constraints_data:
            li_edge = (constraint.l, constraint.i)
            ij_edge = (constraint.i, constraint.j)
            weight = constraint.li_weight
            t_li = variables[li_edge]
            t_ij = variables[ij_edge]
            result.append(t_ij >= t_li + weight)

        for constraint in self.constraints_data.total_time_constraints_data:
            lM_edge = (constraint.l, constraint.M)
            MM_edge = (constraint.M, constraint.M)
            T_M = variables[MM_edge]
            t_lM = variables[lM_edge]
            weight = constraint.lM_weight
            result.append(T_M >= t_lM + weight)
        return result

    def get_model(self):
        variables = self._generate_variables()
        objective = sum(variables.values())
        constraints = self._generate_constraints(variables)
        return variables, objective, constraints

    def solve_model(self):
        problem = LpProblem(name="Найти наиболее ранние моменты начала работ", sense=LpMinimize)

        # variables = self._generate_variables()
        # objective = sum(variables.values())
        # constraints = self._generate_constraints(variables)
        variables, objective, constraints = self.get_model()

        problem += objective
        for c in constraints:
            problem += c

        problem.solve(PULP_CBC_CMD(msg=False))

        result = []
        for var in variables:
            result.append(
                VariableSolutionData(
                    i=var[0],
                    j=var[1],
                    value=variables[var].value(),
                    name="t"
                )
            )
        return result


class IntensiveMathModelSolver:
    def __init__(self, scheduling_data: SchedulingData, default_math_model_solver: DefaultMathModelSolver,
                 is_sidnev: bool):
        self.scheduling_data: SchedulingData = scheduling_data
        self.default_total_time = default_math_model_solver.total_time
        if is_sidnev:
            w = 0.75
        else:
            w = scheduling_data.intensity_limit
        self.t_solution, self.m_solution, self.T_result = self.solve_intensive_model(is_sidnev=is_sidnev, w=w)

    def solve_intensive_model(self, is_sidnev: bool, w: float):
        from scipy.optimize import minimize
        all_edges = self.scheduling_data.get_edges()
        last_node = self.scheduling_data.last_node
        last_incoming_nodes = self.scheduling_data.get_incoming_nodes(last_node)
        max_i = last_node + 1
        linear_indices = [edge[0] * max_i + edge[1] for edge in all_edges]

        def get_linear_index_by_ij(i, j):
            return linear_indices.index(i * max_i + j)

        def get_ij_by_linear_index(index):
            ij = linear_indices[index]
            i = ij // max_i
            j = ij % max_i
            return i, j

        def obj_expression(m_tau):
            if is_sidnev:
                tau = m_tau[len(m_tau) // 2 + 1:]
                T = m_tau[len(m_tau) // 2]
                return sum(tau) + T
            else:
                m = m_tau[:len(m_tau) // 2]
                return sum(m)

        def constraints_expressions(m_tau):
            m = m_tau[:len(m_tau) // 2]
            tau = m_tau[len(m_tau) // 2 + 1:]
            T = m_tau[len(m_tau) // 2]
            if is_sidnev:
                constraints = [w * len(all_edges) - sum(m)]
            else:
                constraints = [w * self.default_total_time - T]
            nodes = self.scheduling_data.nodes
            for i in nodes:
                if i == 1 or i == last_node:
                    continue
                outcoming_nodes = self.scheduling_data.get_outcoming_nodes(i)
                incoming_nodes = self.scheduling_data.get_incoming_nodes(i)
                for j in outcoming_nodes:
                    for l in incoming_nodes:
                        li_edge = (l, i)
                        Q = self.scheduling_data.get_edge_weight(li_edge)
                        linear_ij = get_linear_index_by_ij(i, j)
                        linear_li = get_linear_index_by_ij(l, i)
                        constraint = tau[linear_ij] - tau[linear_li] - Q / m[linear_li]
                        constraints.append(constraint)
            for l in last_incoming_nodes:
                M = last_node
                edge = (l, M)
                Q = self.scheduling_data.get_edge_weight(edge)
                linear_lM = get_linear_index_by_ij(l, M)
                constraint = T - tau[linear_lM] - Q / m[linear_lM]
                constraints.append(constraint)
            return constraints

        initial_guess = np.ones(len(all_edges) * 2 + 1)
        bounds = [(0, None)] * len(initial_guess)
        solution = minimize(
            fun=obj_expression,
            x0=initial_guess,
            constraints={'type': 'ineq', 'fun': constraints_expressions},
            bounds=bounds)
        t_result = []
        m_result = []
        for index in range(len(all_edges)):
            i, j = get_ij_by_linear_index(index)
            m_value = round(solution.x[:len(solution.x) // 2][index], 4)
            t_value = round(solution.x[len(solution.x) // 2 + 1:][index], 4)
            m_var = VariableSolutionData(i=i, j=j, value=m_value, name="m")
            t_var = VariableSolutionData(i=i, j=j, value=t_value, name="t")
            m_result.append(m_var)
            t_result.append(t_var)
        T_result = round(solution.x[len(solution.x) // 2], 4)
        return t_result, m_result, T_result


class BinaryMathModelSolver:

    def __init__(self, scheduling_data: SchedulingData):
        self.scheduling_data = scheduling_data
        self.task_allocation = self._allocate_tasks()

    def _allocate_tasks(self):
        tasks = self.scheduling_data.get_edges()
        performers_number = self.scheduling_data.performers_number

        allocation = [[] for _ in range(performers_number)]
        for i in range(len(tasks)):
            allocation[i % performers_number].append(tasks[i])
        return allocation

    def comb(self, performer_index):
        k = 2
        n = len(self.task_allocation[performer_index])
        return math.comb(n, k)

    def combs_sum(self):
        return sum([self.comb(i) for i in range(len(self.task_allocation))])

    def constraints_num(self):
        return 3 * self.combs_sum()

    def variables_num(self):
        return 2 * self.combs_sum()


class ChangedBinaryMathModelSolver:
    def __init__(self, scheduling_data: SchedulingData, default_math_model_solver: DefaultMathModelSolver):
        self.scheduling_data = scheduling_data
        self.task_allocation = self._allocate_tasks()
        self.default_math_model_solver = default_math_model_solver
        self.t_solution, self.y_solution = self.solve_task()

    def tasks_order(self):
        order_dict = {}
        y_ones: list[BinaryVariableSolutionData] = list(filter(lambda elem: elem.value == 1, self.y_solution))
        for y in y_ones:
            if y.task_1 not in order_dict:
                order_dict[y.task_1] = 0
            if y.task_2 not in order_dict:
                order_dict[y.task_2] = 0
            order_dict[y.task_1] += 1
            order_dict[y.task_2] -= 1
        result_order = sorted(order_dict.keys(), key=lambda elem: order_dict[elem], reverse=True)
        return result_order

    def _allocate_tasks(self):
        tasks = self.scheduling_data.get_edges()
        return tasks[:3]

    def _generate_binary_variables(self):
        y_variables = {}
        allocation_size = len(self.task_allocation)
        for a in range(allocation_size):
            for b in range(a + 1, allocation_size):
                i, j = self.task_allocation[a]
                l, m = self.task_allocation[b]
                y_var_1 = LpVariable(name=f"Y_{i}{j}_{l}{m}", cat="Binary")
                y_variables[((i, j), (l, m))] = y_var_1
                y_var_2 = LpVariable(name=f"Y_{l}{m}_{i}{j}", cat="Binary")
                y_variables[((l, m), (i, j))] = y_var_2
        return y_variables

    def _generate_binary_constraints(self, t_variables, y_variables):
        result = []
        allocation_size = len(self.task_allocation)
        M = 1000
        for a in range(allocation_size):
            for b in range(a + 1, allocation_size):
                i, j = self.task_allocation[a]
                l, m = self.task_allocation[b]
                y_ij_lm = y_variables[((i, j), (l, m))]
                y_lm_ij = y_variables[((l, m), (i, j))]
                t_ij = t_variables[(i, j)]
                t_lm = t_variables[(l, m)]
                weight_ij = self.scheduling_data.get_edge_weight((i, j))
                weight_lm = self.scheduling_data.get_edge_weight((l, m))
                result.append((M + weight_lm) * y_ij_lm + (t_ij - t_lm) >= weight_lm)
                result.append((M + weight_ij) * y_lm_ij + (t_lm - t_ij) >= weight_ij)
                result.append(y_ij_lm + y_lm_ij == 1)
        return result

    def solve_task(self):
        problem = LpProblem(name="Найти наиболее ранние моменты начала работ", sense=LpMinimize)

        t_variables, objective, t_constraints = self.default_math_model_solver.get_model()

        y_variables = self._generate_binary_variables()
        y_constraints = self._generate_binary_constraints(t_variables, y_variables)

        problem += objective
        for c in t_constraints:
            problem += c

        for c in y_constraints:
            problem += c
        problem.solve(PULP_CBC_CMD(msg=False))

        t_solution = []
        for var in t_variables:
            t_solution.append(
                VariableSolutionData(
                    i=var[0],
                    j=var[1],
                    value=t_variables[var].value(),
                    name="t"
                )
            )
        y_solution = []
        for var in y_variables:
            y_solution.append(
                BinaryVariableSolutionData(
                    task_1=var[0],
                    task_2=var[1],
                    value=y_variables[var].value(),
                    name="y"
                )
            )
        return t_solution, y_solution
