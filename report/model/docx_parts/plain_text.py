from dataclasses import dataclass


@dataclass
class PlainText:
    text: str
    bold: bool
    italic: bool
    size: int = 24
    font: str = "Times New Roman"
