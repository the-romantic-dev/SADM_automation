import logging
import traceback
from pathlib import Path
from threading import Thread
from typing import Callable

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from sympy import Rational

from definitions import ROOT_DIR
from tasks.task1_2_lp.model import Objective, ObjectiveType, Constraint, LPProblem
from tasks.teacher import Teacher
from ui.lpp.constraint_layout import constraint_layout
from ui.lpp.objective_layout import objective_layout
from ui.lpp.teacher_layout import teacher_layout
from ui.lpp.variant_layout import variant_layout


class LPPApp(App):
    def __init__(self, script_callback: Callable[[Teacher, LPProblem, int, Callable], None], **kwargs):
        self.script_callback = script_callback
        super().__init__(**kwargs)

    def build(self):
        # Основной контейнер
        main_layout = AnchorLayout()
        lpp_box = BoxLayout(orientation="vertical", size_hint_y=None, padding=10, spacing=10)

        start_button = Button(text='Start script', size_hint=(None, None), size=(100, 30),
                              background_color=(248 / 255, 200 / 255, 101 / 255, 1))
        with open(Path(ROOT_DIR, 'ui/lpp/config.txt'), 'r') as config:
            elements = config.readline().split(' ')

        obj, obj_ds = objective_layout(obj_type_txt=elements[1], obj_x1=elements[2], obj_x2=elements[3])
        constr1, constr1_ds = constraint_layout(elements[4], elements[5], elements[6])
        constr2, constr2_ds = constraint_layout(elements[7], elements[8], elements[9])
        teacher, teacher_ds = teacher_layout(elements[10])
        variant, variant_ds = variant_layout(elements[0])

        def on_press(instance):
            instance.disabled = True
            obj_type_txt, obj_x1, obj_x2 = obj_ds[0](), obj_ds[1](), obj_ds[2]()

            c1_x1, c1_x2, c1_const = constr1_ds[0](), constr1_ds[1](), constr1_ds[2]()
            c2_x1, c2_x2, c2_const = constr2_ds[0](), constr2_ds[1](), constr2_ds[2]()

            variant_num = int(variant_ds[0]())
            teacher_name = teacher_ds[0]()

            with open(Path(ROOT_DIR, 'ui/lpp/config.txt'), 'w') as config:
                config.write(' '.join([
                    str(variant_num),
                    obj_type_txt, obj_x1, obj_x2,
                    c1_x1, c1_x2, c1_const,
                    c2_x1, c2_x2, c2_const,
                    teacher_name
                ]))


            _teacher = Teacher.SABONIS if teacher_name == 'Сабонис' else Teacher.SIDNEV
            obj_type = ObjectiveType.MAX if obj_type_txt == 'max' else ObjectiveType.MIN
            objective = Objective(obj_type=obj_type, coeffs=[Rational(obj_x1), Rational(obj_x2)])
            constraints = [
                Constraint(coeffs=[Rational(c1_x1), Rational(c1_x2)], const=Rational(c1_const)),
                Constraint(coeffs=[Rational(c2_x1), Rational(c2_x2)], const=Rational(c2_const))
            ]

            problem = LPProblem(constraints, objective)

            def callback():
                instance.disabled = False

            def long_task():
                self.script_callback(_teacher, problem, variant_num, callback)

            thread = Thread(target=long_task)
            try:
                thread.start()
            except Exception as e:
                import logging
                logger = logging.getLogger('ftpuploader')
                callback()
                logger.error('Exception: %s', repr(e))

        start_button.bind(on_press=on_press)

        lpp_box.add_widget(variant)
        lpp_box.add_widget(obj)
        lpp_box.add_widget(constr1)
        lpp_box.add_widget(constr2)
        lpp_box.add_widget(teacher)

        lpp_box.add_widget(start_button)
        main_layout.add_widget(lpp_box)
        main_layout.anchor_x = 'center'
        main_layout.anchor_y = 'center'

        return main_layout
