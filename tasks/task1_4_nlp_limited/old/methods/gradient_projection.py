import sympy as sp
# from task import Task
import util
from .npp_method import NPPMethod

x1, x2 = sp.symbols('x1 x2')
tol = 1e-7


class GradientProjection(NPPMethod):
    def __init__(self):
        super().__init__()
        self.A0 = None
        self.b = None
        self.report_data = []

    def solve(self, f, limitations):
        self.f = f
        self.limits = limitations
        # Шаг 0. Подходит ли градиент как начальное направление
        X, A0, A, b, gradient, direction = self._gp_step_0(f, limitations)

        while True:
            # Шаг 1. Определение длины шага
            X, limit_index, limitation__step_sizes_num = self._gp_step_1(direction, A0, b, X)

            self.track.append(X)
            self.values_track.append(f.subs({x1: X[0, 0], x2: X[1, 0]}))
            # Шаг 6. Если нет пересечений границ в направлении К, берем  следующим направлением градиент
            if limitation__step_sizes_num == 0:
                raise ValueError("Множество индексов нарушаемых ограничений пустое")
                report_6 = {'step': 5}
                direction = util.gradient(X)
                report_6 = {'gradient_direction': direction}
                self.report_data.append(report_6)
            else:
                # Шаг 2. Формирование новой матрицы активных ограничений
                projection, A = self._gp_step_2(X, A, A0, limit_index)

                # Шаг 3. Проверка останова
                if self.is_projection_zero(projection):
                    report_3 = {'step': 3}
                    lamb = -(A * A.T).inv() * A * util.gradient(X)  # reported
                    report_3['lamb'] = lamb
                    if self.is_lamb_negative_or_zero(lamb):
                        # Шаг 5. Останов
                        self.report_data.append(report_3)
                        break
                    else:
                        # Шаг 4. Модификация матрицы
                        report_3['step'] = 4
                        direction = self.matrix_modification(lamb, A, util.gradient(X))
                        report_3['lamb_direction'] = direction
                        self.report_data.append(report_3)
                else:
                    direction = projection
        self.solution['x1'] = self.track[-1][0, 0]
        self.solution['x2'] = self.track[-1][1, 0]
        self.solution['f'] = f.subs({x1: self.track[-1][0, 0], x2: self.track[-1][1, 0]})

    def _gp_step_0(self, f, limitations):
        X = sp.Matrix([[0], [0]])  # reported
        self.track.append(X)
        A0, b = sp.linear_eq_to_matrix(limitations, [x1, x2])
        self.A0 = A0
        self.b = b
        A = A0[2:4, :]  # reported
        gradient = util.gradient(X)
        direction = None
        self.values_track.append(f.subs({x1: X[0, 0], x2: X[1, 0]}))
        if self.is_gradient_direction_fits(A, gradient):
            direction = gradient  # reported
        else:
            raise ValueError("Градиент не подходит как начальное направление. Меняй алгоритм")
        self.report_data.append({"step": 0, "start_x": X, "A": A, "gradient": gradient})
        return X, A0, A, b, gradient, direction

    def _gp_step_1(self, direction, A0, b, X):
        report_1 = {"step": 1}
        step_size, limit_index, limitation__step_sizes_num = self.step_size(direction, A0, b, X, report_1)  # step_size reported
        report_1["result_step_size"] = step_size
        X = X + step_size * direction  # reported
        report_1["Xi+1"] = X
        self.report_data.append(report_1)
        return X, limit_index, limitation__step_sizes_num

    def _gp_step_2(self, X, A, A0, limit_index):
        report_2 = {'step': 2}
        report_2['limit_index'] = limit_index
        if limit_index >= 0:
            A = A0.row(limit_index)
        # A reported
        report_2['newA'] = A
        gradient = util.gradient(X)  # reported
        report_2['new_grad'] = gradient
        projection = self.projection_operator(A) * gradient  # reported + self.projection_operator(A)
        report_2['P'] = self.projection_operator(A)
        report_2['K'] = projection
        self.report_data.append(report_2)
        return projection, A

    def report(self, output_func):
        output_func("|---------------------------------------------------------|")
        output_func("|-----------ОТЧЕТ ПО МЕТОДУ ПРОЕКЦИИ ГРАДИЕНТА------------|")
        output_func("|---------------------------------------------------------|")
        for data in self.report_data:
            match data['step']:
                case 0:
                    self.report_0(data, output_func)
                case 1:
                    self.report_1(data, output_func)
                case 2:
                    self.report_2(data, output_func)
                case 3:
                    self.report_3(data, output_func)

    def report_0(self, data, output_func):
        output_func("\nШаг 0")
        output_func(f"Начальная точка:\n{data['start_x']}\n")
        output_func(f"Активные ограничения:\n{data['A']}\n")
        output_func(f"А * gradient:\n{data['A'] * data['gradient']}\n")
        output_func(f"Направление:\n{data['gradient']}\n")

    def report_1(self, data, output_func):
        output_func("\nШаг 1")
        output_func(f"A0:\n{sp.pretty(self.A0)}\n")
        output_func(f"A0 * K:\n{data['limitation_vector']}\n")
        output_func(f"I_пред:\n{data['t_пред_i'].keys()}\n")
        output_func(f"t* = {data['t*']}\n")
        for i in data['t_пред_i'].keys():
            output_func(f"t_{i + 1} = {data['t_пред_i'][i]}")
        output_func()
        output_func(f"Итоговый шаг: {data['result_step_size']}\n")
        output_func(f"Новая точка:\n{data['Xi+1']}\n")

    def report_2(self, data, output_func):
        output_func("\nШаг 2")
        output_func(f"Номер текущего ограничения: {data['limit_index']}\n")
        output_func(f"Градиент: {data['new_grad']}\n")
        output_func(f"Новое А:\n{sp.pretty(data['newA'])}\n")
        output_func(f"Новое P:\n{sp.pretty(data['P'])}\n")
        output_func(f"Новое K:\n{sp.pretty(data['K'])}\n")

    def report_3(self, data, output_func):
        output_func("\nШаг 3")
        output_func(f"Лямбда:\n{data['lamb']}")

    def is_gradient_direction_fits(self, A, gradient):
        """Функция проверяет, подходит ли как начальное направление градиент"""
        result = True
        condition_matrix = A * gradient  # reported
        for i in range(condition_matrix.shape[0]):
            if condition_matrix[i, 0] > 0:
                result = False
                break
        return result

    def matrix_modification(self, lamb, A, gradient):
        modified_matricies = []
        for i in range(lamb.shape[0]):

            l = lamb[i, 0]
            if l > 0:
                A_copy = A.copy()
                A_copy.row_del(i)
                modified_matricies.append(A_copy)
        result_direction = sp.Matrix([0, 0])
        for matrix in modified_matricies:
            projection = self.projection_operator(matrix) * gradient
            if projection.norm() > result_direction.norm():
                result_direction = projection
        return result_direction

    def projection_operator(self, A):
        return sp.eye(2) - A.T * (A * A.T).inv() * A

    def is_projection_zero(self, projection):
        return projection.norm() < tol

    def is_lamb_negative_or_zero(self, lamb):
        result = True
        tol = 1e-1
        for i in range(lamb.shape[0]):
            if lamb[i, 0] > tol:
                result = False
                break
        return result

    def step_size(self, direction, A0, b, X, report_1):
        step_sizes = self.limitation_step_sizes(A0, b, direction, X, report_1)  # reported
        default_step_size = self.default_step_size(X, direction)  # reported
        limitations_steps_sizes_num = len(step_sizes)
        report_1["t*"] = default_step_size
        report_1["t_пред_i"] = step_sizes

        step_sizes[-1] = default_step_size
        min_step_size = 10000000
        min_step_size_index = -2
        for i, size in step_sizes.items():
            if size < min_step_size:
                min_step_size = size
                min_step_size_index = i
        return (min_step_size, min_step_size_index, limitations_steps_sizes_num)

    def default_step_size(self, X, direction):
        gradient = util.gradient(X)
        gesse = util.gesse()

        a = gradient.T * direction
        b = direction.T * gesse * direction
        return -a.det() / b.det()

    def limitation_step_sizes(self, A0, b, direction, X, report_1):
        vector = A0 * direction
        report_1["limitation_vector"] = vector
        result = {}
        for i in range(vector.shape[0]):
            if vector[i, 0] > 0:
                result[i] = (b[i, 0] - (A0.row(i) * X).det()) / (A0.row(i) * direction).det()
        return result
