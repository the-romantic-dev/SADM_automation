import sympy as sp

def create_main_expression(C):
    """Создает из коэффициентов главное символьное уравнение задачи"""
    f = C[0] * x1**2 + C[1] * x2**2 + C[2] * x1 * x2 + C[3] * x1 + C[4] * x2
    return f

x1, x2 = sp.symbols('x1 x2')
tol = 1e-1
C = [-3, -3, 0, 1, 1]
expr = create_main_expression(C)
folder = "D:/Убежище/Университет/5 семестр/СисАнал/Заказы/Расчетка 4/Онлайн"
print(folder)