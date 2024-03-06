def remove_dict_keys(dictionary: dict, keys: list):
    for i in keys:
        dictionary.pop(i)


def transpose(matrix: list[list]):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]
