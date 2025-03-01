from typing import Callable

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from ui.lpp.util import generate, height


def constraint_layout(x1:str= None, x2:str=None, const:str=None) -> tuple[BoxLayout, list[Callable]]:
    box = BoxLayout(
        orientation="horizontal",
        spacing=2,
        size_hint_y=None,  # Убираем растягивание по вертикали
        height=height,  # Фиксированная высота,
        pos_hint={'center_y': 0.5}
    )
    input_width = 40
    x1_text_input: TextInput = generate(TextInput, hint_text="", multiline=False, width=input_width)
    if x1 is not None:
        x1_text_input.text = x1
    x2_text_input: TextInput = generate(TextInput, hint_text="", multiline=False, width=input_width)
    if x2 is not None:
        x2_text_input.text = x2
    const_text_input: TextInput = generate(TextInput, hint_text="", multiline=False, width=input_width)
    if const is not None:
        const_text_input.text = const
    data_sources = [
        lambda: x1_text_input.text,
        lambda: x2_text_input.text,
        lambda: const_text_input.text
    ]

    elements = [
        generate(Widget, size_hint_x=None, width=20),
        x1_text_input,
        generate(Label, text="* x1 +", width=40),
        x2_text_input,
        generate(Label, text="* x2", width=40),
        generate(Label, text="<=", width=10),
        generate(Widget, size_hint_x=None, width=5),
        const_text_input
    ]

    for e in elements:
        box.add_widget(e)
    return box, data_sources
