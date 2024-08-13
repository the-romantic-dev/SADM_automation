from copy import deepcopy

from sympy import Matrix, Expr, Rational

from tasks.task1_2_lp.model.lp_problem.constraint.constraint import Constraint
from tasks.task1_2_lp.model.lp_problem.enums.comp_operator import CompOperator
from tasks.task1_2_lp.model.lp_problem.enums.objective_type import ObjectiveType
from tasks.task1_2_lp.model.lp_problem.objective.objective import Objective


def eye_row_to_cols(matrix: Matrix) -> dict[int, list[int]]:
    def eye_column_one_index(index: int) -> int:
        col: Matrix = matrix.col(index)
        elements = col.T.tolist()[0]
        ones = []
        for j, elem in enumerate(elements):
            if elem == 0:
                continue
            elif elem == 1:
                ones.append(j)
            else:
                return -1
        if len(ones) == 1:
            return ones[0]
        return -1

    result = dict()
    for i in range(matrix.cols):
        eye_elem_row = eye_column_one_index(i)
        if eye_elem_row >= 0:
            if eye_elem_row not in result:
                result[eye_elem_row] = []
            result[eye_elem_row].append(i)
    return result


def inverse_objective_type(obj_type: ObjectiveType):
    result = ObjectiveType.MIN
    if obj_type == ObjectiveType.MIN:
        result = obj_type.MAX
    return result


def inverse_comp_operator(comp_operator: CompOperator, obj_type: ObjectiveType):
    if comp_operator == CompOperator.GE:
        return CompOperator.LE
    elif comp_operator == CompOperator.LE:
        return CompOperator.GE
    else:
        if obj_type == ObjectiveType.MAX:
            return CompOperator.GE
        else:
            return CompOperator.LE


class LPProblem:
    M: int = 100000

    def __init__(self, constraints: list[Constraint], objective: Objective):
        self._constraints = constraints
        self._objective = objective

    @property
    def eye_row_to_cols(self):
        return eye_row_to_cols(self.canonical_form.matrices[0])

    @property
    def eye_rows(self):
        return sorted(list(self.eye_row_to_cols.keys()))

    @property
    def constraints(self):
        return self._constraints

    @property
    def var_count(self):
        return self._objective.vars_count

    @property
    def objective(self):
        return self._objective

    @property
    def matrices(self) -> tuple[Matrix, Matrix, Matrix]:
        """
        Возвращает матрицы (sympy.Matrix):
         - матрицу коэффициентов ограничений A
         - матрицу (вектор) констант b
         - матрицу (вектор) коэффициентов целевой функции
         """
        A = []
        b = []
        c = self._objective.coeffs
        for con in self._constraints:
            A.append(con.coeffs)
            b.append(con.const)

        return Matrix(A), Matrix(b), Matrix(c)

    @property
    def constraints_expressions(self) -> list[Expr]:
        result = []
        for i in self._constraints:
            result.append(i.as_expr)
        return result

    @property
    def is_canonical(self):
        """
        Проверка, является ли форма задачи ЛП канонической
        """
        return self._is_all_eq() and self._is_consts_positive() and self._objective.type == ObjectiveType.MAX

    @property
    def auxiliary_form(self):
        if self.has_simple_start_basis:
            raise ArithmeticError("Не нужно решать вспомогательную задачу")
        eye_rows = self.eye_rows
        A = self.canonical_form.matrices[0]
        artificial_var_indices = [self.canonical_form.var_count + i for i in range(A.rows - len(eye_rows))]

        def non_eye_rows():
            _result = []
            for i in range(A.rows):
                if i not in eye_rows:
                    _result.append(i)
            return _result

        _non_eye_rows = non_eye_rows()
        old_constraints = deepcopy(self.canonical_form.constraints)
        new_constraints = []
        for i, oc in enumerate(old_constraints):
            coeffs = oc.coeffs
            if i not in _non_eye_rows:
                new_coeffs = coeffs + [0 for _ in range(len(artificial_var_indices))]
            else:
                artificial_var_index = artificial_var_indices[_non_eye_rows.index(i)]
                new_coeffs = coeffs + [
                    Rational(0) if self.canonical_form.var_count + j != artificial_var_index else Rational(1) for j in
                    range(len(artificial_var_indices))]
            nc = Constraint(new_coeffs, oc.const, oc.comp_operator)
            new_constraints.append(nc)
        obj_coeffs = [Rational(0) for _ in range(self.canonical_form.var_count)] + [Rational(-1) for _ in
                                                                                    range(len(artificial_var_indices))]
        new_objective = Objective(ObjectiveType.MAX, coeffs=obj_coeffs)
        return LPProblem(constraints=new_constraints, objective=new_objective)

    @property
    def has_simple_start_basis(self):
        rows = len(self.constraints)
        _eye_rows = self.eye_rows
        if len(set(_eye_rows)) != rows:
            return False
        for i in range(1, len(_eye_rows)):
            if _eye_rows[i] - _eye_rows[i - 1] != 1:
                return False
        return True

    @property
    def start_basis(self) -> list[int]:
        if not self.has_simple_start_basis:
            raise ArithmeticError("Чтобы найти базис в ЗЛП должна быть единичная подматрица")
        basis_len = len(self.constraints)
        result = []
        for cols in self.eye_row_to_cols.values():
            result.append(cols[0])
        return result

    def get_dual_problem(self, variable_symbol: str):
        A, b, C = self.matrices

        new_obj_type = inverse_objective_type(self.objective.type)
        new_obj_coeffs = b.T.tolist()[0]
        new_objective = Objective(
            obj_type=new_obj_type,
            coeffs=new_obj_coeffs,
            const=self._objective.const,
            variable_symbol=variable_symbol)

        new_A: list[list[Rational]] = A.T.tolist()
        if self.is_canonical:
            new_A = new_A[:-A.rows]
        new_b = C.T.tolist()[0]
        new_comp_operator = inverse_comp_operator(self.constraints[0].comp_operator, self.objective.type)
        new_constraints = [Constraint(
            coeffs=coeffs,
            const=const,
            comp_operator=new_comp_operator,
            variable_symbol=variable_symbol
        ) for coeffs, const in zip(new_A, new_b)]

        result = LPProblem(
            constraints=new_constraints,
            objective=new_objective
        )
        return result

    @property
    def canonical_form(self):
        """
        Возвращает каноническую форму задачи ЛП. Каноническая форма должна соответствовать следующим критериям:
            - поиск максимума целевой функции
            - неотрицательный вектор констант b
            - все переменные неотрицательные
            - все ограничения представлены равенствами
        """
        if self.is_canonical:
            return self

        new_constraints = []
        total_vars = self.var_count
        for c in self._constraints:
            new_c = c.eq_form(art_var_index=total_vars)
            if new_c.const < 0:
                new_c = -new_c
            if not c.is_eq:
                total_vars += 1
            new_constraints.append(new_c)

        for c in new_constraints:
            c.expand_coefs(total_vars)

        new_objective = deepcopy(self._objective)
        new_objective.expand_coefs(total_vars)
        if new_objective.type == ObjectiveType.MIN:
            new_objective = -new_objective

        return LPProblem(constraints=new_constraints, objective=new_objective)

    def _is_all_eq(self):
        result = True
        for con in self._constraints:
            if con.comp_operator != CompOperator.EQ:
                result = False
                break
        return result

    def _is_consts_positive(self):
        result = True
        for con in self._constraints:
            if con.const < 0:
                result = False
                break
        return result

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        result = [str(self._objective)]
        for c in self._constraints:
            result.append(str(c))

        return "\n".join(result)

    def __repr__(self):
        return str(self)
