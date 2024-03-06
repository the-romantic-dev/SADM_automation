from docx.shared import Pt
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.document import Document as DocumentType
from docx.oxml import OxmlElement
from report.docx.tables import _make_table_from_child_document

# document_name = 'output.docx'

# def input_rational_for_docx(run, p, q):
#     oMath = OxmlElement('m:oMath')
#     frac = OxmlElement('m:f')
#     num = OxmlElement('m:num')
#     den = OxmlElement('m:den')
#
#     num.append(OxmlElement('m:r'))
#     num[0].append(OxmlElement('m:t'))
#     num[0][0].text = f'{p}'
#
#     den.append(OxmlElement('m:r'))
#     den[0].append(OxmlElement('m:t'))
#     den[0][0].text = f'{q}'
#
#     frac.append(num)
#     frac.append(den)
#
#     mr = OxmlElement('m:r')
#     mr.append(frac)
#     oMath.append(mr)
#
#     run._element.clear_content()
#     # Set the font size for the equation
#
#     # Add the math element to the run
#     run._element.append(oMath)
def get_image_dimensions(image_path):
    from PIL import Image
    # Используем библиотеку PIL для получения размеров изображения
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height
def add_picture(picture_path: str, run: Run):
    run.element.text = ''
    pic = run.add_picture(picture_path)
    original_width, original_height = get_image_dimensions(picture_path)
    pic.width = Pt(612)
    pic.height = Pt(int((612 / original_width) * original_height))

def add_text(text: str, run: Run):
    run.element.text = ''
    run.element.text = text

def add_document_content(run: Run, document: DocumentType):
    from docx.oxml import CT_P
    from docx.oxml import CT_Tbl

    run.element.text = ''
    parent_elm = document.element.body
    paste_elements = []
    for child in parent_elm.iterchildren():
        result = None
        if isinstance(child, CT_P):
            result = Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            result = _make_table_from_child_document(child, document)
        else:
            continue
        paste_elements.append(result._element)
    for elem in reversed(paste_elements):
        run._r.addnext(elem)






