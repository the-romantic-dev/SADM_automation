from copy import deepcopy

from sympy import Matrix, Expr, Rational, symbols, Symbol, Mul

from tasks.task1_2_lp.model import Constraint
from tasks.task1_2_lp.model import CompOperator
from tasks.task1_2_lp.model import ObjectiveType
from tasks.task1_2_lp.model import Objective


def map_rows_to_identity_columns(matrix: Matrix) -> dict[int, list[int]]:
    """
        Анализирует столбцы переданной матрицы и определяет те, которые содержат
        одну единственную единицу ('1'), а остальные элементы равны нулю ('0'),
        аналогично столбцам единичной матрицы. Функция возвращает словарь, который
        отображает индекс строки (где находится '1') в список индексов столбцов,
        соответствующих данному шаблону.

        Параметры:
        ----------
        matrix : sympy.Matrix
            Матрица, которую нужно проанализировать. Предполагается, что этот
            объект поддерживает методы для доступа к отдельным столбцам и
            определения размеров матрицы.

        Возвращает:
        -----------
        dict[int, list[int]]
            Словарь, где каждый ключ — это индекс строки, а соответствующее
            значение — список индексов столбцов. Каждый столбец в списке
            содержит ровно одну '1', а остальные значения столбца равны '0'.
            Если для строки нет подходящих столбцов, она не будет присутствовать
            в словаре.

        Пример:
        -------
        Для следующей матрицы:

            1 0 0 1\n
            0 1 0 0\n
            0 0 1 0

        Функция вернет:

            {0: [0, 3], 1: [1], 2: [2]}
        """

    def find_identity_row_for_column(col_index: int) -> int:
        col: Matrix = matrix.col(col_index)
        ones = []
        for j, elem in enumerate(col.T.tolist()[0]):
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
        eye_elem_row = find_identity_row_for_column(i)
        if eye_elem_row >= 0:
            if eye_elem_row not in result:
                result[eye_elem_row] = []
            result[eye_elem_row].append(i)
    return result


def inverse_objective_type(obj_type: ObjectiveType):
    """Меняет тип целевой функции на противоположный"""
    result = ObjectiveType.MIN
    if obj_type == ObjectiveType.MIN:
        result = obj_type.MAX
    return result


def inverse_comp_operator(comp_operator: CompOperator, obj_type: ObjectiveType):
    """Меняет тип оператора сравнения на противоположный"""
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
    M: Symbol = symbols('M')

    def __init__(self, constraints: list[Constraint], objective: Objective):
        self._constraints = constraints
        self._objective = objective

    @property
    def identity_rows(self):
        rows = map_rows_to_identity_columns(self.canonical_form.matrices[0]).keys()
        return sorted(list(rows))

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
         - матрицу (вектор) коэффициентов целевой функции C
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
        modified_lpp = self.modified_form
        obj_coeffs = [Rational(-1) if coeff == -self.M else Rational(0) for coeff in modified_lpp.objective.coeffs]
        return LPProblem(
            constraints=modified_lpp.constraints,
            objective=Objective(obj_type=modified_lpp.objective.type, coeffs=obj_coeffs)
        )

    @property
    def modified_form(self):
        if self.has_simple_start_basis:
            raise ArithmeticError("Не нужно решать вспомогательную задачу")
        A = self.canonical_form.matrices[0]
        non_identity_rows = [i for i in range(A.rows) if i not in self.identity_rows]
        artificial_var_indices = [self.canonical_form.var_count + i for i in range(len(non_identity_rows))]

        old_constraints = deepcopy(self.canonical_form.constraints)
        new_constraints = []
        for i, oc in enumerate(old_constraints):
            coeffs = oc.coeffs
            if i not in non_identity_rows:
                new_coeffs = coeffs + [0 for _ in range(len(artificial_var_indices))]
            else:
                artificial_var_index = artificial_var_indices[non_identity_rows.index(i)]
                new_coeffs = coeffs + [
                    Rational(0) if self.canonical_form.var_count + j != artificial_var_index else Rational(1) for j in
                    range(len(artificial_var_indices))]
            nc = Constraint(new_coeffs, oc.const, oc.comp_operator)
            new_constraints.append(nc)
        obj_coeffs = self.canonical_form.objective.coeffs + [-self.M for _ in range(len(artificial_var_indices))]
        new_objective = Objective(inverse_objective_type(self.objective.type), coeffs=obj_coeffs)
        return LPProblem(constraints=new_constraints, objective=new_objective)

    @property
    def has_simple_start_basis(self):
        rows = len(self.constraints)
        _eye_rows = self.identity_rows
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
        identity_columns = map_rows_to_identity_columns(self.canonical_form.matrices[0]).values()
        for cols in identity_columns:
            result.append(cols[0])
        return result[:basis_len]

    def get_dual_problem(self, variable_symbol: str):
        def new_objective(_b) -> Objective:
            new_obj_type = inverse_objective_type(self.objective.type)
            new_obj_coeffs = _b.T.tolist()[0]
            return Objective(
                obj_type=new_obj_type,
                coeffs=new_obj_coeffs,
                const=self._objective.const,
                variable_symbol=variable_symbol)

        def new_constraints(_A, _C):
            new_A: list[list[Rational]] = _A.T.tolist()
            new_b = _C.T.tolist()[0]
            new_comp_operator = inverse_comp_operator(self.constraints[0].comp_operator, self.objective.type)
            return [Constraint(
                coeffs=coeffs,
                const=const,
                comp_operator=new_comp_operator,
                variable_symbol=variable_symbol
            ) for coeffs, const in zip(new_A, new_b)]

        if self.is_canonical:
            A, b, C = self.canonical_form.matrices

        else:
            A, b, C = self.matrices

        result = LPProblem(
            constraints=new_constraints(A, C),
            objective=new_objective(b)
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
