from pathlib import Path

from docx import Document

from report.model.template.document_template import DocumentTemplate
from report.model.elements.formula import Formula
if __name__ == '__main__':

    folder_path = Path(r"D:\Desktop\test")
    document_path = Path(folder_path, "tags.docx")
    insert_document_1 = Document(Path(folder_path, "tags_2.docx").as_posix())
    insert_document_2 = Document(Path(folder_path, "tags_2.docx").as_posix())
    template = DocumentTemplate(document_path)
    insert_keys = template.insert_keys
    template.insert_text("tag4", "хуй")
    formulas_list = [
        Formula(["x^2"]),
        Formula(["x_3"]),
        Formula(["\\alpha^7"]),
    ]
    # template.insert_formulas_list("tag3", formulas_list)
    template.insert_data_from_documents_list("tag8", [insert_document_1, insert_document_2])
    template.delete_key("tag3")
    template.save(folder_path, "tags_proc.docx", add_pdf=False)