from typing import Callable

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

height = 30


def generate(fabric: Callable, *args, **kwargs):
    width = kwargs['width'] if 'width' in kwargs else 100
    return fabric(*args, **kwargs, size_hint=(None, None), size=(width, height), pos_hint={'center_y': 0.5})


def objective_layout(
        obj_type_txt: str = None,
        obj_x1: str = None,
        obj_x2: str = None) -> tuple[BoxLayout, list[Callable]]:
    box = BoxLayout(
        orientation="horizontal",
        spacing=2,
        size_hint_y=None,  # Убираем растягивание по вертикали
        height=height,  # Фиксированная высота,
        pos_hint={'center_y': 0.5}
    )
    input_width = 40
    spinner: Spinner = generate(Spinner, text="max", values=("min", "max"), width=50)
    if obj_type_txt is not None:
        spinner.text = obj_type_txt
    x1_text_input: TextInput = generate(TextInput, hint_text="", multiline=False, width=input_width)
    if obj_x1 is not None:
        x1_text_input.text = obj_x1
    x2_text_input: TextInput = generate(TextInput, hint_text="", multiline=False, width=input_width)
    if obj_x2 is not None:
        x2_text_input.text = obj_x2
    data_sources = [
        lambda: spinner.text,
        lambda: x1_text_input.text,
        lambda: x2_text_input.text
    ]
    elements = [
        generate(Widget, size_hint_x=None, width=10),
        spinner,
        generate(Label, text="(", width=10, font_size=25),
        x1_text_input,
        generate(Label, text="* x1 +", width=40),
        x2_text_input,
        generate(Label, text="* x2", width=40),
        generate(Label, text=")", width=10, font_size=25)
    ]

    for e in elements:
        box.add_widget(e)
    return box, data_sources
