import os
from pathlib import Path
from docx import Document
from docx.document import Document as DocumentType
from docx.text.paragraph import Paragraph
from docx2pdf import convert
from collections.abc import Callable

from lxml.etree import _Element

from report.model.element_creator import copy_paragraph
from report.model.formula import Formula
from report.model.insert_key import InsertKey
from report.model.isolate_key_runs import isolate_key_runs
from report.model.util import short_tag, keys_in_run, can_replace_paragraph


def replace_paragraph_with_elements(paragraph: Paragraph, elements: list[_Element]):
    paragraph_element = paragraph._p
    for elem in reversed(elements):
        paragraph_element.addnext(elem)
    body_element = paragraph_element.getparent()
    body_element.remove(paragraph_element)


def get_document_elements(document: DocumentType):
    ignored_tags = ["sectPr"]
    body_element = document._element.body
    result: list[_Element] = []
    for child in body_element.iterchildren():
        if short_tag(child) in ignored_tags:
            continue
        result.append(child)
    return result


class DocumentTemplate:
    def __init__(self, path: Path):
        self.document: DocumentType = Document(path.as_posix())
        self.name = path.name
        self._insert_keys = None

    def save(self, save_path: Path, document_name: str = "output.docx", add_pdf: bool = True):
        docx_path = save_path.joinpath(document_name)
        self.document.save(docx_path.absolute().as_posix())
        if add_pdf:
            pdf_path = save_path.joinpath(f"{document_name.split('.')[0]}.pdf")
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            convert(docx_path.absolute().as_posix(), pdf_path.absolute().as_posix())

    @property
    def insert_keys(self) -> dict[int, InsertKey]:
        """
            Парсинг ключей делается с предположением, что в ключи находятся в обособленных Run, т.к. были
            выполнены преобразования в init
         """
        if self._insert_keys is not None:
            return self._insert_keys

        isolate_key_runs(self.document)

        result = []
        paragraphs: list[Paragraph] = self.document.paragraphs
        for p in paragraphs:
            for r in p.runs:
                keys = keys_in_run(r)
                if keys:
                    insert_key = InsertKey(
                        paragraph=p,
                        run=r,
                        key=keys[0].strip()
                    )
                    result.append(insert_key)
        dict_result = {}
        for i, key in enumerate(result):
            dict_result[i] = key
        self._insert_keys = dict_result
        return dict_result

    def _find_insert_keys(self, key: str) -> dict[int, InsertKey]:
        result = {}
        for i, ik in self.insert_keys.items():
            if ik.key == key:
                result[i] = ik
        if len(result) == 0:
            print(f"Ключ [{key}] не существует или уже использован")
        return result

    def _insert(self, key: str, insert_func: Callable[[InsertKey], None], report: str):
        insert_keys = self._find_insert_keys(key)
        for i, ik in insert_keys.items():
            insert_func(ik)
            del self.insert_keys[i]
            print(f"{self.name}:[{key}]: {report}")

    def insert_text(self, key: str, text: str):
        def insert_func(ik: InsertKey):
            ik.run.text = text

        self._insert(key=key, insert_func=insert_func, report="TEXT")

    def insert_formula(self, key: str, formula: Formula):
        def insert_func(ik: InsertKey):
            ik.run._r.addnext(formula.oMath)
            para = ik.run._r.getparent()
            para.remove(ik.run._r)

        self._insert(key=key, insert_func=insert_func, report="FORMULA")

    def insert_formulas_list(self, key: str, formulas_list: list[Formula]):

        def insert_func(ik: InsertKey):
            if not can_replace_paragraph(ik.paragraph):
                print(
                    f"Нельзя вставить список формул по ключу [{key}] вместо параграфа [{ik.paragraph.text}],"
                    f"т.к в параграфе есть другой текст помимо ключа")
                return
            formula_paragraph_elements = []
            for formula in formulas_list:
                new_paragraph = copy_paragraph(ik.paragraph)
                new_paragraph_element = new_paragraph._p
                tag_run_element = new_paragraph.runs[0]._r
                tag_run_element.addnext(formula.oMath)
                new_paragraph_element.remove(tag_run_element)
                formula_paragraph_elements.append(new_paragraph_element)

            replace_paragraph_with_elements(ik.paragraph, formula_paragraph_elements)

        self._insert(key=key, insert_func=insert_func, report="FORMULAS LIST")

    def insert_data_from_document(self, key: str, document: DocumentType):
        def insert_func(ik: InsertKey):
            if not can_replace_paragraph(ik.paragraph):
                print(
                    f"Нельзя вставить содержимое другого документа по ключу [{key}] вместо параграфа [{ik.paragraph.text}],"
                    f"т.к в параграфе есть другой текст помимо ключа")
                return
            elements_to_insert = get_document_elements(document)
            replace_paragraph_with_elements(ik.paragraph, elements_to_insert)

        self._insert(key=key, insert_func=insert_func, report="DOCUMENT")

    def insert_data_from_documents_list(self, key: str, documents: list[DocumentType]):

        def insert_func(ik: InsertKey):
            if not can_replace_paragraph(ik.paragraph):
                print(
                    f"Нельзя вставить содержимое списка документов по ключу [{key}] вместо параграфа [{ik.paragraph.text}],"
                    f"т.к в параграфе есть другой текст помимо ключа")
                return

            elements_to_insert = []
            for document in documents:
                elements_to_insert.extend(get_document_elements(document))
            replace_paragraph_with_elements(ik.paragraph, elements_to_insert)

        self._insert(key=key, insert_func=insert_func, report="DOCUMENT LIST")

    def delete_key(self, key: str):
        def insert_func(ik: InsertKey):
            if can_replace_paragraph(ik.paragraph):
                parent = ik.paragraph._p.getparent()
                parent.remove(ik.paragraph._p)
            else:
                parent = ik.paragraph._p
                parent.remove(ik.run._r)
        self._insert(key=key, insert_func=insert_func, report=" -- DELETED -- ")