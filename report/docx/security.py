import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Callable


def change_total_edit_minutes(new_time_minutes: int, docx_path: Path):
    def sub(root: ET.Element):
        # Находим элемент TotalTime и изменяем его значение
        # Если элемента TotalTime нет, его можно добавить
        total_time_element = root.find(
            '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}TotalTime')
        if total_time_element is None:
            total_time_element = ET.SubElement(root,
                                               '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}TotalTime')

        # Устанавливаем новое значение общего времени редактирования (в минутах)
        total_time_element.text = str(new_time_minutes)

    change_app_property(docx_path, new_file_prefix='edited_time', change_root_function=sub)


def change_revision_count(revision: int, docx_path: Path):
    def sub(root: ET.Element):
        revision_element = root.find(
            '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Revision')
        if revision_element is None:
            revision_element = ET.SubElement(root,
                                             '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Revision')

        revision_element.text = str(revision)  # Задаем новый номер редакции

    change_app_property(docx_path, new_file_prefix='edited_revision', change_root_function=sub)


def change_app_property(docx_path: Path, new_file_prefix: str, change_root_function: Callable[[ET.Element], None]):
    with zipfile.ZipFile(docx_path, 'r') as docx:
        # Читаем содержимое файла app.xml
        app_xml = docx.read('docProps/app.xml')

    # Парсим XML
    tree = ET.ElementTree(ET.fromstring(app_xml))
    root = tree.getroot()

    change_root_function(root)

    # Сохраняем изменения обратно в app.xml
    new_app_xml = ET.tostring(root, encoding='utf-8', xml_declaration=True)

    new_docx_path = Path(docx_path.parent, f'{new_file_prefix}_{docx_path.name}')

    # Копируем содержимое старого docx в новый, заменяя файл app.xml
    with zipfile.ZipFile(docx_path, 'r') as original_zip:
        with zipfile.ZipFile(new_docx_path, 'w') as new_zip:
            # Проходимся по всем файлам в оригинальном архиве
            for item in original_zip.infolist():
                if item.filename != 'docProps/app.xml':
                    # Копируем остальные файлы без изменений
                    new_zip.writestr(item, original_zip.read(item.filename))

            # Заменяем файл app.xml на новый
            new_zip.writestr('docProps/app.xml', new_app_xml)
    return new_docx_path

# def change_total_editing_time(docx_path: Path, new_time_minutes: int, new_file_prefix: str = 'edited_time'):
#     with zipfile.ZipFile(docx_path, 'r') as docx:
#         # Читаем содержимое файла app.xml
#         app_xml = docx.read('docProps/app.xml')
#
#     # Парсим XML
#     tree = ET.ElementTree(ET.fromstring(app_xml))
#     root = tree.getroot()
#
#     # Находим элемент TotalTime и изменяем его значение
#     # Если элемента TotalTime нет, его можно добавить
#     total_time_element = root.find(
#         '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}TotalTime')
#     if total_time_element is None:
#         total_time_element = ET.SubElement(root,
#                                            '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}TotalTime')
#
#     # Устанавливаем новое значение общего времени редактирования (в минутах)
#     total_time_element.text = str(new_time_minutes)  # Задаем 120 минут, например
#
#     # Сохраняем изменения обратно в app.xml
#     new_app_xml = ET.tostring(root, encoding='utf-8', xml_declaration=True)
#
#     new_docx_path = Path(docx_path.parent, f'{new_file_prefix}_{docx_path.name}')
#
#     # Копируем содержимое старого docx в новый, заменяя файл app.xml
#     with zipfile.ZipFile(docx_path, 'r') as original_zip:
#         with zipfile.ZipFile(new_docx_path, 'w') as new_zip:
#             # Проходимся по всем файлам в оригинальном архиве
#             for item in original_zip.infolist():
#                 if item.filename != 'docProps/app.xml':
#                     # Копируем остальные файлы без изменений
#                     new_zip.writestr(item, original_zip.read(item.filename))
#
#             # Заменяем файл app.xml на новый
#             new_zip.writestr('docProps/app.xml', new_app_xml)
