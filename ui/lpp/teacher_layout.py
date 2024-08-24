from typing import Callable

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from ui.lpp.util import generate, height


def teacher_layout() -> tuple[BoxLayout, list[Callable]]:
    box = BoxLayout(
        orientation="horizontal",
        spacing=2,
        size_hint_y=None,  # Убираем растягивание по вертикали
        height=height,  # Фиксированная высота,
        pos_hint={'center_y': 0.5}
    )
    input_width = 100
    spinner: Spinner = generate(Spinner, text="Сабонис", values=("Сабонис", "Сиднев"), width=input_width)
    data_sources = [
        lambda: spinner.text
    ]
    elements = [
        generate(Widget, size_hint_x=None, width=20),
        generate(Label, text="Преподаватель: ", width=100),
        generate(Widget, size_hint_x=None, width=5),
        spinner
    ]

    for e in elements:
        box.add_widget(e)
    return box, data_sources
