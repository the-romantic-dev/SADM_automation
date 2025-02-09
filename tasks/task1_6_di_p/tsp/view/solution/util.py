from report.model.docx_parts.formula import Formula
from report.model.docx_parts.table import Table
from tasks.task1_6_di_p.tsp.model.report_dataclasses import TSPReportDataLast, TSPReportData


def paths_way_to_latex(paths_way):
    result = []
    for path in paths_way:
        if path[1]:
            result.append(str((path[0][0] + 1, path[0][1] + 1)))
        else:
            result.append(f"\\left( \\overline{{ {path[0][0] + 1}, {path[0][1] + 1} }} \\right)")
    str_res = "()"
    if len(result) > 0:
        str_res = ",".join(result)
    return str_res


def get_previous_G_latex(report_data: TSPReportData | TSPReportDataLast) -> str:
    paths_way = report_data.paths_way
    data = paths_way
    under_latex = paths_way_to_latex(data)
    if under_latex == "()":
        return f"G^{{ ({report_data.tree_level})}}"
    else:
        return f"G_{{ {under_latex} }}^{{ ({report_data.tree_level})}}"


def get_exclude_G_latex(report_data: TSPReportData) -> str:
    paths_way = report_data.paths_way
    worst_tau = report_data.worst_tau
    data = paths_way + [(worst_tau[0], False)]
    return f"G_{{ {paths_way_to_latex(data)} }}^{{ ({report_data.tree_level + 1})}}"


def get_include_G_latex(report_data: TSPReportData):
    paths_way = report_data.paths_way
    worst_tau = report_data.worst_tau
    data = paths_way + [(worst_tau[0], True)]
    return f"G_{{ {paths_way_to_latex(data)} }}^{{ ({report_data.tree_level + 1})}}"


def matrix_to_table(matrix):
    table_data = []

    row_indices = sorted(matrix.keys())
    column_indices = list(sorted(matrix[row_indices[0]].keys()))

    table_data.append(["-"] + [Formula(str(j + 1)) for j in column_indices])

    for i in row_indices:
        row = [Formula(f'{i + 1}')]
        for j in column_indices:
            elem = matrix[i][j]
            latex_elem = "\\infty" if elem > 10 ** 7 else str(elem)
            row.append(Formula(latex_elem))
        table_data.append(row)
    fill_color = '#FFE699'
    color_fills = ({(0, 0): fill_color} |
                   {(0, j + 1): fill_color for j in range(len(column_indices))} |
                   {(i + 1, 0): fill_color for i in range(len(row_indices))})
    return Table(table_data, color_fills)
