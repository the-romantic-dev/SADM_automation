from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from sympy import Rational, Symbol, Expr
from report.docx.omml import sympy2omml, latex2omml
from typing import List
from docx.document import Document as DocumentType
from docx.table import Table, _Cell
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml.etree import _Element


def paint_table_row(table, row_index, color='FFE699'):
    for _, cell in enumerate(table.rows[row_index].cells):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)


def paint_table_column(table, column_index, color='FFE699'):
    for _, cell in enumerate(table.columns[column_index].cells):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)


def paint_table_cell(table, row_index, column_index, color='FFE699'):
    column_size = len(table.columns)
    for i, cell in enumerate(table.rows[row_index].cells):
        if 0 <= column_index == i or (column_index < 0 and i == column_size + column_index):
            shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
            cell._tc.get_or_add_tcPr().append(shading_elm)
            break


def fill_table(table, data: List[List], alignment='center'):
    if len(table.rows) != len(data):
        raise IndexError("Количество строк в util не совпадает с количеством строк в таблице")
    for i, row in enumerate(data):
        for j, cell_value in enumerate(row):
            cell = table.cell(i, j)
            run = cell.paragraphs[0].add_run()
            if isinstance(cell_value, Rational) or isinstance(cell_value, Symbol) or isinstance(cell_value, Expr):
                run.element.append(sympy2omml(cell_value))
            elif isinstance(cell_value, str):
                # run.element.append(latex2omml(cell_value))
                run.text = cell_value

            elif isinstance(cell_value, _Element):
                run.element.append(cell_value)
            else:
                cell.text = str(cell_value)
            match alignment:
                case 'center':
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                case 'left':
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
                case 'right':
                    cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT


def create_table(document: DocumentType, rows: int, cols: int):
    result = document.add_table(rows, cols)
    result.style = 'Table Grid'
    return result


def create_table_filled(
        document: DocumentType,
        data: List[List],
        alignment='center'
):
    max_row_len = -1
    for row in data:
        if len(row) > max_row_len:
            max_row_len = len(row)

    result = create_table(document, len(data), max_row_len)
    fill_table(table=result, data=data, alignment=alignment)
    return result


def _make_table_from_child_document(child, document):
    table = Table(child, document)
    table.style = 'Table Grid'
    for row in table.rows:
        for cell in row.cells:
            set_cell_border(
                cell,
                top={'sz': 2, 'val': 'single', 'color': '#000000'},
                bottom={'sz': 2, 'val': 'single', 'color': '#000000'},
                start={'sz': 2, 'val': 'single', 'color': '#000000'},
                end={'sz': 2, 'val': 'single', 'color': '#000000'}
            )
    return table


def set_cell_border(cell: _Cell, **kwargs):
    """
    Set cell`s border
    Usage:

    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        start={"sz": 24, "val": "dashed", "shadow": "true"},
        end={"sz": 12, "val": "dashed"},
    )
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    # check for tag existnace, if none found, then create one
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)

    # list over all available tags
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)

            # check for tag existnace, if none found, then create one
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))
