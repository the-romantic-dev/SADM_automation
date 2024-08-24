from typing import Callable

height = 30


def generate(fabric: Callable, *args, **kwargs):
    width = kwargs['width'] if 'width' in kwargs else 100
    return fabric(*args, **kwargs, size_hint=(None, None), size=(width, height), pos_hint={'center_y': 0.5})
