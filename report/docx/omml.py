from pathlib import Path

import latex2mathml.converter
from lxml import etree
from sympy import latex


def latex2omml(latex_expr):
    mathml_output = latex2mathml.converter.convert(latex=latex_expr)
    root_name = "SADM_automation"
    root_path = Path.cwd()
    while root_path.name != root_name:
        root_path = root_path.parent
    mml2omml_path = Path(root_path, "report", "docx", "MML2OMML.XSL")
    tree = etree.fromstring(mathml_output)
    xslt = etree.parse(mml2omml_path.as_posix())
    transform = etree.XSLT(xslt)
    new_dom = transform(tree)
    return new_dom.getroot()


def sympy2omml(sympy_expr):
    latex_output = latex(sympy_expr)
    return latex2omml(latex_output)
