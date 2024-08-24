import re

from lxml import etree as lxml_etree

from report.docx.docx_namespaces import m as m_ns


def is_math_element(element):
    return element.tag == f"{{{m_ns}}}oMath"


def element_from_xml(xml: str, namespaces: dict[str, str]):
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


def replace_in_xml(xml: str, key: str, data: str) -> str:
    def replace_func(match):
        content = match.group()
        open_bracket = content.index('>')
        close_bracket = content.rindex('<')
        return content[:open_bracket + 1] + str(data) + content[close_bracket:]

    pattern = f'>[^<>]*{re.escape(key)}[^<>]*</'
    return re.sub(pattern, replace_func, xml)
