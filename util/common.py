from sympy import Rational


def remove_dict_keys(dictionary: dict, keys: list):
    for i in keys:
        dictionary.pop(i)


def transpose(matrix: list[list]):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def get_image_dimensions(image_path):
    from PIL import Image
    # Используем библиотеку PIL для получения размеров изображения
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height


def rationalize(data, result=None):
    if result is None:
        result = []
    if isinstance(data, int) or isinstance(data, float):
        result.append(Rational(str(data)))
    elif isinstance(data, list) or isinstance(data, tuple):
        for elem in data:
            rationalize(elem, result)
    else:
        raise TypeError("Рационализировать можно только число или список чисел")

def derationalize(data, result=None):
    if result is None:
        result = []
    if isinstance(data, Rational):
        if Rational.is_integer:
            result.append(int(data))
        else:
            result.append(float(data))
    elif isinstance(data, list) or isinstance(data, tuple):
        for elem in data:
            rationalize(elem, result)
    else:
        raise TypeError("Дерационализировать можно только Rational или список Rational")