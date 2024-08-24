from enum import Enum

from lxml import etree as lxml_etree
from lxml.etree import _Element

from report.docx.docx_namespaces import m as m_ns, w as w_ns
from report.model.elements.util import is_math_element, element_from_xml


class BraceType(Enum):
    PARENTHESES = 0
    BRACKETS = 1
    STRAIGHT = 2
    CURLY = 3
    LEFT_CURLY = 4


def braces(math_element: _Element, brace_type: BraceType = BraceType.PARENTHESES) -> _Element:
    if not is_math_element(math_element):
        raise ValueError("Элемент не является частью уравнения Word")

    brace_elements = element_from_xml(
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
    dPr = element_from_xml(
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
