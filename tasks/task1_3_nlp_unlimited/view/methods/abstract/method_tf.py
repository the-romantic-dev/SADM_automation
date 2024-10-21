from pathlib import Path

from docx import Document
from sympy import Matrix

from report.model.docx_parts.formula import Formula
from report.model.docx_parts.table import Table
from report.model.elements.math.braces import braces
from report.model.template.document_template import DocumentTemplate
from report.model.template.filler_decorators import template_filler, document, table, image
from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf
from tasks.task1_3_nlp_unlimited.model.methods import IterativeMethod
from tasks.task1_3_nlp_unlimited.view.methods.univariate_first_step_size.univariate_first_step_size_tf import \
    UnivariateFirstStepSizeTF
from tasks.task1_3_nlp_unlimited.view.plot.plotter import NLPMethodPlotter

template_path = Path(Path(__file__).parent, "method.docx")

pic_path = Path(Path(__file__).parent.parent.parent, "plot/pic.png")


@sub_tf
class MethodTF(TemplateFiller):
    def __init__(self, method: IterativeMethod, start_point: Matrix, description_document_path: Path,
                 is_step_univariate: bool

                 ):
        self.description_document_path = description_document_path
        self.is_step_univariate = is_step_univariate
        template = DocumentTemplate(template_path)
        super().__init__(template)
        self.method = method
        self.start_point = start_point
        self.solution = method.solve(start_point)

    @document
    def _fill_method_steps_description(self):
        return Document(self.description_document_path.as_posix())

    @template_filler
    def _fill_univariate_first_step_size(self):
        if not self.is_step_univariate:
            return None
        return UnivariateFirstStepSizeTF(self.method, self.start_point)

    @table
    def _fill_steps_table(self):
        header = [Formula('i'), Formula('x_1'), Formula('x_2'), Formula('f(X)')]
        table_data = [header]
        index_color = "#BDD6EE"
        header_color = "#FFE599"
        colors = {
            (0, 0): index_color,
            (0, 1): header_color,
            (0, 2): header_color,
            (0, 3): header_color
        }
        for i, sol in enumerate(self.solution):
            row = [
                str(i),
                str(round(float(sol.x1), 4)),
                str(round(float(sol.x2), 4)),
                str(round(float(sol.value), 4))
            ]
            table_data.append(row)
            colors[(i + 1, 0)] = index_color
        return Table(table_data, colors)

    @image
    def _fill_steps_plot_image(self):
        plotter = NLPMethodPlotter(self.method.objective, self.solution)
        plotter.save_png(pic_path)
        return pic_path
