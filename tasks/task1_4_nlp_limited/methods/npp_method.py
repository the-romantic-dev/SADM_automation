import plotter

class NPPMethod:
    def __init__(self):
        self.f = None
        self.limits = None
        self.solution = {}
        self.track = []
        self.values_track = []

    def prepare_plot(self):
        plotter.plt.figure(figsize=(15, 9))
        plotter.clear()
        limits_intersects = plotter.get_limits_points(self.limits)
        bounds = plotter.calculate_max_min_dots(self.track + limits_intersects)
        plotter.add_level_lines(self.f, bounds)
        plotter.add_limits(self.limits, bounds)
        plotter.add_solution_track(self.track)

    def show_plot(self):
        self.prepare_plot()
        plotter.show()

    def save_plot(self, path: str):
        self.prepare_plot()
        plotter.save(path)