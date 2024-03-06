import matplotlib.pyplot as plt

def create_gantt_chart(tasks):
    fig, ax = plt.subplots(figsize=(10, 5))

    for y, (task_name, start, end) in enumerate(tasks):
        ax.barh(y, end - start, left=start, height=1, align='center', label=task_name)
        ax.text((start + end) / 2, y, task_name, ha='center', va='center', color='white', fontsize=8)

    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([task[0] for task in tasks])
    ax.set_xlabel('Time')
    ax.set_ylabel('Task Executor')
    ax.set_title('Gantt Chart')

    plt.show()

# Пример данных для задач
tasks_data = [
    ('Task 1', 0, 5),
    ('Task 2', 0, 7),
    ('Task 3', 4, 9),
    ('Task 4', 8, 12),
]

# Создание диаграммы Гантта
create_gantt_chart(list(reversed(tasks_data)))