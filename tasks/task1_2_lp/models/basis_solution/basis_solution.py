from sympy import symbols, solve, Expr, Add

from tasks.task1_2_lp.models.lp_problem.lp_problem import LPProblem


class BasisSolution:
    def __init__(self, lp_problem: LPProblem, basis: list[int] | tuple[int]):
        self.lp_problem = lp_problem
        self.basis = basis
        self._free = None
        self._free_variables = None

    @property
    def free(self):
        if self._free is not None:
            return self._free
        canonical = self.lp_problem.canonical_form
        vars_indices = [i for i in range(canonical.var_count)]
        free = list(filter(lambda index: index not in self.basis, vars_indices))
        self._free = free
        return free

    @property
    def free_variables(self):
        if self._free_variables is not None:
            return self._free_variables
        result = symbols(" ".join([f"x{i + 1}" for i in self.free]))
        self._free_variables = result
        return result

    @property
    def basis_variables(self):
        return symbols(" ".join([f"x{i + 1}" for i in self.basis]))

    @property
    def basis_expressions(self) -> list[Expr]:
        basis_variables = self.basis_variables
        equations = self.lp_problem.canonical_form.constraints_expressions
        solution_dict = solve(equations, basis_variables)
        result = []
        for b in basis_variables:
            result.append(solution_dict[b])
        return result

    @property
    def objective_expression(self):
        obj = self.lp_problem.objective
        expr = obj.as_expr
        basis_expressions = self.basis_expressions
        objective_vars = expr.free_symbols
        reps = []
        for i, x in enumerate(self.basis_variables):
            if x not in objective_vars:
                continue
            reps.append((x, basis_expressions[i]))
        result = expr.subs(reps)
        return result

    @property
    def objective_expression_coeffs(self):
        e = self.objective_expression
        coeffs = [e.coeff(x) for x in self.free_variables]
        return coeffs

    @property
    def objective_value(self):
        e = self.objective_expression
        const = e
        for x in self.free_variables:
            const = const.subs(x, 0)
        return const

    @property
    def basis_values(self):
        result = []
        for e in self.basis_expressions:
            const = e
            for x in self.free_variables:
                const = const.subs(x, 0)
            result.append(const)
        return result

    @property
    def is_acceptable(self):
        result = True
        for v in self.basis_values:
            if v < 0:
                result = False
                break
        return result

    @property
    def basis_expression_coeffs(self):
        result = []
        for e in self.basis_expressions:
            coeffs = [e.coeff(x) for x in self.free_variables]
            result.append(coeffs)
        return result

    def basis_expression_coeffs_column(self, index):
        result = [row[index] for row in self.basis_expression_coeffs]
        return result

    @property
    def unacceptable_vars_indices(self):
        result = []
        for i, v in enumerate(self.basis_values):
            if v < 0:
                result.append(self.basis[i])
        return result

    @property
    def is_opt(self):
        obj_coeffs = self.objective_expression_coeffs
        result = True
        for c in obj_coeffs:
            if c > 0:
                result = False
                break
        return result
