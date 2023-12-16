from sympy import Matrix,symbols, solve, Eq

def reverse_canonical(canonical):
    reversed_canonical = {}
    reversed_canonical['C'] = canonical['B'][:]
    reversed_canonical['B'] = canonical['C'][:]
    reversed_canonical['A'] = transpose_matrix(canonical['A'])
    return reversed_canonical
    
def transpose_matrix(matrix):
    # Определение числа строк и столбцов в исходной матрице
    rows = len(matrix)
    cols = len(matrix[0])

    # Создаем новую пустую матрицу для результатов с переключенными строками и столбцами
    transposed_matrix = [[0 for _ in range(rows)] for _ in range(cols)]

    # Транспонирование матрицы
    for i in range(rows):
        for j in range(cols):
            transposed_matrix[j][i] = matrix[i][j]

    return transposed_matrix

def conjugate_points(base, canonical):
    A_i = [[item[j] for j in range(len(item)) if j in base] for item in canonical['A']]
    C_i = [canonical['C'][i] for i in range(len(canonical['C'])) if i in base]
    AT_i = transpose_matrix(A_i)
    y1, y2 = symbols('y1 y2')
    
    equations = Eq(Matrix(AT_i) * Matrix([y1, y2]), Matrix(C_i))
    solutions = solve(equations, (y1, y2))
    return {
        "A_i": A_i, 
        "AT_i": AT_i,
        "C_i": C_i,
        "y1": solutions[y1],
        "y2": solutions[y2]
    }
    