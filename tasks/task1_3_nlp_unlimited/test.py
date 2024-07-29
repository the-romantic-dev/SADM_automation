from docxtpl import DocxTemplate

doc = DocxTemplate("temple.docx")
context = {'var1': "GaySUKA1", 'var2': "FFFFFFFFF", 'var3': 111}
doc.render(context)
doc.save("temple_filled.docx")
