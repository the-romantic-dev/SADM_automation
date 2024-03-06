from docx.document import Document as DocumentType
from docx import Document

from report.docx.omml import latex2omml
from report.docx.tables import create_table_filled
from report.docx.templates import fill_template

from pathlib import Path


class DocumentTemplate:
    def __init__(self, template_path: Path):
        self.template: DocumentType = Document(template_path.absolute().as_posix())
        self.data_producers = {}

    def _fill_table(self, key: str, table_data: list[list]):
        table = Table(table_data)
        self.data_producers[key] = table.produce_data

    def _fill_formulas_list(self, key: str, latex_formulas_list: list[str]):
        self.data_producers[key] = FormulasList(latex_formulas_list).produce_data

    def _fill_formula(self, key: str, formula_latex: str):
        self.data_producers[key] = Formula(formula_latex).produce_data

    def _fill_text(self, key: str, text: str):
        self.data_producers[key] = lambda: text

    def _fill_picture(self, key: str, picture_path: Path):
        self.data_producers[key] = lambda: picture_path.absolute().as_posix()

    def save(self, save_path: Path, document_name: str = "output.docx"):
        fill_template(template=self.template, data_producers=self.data_producers)
        file_path = save_path.joinpath(document_name)
        self.template.save(file_path.absolute().as_posix())


class DataProducer:
    def __init__(self, data):
        self.data = data

    def produce_data(self):
        return self.data


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
            p = self._temp_document.add_paragraph()
            r = p.add_run()
            omml = formula.produce_data()
            r.element.append(omml)
        super().__init__(data=self._temp_document)


class Table(DataProducer):
    def __init__(self, table_data: list[list]):
        self._data = table_data
        self._temp_document: DocumentType = Document()
        self.docx_table = create_table_filled(document=self._temp_document, data=table_data)
        super().__init__(data=self._temp_document)
