import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from typing import Callable

from sympy import Rational

from tasks.task1_3_nlp_unlimited.main import nlp_unlimited_main
from tasks.task1_3_nlp_unlimited.model import NLPObjective
from tasks.task1_3_nlp_unlimited.model.util import UnivariateMethod
from tasks.teacher import Teacher

icon_path = Path(Path(__file__).parent, 'icon.png')

tasks_names = [
    'Линейное программирование',
    'Нелинейное программирование (без ограничений)'
]
teachers = ['Сиднев', 'Сабонис']
methods = ['Наиск. подъема', 'Ньютона', 'Сопр. градиентов', 'Релакс.', 'Бройдена']
names_to_um = {
    methods[0]: UnivariateMethod.RapidAscent,
    methods[1]: None,
    methods[2]: UnivariateMethod.ConjugateGradient,
    methods[3]: UnivariateMethod.Relaxation,
    methods[4]: UnivariateMethod.Broyden,
}
data_sources = dict()


def build_root() -> tk.Tk:
    root = tk.Tk()
    root['bg'] = '#F4F2F5'
    root.title("Решатель для САПР")
    root.geometry("600x450")
    root.resizable(width=False, height=False)
    icon = tk.PhotoImage(file=icon_path)
    root.iconphoto(True, icon)
    return root


def build_task_menu(root: tk.Tk, callback: Callable[[str], None]):
    selected_value = tk.StringVar()
    selected_value.set(tasks_names[0])

    dropdown = tk.OptionMenu(root, selected_value, *tasks_names, command=callback)
    dropdown.place(relx=0.05)
    return dropdown


def build_task_frame(root: tk.Tk):
    frame = tk.Frame(root, bg='#D4BEE4')
    frame.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.7)
    return frame


def build_solve_button(root, callback: Callable[[], None]):
    button = tk.Button(root, text="Решить", font=('Roboto', 18), bg='#3B1E54', fg='white', command=callback)
    button.place(rely=0.88, relx=0.28, relwidth=0.5)
    return button


def nlp_parse_and_run(frame: tk.Frame):
    objective = NLPObjective([
        Rational(data_sources['C11'].get()),
        Rational(data_sources['C22'].get()),
        Rational(data_sources['C12'].get()),
        Rational(data_sources['C1'].get()),
        Rational(data_sources['C2'].get())
    ])
    teacher = Teacher.SIDNEV if data_sources['teacher'].get() == 'Сиднев' else Teacher.SABONIS
    variant = int(data_sources['variant'].get())
    start_X = (
        Rational(data_sources['x1'].get()),
        Rational(data_sources['x2'].get())
    )
    method = names_to_um[data_sources['univariate_method'].get()]
    for i in data_sources:
        print(f'{i} = {data_sources[i].get()}')
    nlp_unlimited_main(teacher, objective, variant, start_X, method)


def build_savepath(root):
    label = tk.Label(root, text='Путь сохранения отчета')
    label.place(relx=0.05, rely=0.09)

    entry = tk.Entry(root, width=50)
    entry.place(relx=0.3, relwidth=0.5, rely=0.09)

    def browse_file():
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.docx"),
                                                           ("All files", "*.*")])
        if filename:  # Проверяем, что пользователь выбрал файл
            entry.delete(0, tk.END)  # Очищаем текущее значение
            entry.insert(0, filename)  # Вставляем выбранный путь в Entry

    browse_button = tk.Button(root, text="Выбрать путь", command=browse_file)
    browse_button.place(relx=0.82, rely=0.08)
    return entry


def rebuild_frame(curr_task: str):
    print(curr_task)


def build_nlp_unlimited_frame(frame: tk.Frame):
    labels_text = ['C11', 'C22', 'C12', 'C1', 'C2']
    total = len(labels_text)
    labels = [tk.Label(frame, text=labels_text[i]) for i in range(total)]
    entries = [tk.Entry(frame, width=10) for _ in range(total)]
    for i in range(total):
        labels[i].grid(row=i, column=0, padx=10, sticky='ew')
        entries[i].grid(row=i, column=1, pady=5)
        data_sources[labels_text[i]] = entries[i]
    teacher_menu, teacher_var = create_teacher_menu(frame)
    data_sources['teacher'] = teacher_var

    teacher_label = tk.Label(frame, text='Препод:')
    teacher_label.grid(row=0, column=2, padx=10, sticky='e')
    teacher_menu.grid(row=0, pady=5, column=3)

    start_point_label = tk.Label(frame, text='Начальная точка')
    start_point_label.grid(row=2, column=2, padx=5, sticky='e')

    tk.Label(frame, text='x1').grid(row=1, column=3)
    tk.Label(frame, text='x2').grid(row=1, column=4)

    x1 = tk.Entry(frame, width=10)
    x1.grid(row=2, column=3)
    data_sources['x1'] = x1

    x2 = tk.Entry(frame, width=10)
    x2.grid(row=2, column=4)
    data_sources['x2'] = x2

    tk.Label(frame, text='Вариант:').grid(row=0, column=5, sticky='e')
    variant = tk.Entry(frame, width=10)
    variant.grid(row=0, column=6, padx=5)
    data_sources['variant'] = variant

    tk.Label(frame, text='Метод с одномерным\nпоиском первого шага').grid(row=5, column=2)

    um_menu, um_var = create_univariate_method_menu(frame)
    um_menu.grid(row=6, column=2)
    data_sources['univariate_method'] = um_var


def create_teacher_menu(frame: tk.Frame):
    selected_value = tk.StringVar()
    selected_value.set(teachers[0])

    dropdown = tk.OptionMenu(frame, selected_value, *teachers)
    dropdown.place(relx=0.05)
    return dropdown, selected_value


def create_univariate_method_menu(frame: tk.Frame):
    selected_value = tk.StringVar()
    selected_value.set(methods[0])

    dropdown = tk.OptionMenu(frame, selected_value, *methods)
    dropdown.place(relx=0.05)
    return dropdown, selected_value


def build():
    root = build_root()
    task_menu = build_task_menu(root, rebuild_frame)
    frame = build_task_frame(root)
    save_path = build_savepath(root)
    solve_button = build_solve_button(root, lambda: nlp_parse_and_run(frame))
    build_nlp_unlimited_frame(frame)
    root.mainloop()


if __name__ == '__main__':
    build()
