from report.docx.omml import latex2omml
from tasks.scheduling_theory.solvers.scheduling_problem.scheduling_problem_solver import SchedulingProblemSolver, \
    SchedulingStep


def get_vector_latex(vector: list[str]):
    joiner = r'\\'
    return f"\\begin{{matrix}} {joiner.join(vector)} \\end{{matrix}}"


def dict_to_vector_data(d: dict):
    result = []
    for i in d:
        value = "-"
        if d[i] is not None:
            value = d[i]
        result.append(f"{i}:{value}")
    return result

def omml_or_tide(data: list, latex: str):
    if len(data) == 0:
        return "-"

    return latex2omml(latex)


def make_row(row_data: SchedulingStep):
    result = [
        latex2omml(str(row_data.T)),
        ', '.join([str(i) for i in row_data.E]),
        ', '.join([str(i) for i in row_data.D]), latex2omml(
            get_vector_latex(
                dict_to_vector_data(row_data.N)
            )
        ),
        omml_or_tide(row_data.W, get_vector_latex([f"{i}{j}" for i, j in row_data.W])),
        # latex2omml(
        #     get_vector_latex([f"{i}{j}" for i, j in row_data.W])
        # ),
        omml_or_tide(row_data.A, get_vector_latex([f"{i}" for i in row_data.A])),
        # latex2omml(
        #     get_vector_latex([f"{i}" for i in row_data.A])
        # ),
        omml_or_tide(row_data.R, get_vector_latex([f"{i}" for i in row_data.R])),
        # latex2omml(
        #     get_vector_latex([f"{i}" for i in row_data.R])
        # ),
        omml_or_tide(row_data.V, get_vector_latex([f"{i}" for i in row_data.V])),
        # latex2omml(
        #     get_vector_latex([f"{i}" for i in row_data.V])
        # ),
        latex2omml(
            get_vector_latex(
                dict_to_vector_data(row_data.B)
            )
        ),
        latex2omml(
            get_vector_latex(
                dict_to_vector_data(row_data.L)
            )
        )]
    return result


class SchedulingProblemData:
    def __init__(self, scheduling_problem_solver: SchedulingProblemSolver):
        self.scheduling_problem_solver = scheduling_problem_solver
        self.scheduling_data = scheduling_problem_solver.scheduling_data

    def get_downtimes_formulas(self, rule_index: int):
        downtimes_intervals = self.scheduling_problem_solver.downtime_intervals[rule_index]
        result = []
        for p in downtimes_intervals:
            durations = [end - start for start, end in downtimes_intervals[p]]
            durations_str = [str(i) for i in durations]
            if len(durations) > 1:
                latex = f"{p}: {'+'.join(durations_str)} = {sum(durations)}"
            else:
                latex = f"{p}: {sum(durations)}"
            result.append(latex)
        return result

    def get_calculation_table(self, solution_index):
        header_row = [
            "T", "E", "D", "N", "W", "A", "R", "V", "B", "L"
        ]
        header_row = [latex2omml(elem) for elem in header_row]
        result = [header_row]
        data_rows = self.scheduling_problem_solver.solution_steps_per_rule[solution_index]
        for row in data_rows:
            result.append(make_row(row))

        return result
