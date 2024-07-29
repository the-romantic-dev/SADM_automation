from pathlib import Path
# Путь до папки клиента
folder = Path(r"D:\Убежище\Университет\6 семестр\САПР\1\Сиднев\Садовников")

# Путь до изображения графа в папке клиента
graph_img_path = Path(folder, "graph_img.png")

chart_folder = Path(Path.cwd(), "img")

chart_filename = "gantt_chart.png"