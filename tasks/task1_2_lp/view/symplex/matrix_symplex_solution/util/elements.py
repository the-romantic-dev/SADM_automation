from pathlib import Path

from report.docx.docx_namespaces import m, w
from report.model.elements.util import elements_from_xml, replace_in_xml
from tasks.task1_2_lp.local_definitions import TASK_DIR

ELEMENTS_XML_DIR = Path(TASK_DIR, "view/symplex/matrix_symplex_solution/elements_xml")


def _get_xml_from_file(filename: str):
    txt_path = Path(ELEMENTS_XML_DIR, filename)
    with open(txt_path.as_posix(), 'r', encoding='utf-8') as file:
        formula_xml = file.read()
    return formula_xml


def _get_element_from_xml_template(filename: str, keys: str | list[str], replacements: str | list[str]):
    xml = _get_xml_from_file(filename)
    if not isinstance(keys, list):
        keys = [keys]
    if not isinstance(replacements, list):
        replacements = [replacements]
    if len(keys) != len(replacements):
        raise ValueError("Число ключей не совпадает с числом вставок")
    for i in range(len(keys)):
        xml = replace_in_xml(xml, key=keys[i], data=replacements[i])
    element = elements_from_xml(xml, {"m": m, "w": w})[0]
    return element


def basis_value(basis_index: int):
    return _get_element_from_xml_template(filename="basis_value.txt", keys="basis_index", replacements=str(basis_index))


def basis_exclude_criteria(basis_index: int):
    return _get_element_from_xml_template(
        filename="basis_exclude_criteria_common_expression.txt",
        keys="basis_index", replacements=str(basis_index)
    )


def basis_exclude_criteria_frac(basis_index: int, element_index: int, z_index: str):
    return _get_element_from_xml_template(
        filename="basis_exclude_criteria_frac.txt",
        keys=["basis_index", "element_index", "z_index"], replacements=[str(basis_index), str(element_index), z_index]
    )
