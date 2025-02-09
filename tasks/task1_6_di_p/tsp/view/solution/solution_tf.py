from report.model.template.template_filler import TemplateFiller
from report.model.template.tf_decorators import sub_tf


@sub_tf
class SolutionTF(TemplateFiller):
    def __init__(self):
        self.task_table = task_table
        self.variant = variant
        self.solution_data = solution_data
        template = DocumentTemplate(template_path)
        super().__init__(template)