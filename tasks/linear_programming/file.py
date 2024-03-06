# pylint: skip-file

input = "input.txt"
output = "output.txt"

def read_input():
    """Читает файл"""
    result = [[], [], [], [], []]
    with open(input, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("C = "):
                C = [float(item) for item in line.split("=")[1].split()]
                result[3] = C
            elif line.startswith("A1 = "):
                A1 = [float(item) for item in line.split("=")[1].split()]
                result[0] = A1
            elif line.startswith("A2 = "):
                A2 = [float(item) for item in line.split("=")[1].split()]
                result[1] = A2
            elif line.startswith("B = "):
                B = [float(item) for item in line.split("=")[1].split()]
                result[2] = B
            elif line.startswith("Препод:"):
                teacher = line.split(":")[1]
                result[4] = teacher
        return result

def add_output(string):
    with open(output, "a", encoding="utf-8") as file:
        file.write(string + "\n")
    
def clear_output():
    open(output, 'w').close()
