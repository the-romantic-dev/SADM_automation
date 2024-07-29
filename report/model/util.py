import re

from docx.text.paragraph import Paragraph
from docx.text.run import Run
from lxml.etree import _Element

KEY_PATTERN = r'\{\{(.+?)\}\}'


def can_replace_paragraph(paragraph: Paragraph):
    ignorable_tags = ["proofErr", "pPr"]
    tags = []
    for child in paragraph._p.iterchildren():
        tag = short_tag(child)
        tags.append(tag)
    count = 0
    for tag in tags:
        if tag not in ignorable_tags:
            count += 1
    return count <= 1


def short_tag(element: _Element):
    return element.tag.split("}")[-1]


def keys_in_run(run: Run):
    """ Возвращает все ключи, находящиеся в тексте Run """
    text = run.text
    matches = re.findall(KEY_PATTERN, text)
    return matches
