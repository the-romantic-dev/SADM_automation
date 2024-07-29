import re

from docx.table import Table, _Cell
from lxml.etree import _Element
from typing import Dict, Any
from report.docx.core import add_text, add_picture, add_document_content, insert_document_content
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.document import Document as DocumentType


def contains_template(string):
    pattern = r'\{\{[^\}]+\}\}'  # Регулярное выражение для поиска шаблона {{...}}
    match = re.search(pattern, string)
    return bool(match)


def extract_name_from_template(string):
    pattern = r'\{\{([^}]+)\}\}'  # Обновленное регулярное выражение с захватывающими скобками
    match = re.search(pattern, string)
    if match:
        return match.group(1)  # Извлекаем значение из захваченной группы
    else:
        return None


def process_run_append(run, data_producer):
    current_data = data_producer()
    if isinstance(current_data, str):
        if current_data.endswith('.png'):
            print(f'Вставлено изображение {run.text}')
            add_picture(picture_path=current_data, run=run)
        else:
            print(f'Вставлен текст {run.text}')
            add_text(text=current_data, run=run)
    elif isinstance(current_data, _Element):
        print(f'Вставлен элемент {run.text}')
        run.element.text = ''
        run.element.append(current_data)
    elif isinstance(current_data, DocumentType):
        paragraph_element = run.element.getparent()
        print(f'Обработана вставка из документа в {paragraph_element.text}')
        # add_document_content(run=run, document=current_data)
        insert_document_content(paragraph_element, document=current_data)
    elif isinstance(current_data, Run):
        print(f'Вставка Run в {run.text}')
        run.element.text = ''
        run._r.append(current_data.element)
    elif isinstance(current_data, Paragraph):
        print(f'Вставка Paragraph в {run.text}')
        run.text = ''
        for r in current_data.runs:
            run._r.append(r.element)
    else:
        print(f'Неподдерживаемый для вставки тип значения {type(current_data)}')


def fill_template(template: DocumentType, data_producers: Dict[str, Any]):
    for i, paragraph in enumerate(template.paragraphs):
        paragraph: Paragraph = paragraph
        if contains_template(paragraph.text):
            fill_paragraph_template(paragraph, data_producers)
    for i, table in enumerate(template.tables):
        table: Table = table
        for row in table.rows:
            for cell in row.cells:
                paragraph: Paragraph = cell.paragraphs[0]
                if contains_template(paragraph.text):
                    fill_paragraph_template(paragraph, data_producers)


def fill_paragraph_template(paragraph: Paragraph, data_producers: Dict[str, Any]):
    pieced_name = ""
    is_piecing_started = False
    for run in paragraph.runs:
        run: Run = run
        name = extract_name_from_template(run.text)
        if name is None:
            if "{{" in run.text:
                is_piecing_started = True
                pieced_name += run.text.split('{{')[1]
                run.text = ''
            elif "}}" in run.text:
                is_piecing_started = False
                pieced_name += run.text.split('}}')[0]
                name = pieced_name
                run.text = "{{" + pieced_name + "}}"
                pieced_name = ''
            else:
                if is_piecing_started:
                    pieced_name += run.text
                    run.text = ''
                if not is_piecing_started:
                    pass
        if name in data_producers.keys():
            current_data = data_producers[name]
            if current_data is None:
                print(f'Удаление тега {run.text}')
                paragraph._element.remove(run._element)
            else:
                process_run_append(run=run, data_producer=current_data)
        elif name is not None:
            print(f'Во входном словаре для заполнения нет ключа [{name}]')
