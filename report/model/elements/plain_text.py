from dataclasses import dataclass
from enum import Enum, auto


# class TextStyle(Enum):
#     DEFAULT = auto()
#     BOLD = auto()
#     ITALIC = auto()


@dataclass
class PlainText:
    text: str
    bold: bool
    italic: bool
    size: int = 24
    font: str = "Times New Roman"
