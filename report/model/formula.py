import lxml.etree
from lxml.etree import _Element
from report.docx.docx_namespaces import m

from report.docx.omml import latex2omml


class Formula:
    def __init__(self, formula_parts: list[str | _Element] | str | _Element):
        if isinstance(formula_parts, list):
            self._formula_parts = formula_parts
        else:
            self._formula_parts = [formula_parts]
        self._omml = None

    @property
    def oMath(self) -> _Element:
        if self._omml is not None:
            return self._omml
        omml_parts: list[_Element] = []
        for part in self._formula_parts:
            if isinstance(part, str):
                omml_parts.append(latex2omml(part))
            elif isinstance(part, _Element):
                omml_parts.append(part)
        parent_math_element: _Element = lxml.etree.Element(f"{{{m}}}oMath")
        for op in omml_parts:
            children = op.getchildren()
            for child in children:
                parent_math_element.append(child)
        return parent_math_element
