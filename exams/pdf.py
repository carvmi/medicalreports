from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

cnv = canvas.Canvas("laudo.pdf")
cnv.save()
