import re
from enum import Enum

import lxml.etree
from lxml import etree as lxml_etree
from lxml.etree import _Element
from sympy import Matrix

from report.docx.docx_namespaces import m as m_ns
from report.docx.docx_namespaces import w as w_ns
from report.docx.omml import latex2omml
from report.model.report_prettifier import rational_latex


class BraceType(Enum):
    PARENTHESES = 0
    BRACKETS = 1
    STRAIGHT = 2
    CURLY = 3
    LEFT_CURLY = 4


def is_math_element(element):
    return element.tag == f"{{{m_ns}}}oMath"


def braces(math_element: _Element, brace_type: BraceType = BraceType.PARENTHESES) -> _Element:
    if not is_math_element(math_element):
        raise ValueError("Элемент не является частью уравнения Word")

    brace_elements = element_from_string_with_namespaces(
        xml="""
        <m:begChr/>
        <m:endChr/>""",
        namespaces={'m': m_ns}
    )
    match brace_type:
        case BraceType.BRACKETS:
            brace_elements[0].set(f"{{{m_ns}}}val", "[")
            brace_elements[1].set(f"{{{m_ns}}}val", "]")
        case BraceType.STRAIGHT:
            brace_elements[0].set(f"{{{m_ns}}}val", "|")
            brace_elements[1].set(f"{{{m_ns}}}val", "|")
        case BraceType.CURLY:
            brace_elements[0].set(f"{{{m_ns}}}val", "{")
            brace_elements[1].set(f"{{{m_ns}}}val", "}")
        case BraceType.LEFT_CURLY:
            brace_elements[0].set(f"{{{m_ns}}}val", "{")
            brace_elements[1].set(f"{{{m_ns}}}val", "")
        case _:
            brace_elements = []

    md: _Element = lxml_etree.Element(f'{{{m_ns}}}d')
    me: _Element = lxml_etree.Element(f'{{{m_ns}}}e')
    omath: _Element = lxml_etree.Element(f'{{{m_ns}}}oMath')
    dPr = element_from_string_with_namespaces(
        xml="""
            <m:dPr>
                <m:ctrlPr>
                    <w:rPr>
                        <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math" />
                        <w:i />
                    </w:rPr>
                </m:ctrlPr>
            </m:dPr>
        """,
        namespaces={'m': m_ns, 'w': w_ns}
    )[0]
    if len(brace_elements) > 0:
        dPr.insert(0, brace_elements[1])
        dPr.insert(0, brace_elements[0])
    for child in math_element.iterchildren():
        me.append(child)
    md.append(dPr)
    md.append(me)
    omath.append(md)
    return omath


def element_from_string_with_namespaces(xml: str, namespaces: dict[str, str]):
    namespace_attributes = " ".join([f"xmlns:{key}=\"{value}\"" for key, value in namespaces.items()])
    rooted_xml = f"""
            <root {namespace_attributes}>
                {xml}
            </root>
    
    """
    root_element = lxml_etree.fromstring(rooted_xml)
    parsed_elements = []
    for elem in root_element.iterchildren():
        parsed_elements.append(elem)
    return parsed_elements


def elements_list_to_matrix_element(elements: list[list[_Element]], alignment: str):
    oMath = lxml_etree.Element(f"{{{m_ns}}}oMath")
    m = lxml_etree.SubElement(oMath, f"{{{m_ns}}}m")

    cols = len(elements[0])
    mPr = element_from_string_with_namespaces(
        xml=f"""
            <m:mPr>
                <m:mcs>
                    <m:mc>
                        <m:mcPr>
                            <m:count m:val="{cols}" />
                            <m:mcJc m:val="{alignment}" />
                        </m:mcPr>
                    </m:mc>
                </m:mcs>
                <m:ctrlPr>
                    <w:rPr>
                        <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math" />
                        <w:i />
                    </w:rPr>
                </m:ctrlPr>
            </m:mPr>
        """,
        namespaces={"w": w_ns, "m": m_ns}
    )[0]
    m.append(mPr)

    for row in elements:
        mr = lxml.etree.SubElement(m, f"{{{m_ns}}}mr")
        for element in row:
            me: _Element = lxml.etree.SubElement(mr, f"{{{m_ns}}}e")
            if is_math_element(element):
                children = element.getchildren()
                me.extend(children)
            else:
                raise ValueError("It is not oMath element")
    return oMath


def sympy_matrix_to_omml(matrix: Matrix, brace_type: BraceType = BraceType.PARENTHESES) -> _Element:
    def delete_square_brackets(matrix_latex: str) -> str:
        # Используем регулярное выражение для поиска текста в квадратных скобках
        pattern = r'\\left\[(.*?)\\right\]'
        # Находим все вхождения текста в квадратных скобках
        matches = re.findall(pattern, matrix_latex)

        return matches[0]

    def matrix_latex(_matrix: Matrix):
        matrix_as_list = _matrix.tolist()

        for row in matrix_as_list:
            for i in range(len(row)):
                row[i] = rational_latex(row[i])

        if not matrix_as_list or not isinstance(matrix_as_list[0], list):
            return "Ошибка: Входные данные должны быть вложенным списком."

        rows = len(matrix_as_list)
        cols = len(matrix_as_list[0])

        latex_matrix = "\\begin{matrix}\n"

        for i, row in enumerate(matrix_as_list):
            if len(row) != cols:
                return "Ошибка: Все строки должны иметь одинаковую длину."

            latex_matrix += " & ".join(row)

            if i < rows - 1:
                latex_matrix += " \\\\\n"
            else:
                latex_matrix += "\n"

        latex_matrix += "\\end{matrix}"

        return latex_matrix

    matrix_omml = latex2omml(matrix_latex(matrix))
    return braces(matrix_omml, brace_type=brace_type)


def replace_in_xml(xml: str, key: str, data: str) -> str:
    def replace_func(match):
        content = match.group()
        open_bracket = content.index('>')
        close_bracket = content.rindex('<')
        return content[:open_bracket + 1] + str(data) + content[close_bracket:]

    pattern = f'>[^<>]*{re.escape(key)}[^<>]*</'
    return re.sub(pattern, replace_func, xml)
