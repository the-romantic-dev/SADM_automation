from report.model.template.document_template import DocumentTemplate
from report.model.template.template_filler import TemplateFiller


class NLPMethodTF(TemplateFiller):
    def __init__(self, template: DocumentTemplate):
        super().__init__(template)

    