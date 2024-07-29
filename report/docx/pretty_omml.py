import re
from enum import Enum
from lxml import etree as lxml_etree
from lxml.etree import _Element
from sympy import Matrix, latex, Expr, Number, Rational, Integer, Float, primefactors, MutableDenseMatrix

from report.docx.docx_namespaces import m as m_ns
from report.docx.docx_namespaces import w as w_ns
from report.docx.omml import latex2omml


class BraceType(Enum):
    PARENTHESES = 0
    BRACKETS = 1
    STRAIGHT = 2
    CURLY = 3


def braces(math_element: _Element, brace_type: BraceType = BraceType.PARENTHESES) -> _Element:
    if math_element.tag != f"{{{m_ns}}}oMath":
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


def sympy_matrix_to_omml(matrix: Matrix, brace_type: BraceType = BraceType.PARENTHESES) -> _Element:
    def delete_square_brackets(matrix_latex: str) -> str:
        # Используем регулярное выражение для поиска текста в квадратных скобках
        pattern = r'\\left\[(.*?)\\right\]'
        # Находим все вхождения текста в квадратных скобках
        matches = re.findall(pattern, matrix_latex)

        return matches[0]

    matrix = replace_rationals_matrix(matrix)
    bare_matrix_latex = delete_square_brackets(latex(matrix))
    matrix_omml = latex2omml(bare_matrix_latex)
    return braces(matrix_omml, brace_type=brace_type)


def replace_in_xml(xml: str, key: str, data: str) -> str:
    def replace_func(match):
        content = match.group()
        open_bracket = content.index('>')
        close_bracket = content.rindex('<')
        return content[:open_bracket + 1] + str(data) + content[close_bracket:]

    pattern = f'>[^<>]*{re.escape(key)}[^<>]*</'
    return re.sub(pattern, replace_func, xml)


def is_rational_finite_float(num: Rational):
    q_prime_factors = set(primefactors(num.q))
    for factor in q_prime_factors:
        if factor != 2 and factor != 5:
            return False
    return True


def replace_rationals_matrix(matrix: MutableDenseMatrix):
    return matrix.applyfunc(lambda x: get_replacement(x))


def get_replacement(_num: Number):
    result = _num
    if isinstance(_num, Rational):
        if _num.q == 1:  # если знаменатель равен 1, это целое число
            result = Integer(_num)
        else:
            if is_rational_finite_float(_num):
                result = Float(_num)
            else:
                result = _num
    return result


def replace_rationals_expr(expr: Expr):
    replacements = {}

    for num in expr.atoms(Number):
        replacements[num] = get_replacement(num)
    return expr.xreplace(replacements)
