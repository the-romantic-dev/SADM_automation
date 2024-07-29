from sympy import simplify, Eq, latex, symbols, Matrix
from sympy.parsing.latex import parse_latex
from sympy.simplify.fu import TR22
import latex2mathml.converter
from lxml import etree
from docx import Document
from docx.document import Document as DocumentType

from methods.frank_wolfe.frank_wolfe import FrankWolfe
from task import Task

if __name__ == "__main__":
    frank_wolfe = FrankWolfe()
    frank_wolfe.solve(f=Task.f, limitations=Task.lim1234)
    print(frank_wolfe.get_report())