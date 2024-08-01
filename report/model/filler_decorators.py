from enum import Enum, auto
from functools import wraps

from docx.document import Document

from report.model.document_template import DocumentTemplate
from report.model.formula import Formula
from report.model.template_filler import TemplateFiller


class InsertType(Enum):
    TEXT = auto()
    FORMULA = auto()
    IMAGE = auto()
    FORMULAS_LIST = auto()
    DOCUMENT = auto()
    DOCUMENTS_LIST = auto()


def _get_key(func):
    name = func.__name__
    fill_str = name[:6]
    if not fill_str == "_fill_":
        raise NameError("Filler function must start with _fill_")
    key = name[6:]
    return key


def _insert(template: DocumentTemplate, key: str, data, insert_type: InsertType):
    match insert_type:
        case InsertType.FORMULA:
            if not isinstance(data, Formula):
                raise ValueError("For InsertType.FORMULA insert util must be Formula type")
            template.insert_formula(key=key, formula=data)
        case InsertType.TEXT:
            if not isinstance(data, str):
                raise ValueError("For InsertType.TEXT insert util must be str type")
            template.insert_text(key=key, text=data)
        case InsertType.IMAGE:
            raise ValueError("TODO: сделай вставку изображения")
        case InsertType.FORMULAS_LIST:
            error = ValueError("For InsertType.FORMULAS_LIST insert util must be list[Formula] type")
            if not isinstance(data, list):
                raise error
            else:
                for elem in data:
                    if not isinstance(elem, Formula):
                        raise error
            template.insert_formulas_list(key=key, formulas_list=data)
        case InsertType.DOCUMENT:
            if not isinstance(data, Document):
                raise ValueError("For InsertType.DOCUMENT insert util must be Document type")
            template.insert_data_from_document(key=key, document=data)
        case InsertType.DOCUMENTS_LIST:
            error = ValueError("For InsertType.DOCUMENT_LIST insert util must be list[Document] type")
            if not isinstance(data, list):
                raise error
            else:
                for elem in data:
                    if not isinstance(elem, Document):
                        raise error
            template.insert_data_from_documents_list(key=key, documents=data)


def filler(func, insert_type: InsertType):
    func._is_filler = True
    key = _get_key(func)

    @wraps(func)
    def wrapper(self):
        data = func(self)
        if not isinstance(self, TemplateFiller):
            raise TypeError(f"Object {self} is not TemplateFiller")
        _insert(template=self.template, key=key, data=data, insert_type=insert_type)
        return data

    return wrapper


def formula(func):
    return filler(func, insert_type=InsertType.FORMULA)


def image(func):
    return filler(func, insert_type=InsertType.IMAGE)


def document(func):
    return filler(func, insert_type=InsertType.DOCUMENT)


def formulas_list(func):
    return filler(func, insert_type=InsertType.FORMULAS_LIST)


def text(func):
    return filler(func, insert_type=InsertType.TEXT)


def documents_list(func):
    return filler(func, insert_type=InsertType.DOCUMENTS_LIST)
