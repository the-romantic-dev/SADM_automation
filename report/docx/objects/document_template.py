import os
from copy import deepcopy

from docx.document import Document as DocumentType
from docx import Document
from docx2pdf import convert

from report.docx.core import add_document_content_in_end
from report.docx.omml import latex2omml
from report.docx.tables import create_table_filled
from report.docx.templates import fill_template

from pathlib import Path


class DocumentTemplate:
    def __init__(self, template_path: Path):
        self.template: DocumentType = Document(template_path.absolute().as_posix())
        self.data_producers = {}

    def fill(self):
        methods = [getattr(self, method_name) for method_name in dir(self)
                   if callable(getattr(self, method_name))]
        for method in methods:
            if hasattr(method, '_is_filler') and method._is_filler:
                method()
        fill_template(template=self.template, data_producers=self.data_producers)

    @classmethod
    def filler(cls, func):
        func._is_filler = True

        return func

    def _fill_table(self, key: str, table_data: list[list]):
        table = Table(table_data)
        self.data_producers[key] = table.produce_data

    def _fill_formulas_list(self, key: str, latex_formulas_list: list[str]):
        self.data_producers[key] = FormulasList(latex_formulas_list).produce_data

    def _fill_formula(self, key: str, formula_latex: str):
        self.data_producers[key] = Formula(formula_latex).produce_data


    def _fill_text(self, key: str, text: str):
        self.data_producers[key] = lambda: text

    def _delete_key(self, key: str):
        self.data_producers[key] = None

    def _fill_picture(self, key: str, picture_path: Path):
        self.data_producers[key] = lambda: picture_path.absolute().as_posix()

    def _fill_document_content(self, key, document: DocumentType):
        self.data_producers[key] = lambda: document

    def _fill_document_content_list(self, key: str, data: list[DocumentType]):
        self.data_producers[key] = TemplatesList(data).produce_data

    def save(self, save_path: Path, document_name: str = "output.docx", add_pdf: bool = True):
        # fill_template(template=self.template, data_producers=self.data_producers)
        docx_path = save_path.joinpath(document_name)
        self.template.save(docx_path.absolute().as_posix())
        if add_pdf:
            pdf_path = save_path.joinpath("output.pdf")
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            convert(docx_path.absolute().as_posix(), pdf_path.absolute().as_posix())


class DataProducer:
    def __init__(self, data):
        self.data = data

    def produce_data(self):
        return deepcopy(self.data)


class Formula(DataProducer):
    def __init__(self, latex: str):
        self._latex = latex
        self._omml = latex2omml(latex)
        super().__init__(data=self._omml)


class FormulasList(DataProducer):

    def __init__(self, latex_formulas_list: list[str]):
        self._formulas_list = [Formula(latex) for latex in latex_formulas_list]
        self._temp_document: DocumentType = Document()
        for formula in self._formulas_list:
            omml = formula.produce_data()
            p = self._temp_document.add_paragraph()
            p._element.append(omml)
        super().__init__(data=self._temp_document)


class Table(DataProducer):
    def __init__(self, table_data: list[list]):
        self._data = table_data
        self._temp_document: DocumentType = Document()
        self.docx_table = create_table_filled(document=self._temp_document, data=table_data)
        super().__init__(data=self._temp_document)


class TemplatesList(DataProducer):
    def __init__(self, data: list[DocumentType]):
        self.paragraphs = []
        temp_document: DocumentType = Document()
        for template in data:
            add_document_content_in_end(main_document=temp_document, data_document=template)
        temp_document.save(r"/tasks/task1_2_lp/_templates\sabonis\bruteforce\temp.docx")
        super().__init__(data=temp_document)
