from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, Image

pdfmetrics.registerFont(TTFont('font', 'font.TTF'))

class Graphs:

    @staticmethod
    def draw_title(title : str):
        style = getSampleStyleSheet()
        ct = style['Heading1']
        # ct.fontName = 'font'
        ct.fontSize = 18
        ct.leading = 50
        ct.textColor = colors.green
        ct.alignment = 1
        ct.bold = True
        return Paragraph(title, ct)

    @staticmethod
    def draw_little_title(title : str):
        style = getSampleStyleSheet()
        ct = style['Normal']
        # ct.fontName = 'font'
        ct.fontSize = 15
        ct.leading = 30
        ct.textColor = colors.red
        return Paragraph(title, ct)

    @staticmethod
    def draw_text(text: str):
        style = getSampleStyleSheet()
        ct = style['Normal']
        # ct.fontName = 'font'
        ct.fontSize = 12
        ct.wordWrap = 'CJK'
        ct.alignment = 0
        ct.firstLineIndent = 32
        ct.leading = 25
        return Paragraph(text,ct)

    @staticmethod
    def draw_table(*args):
        col_width = 120
        style = [
            ('FONTNAME', (0, 0), (-1, -1), 'font'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkslategray),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]
        table = Table(args, colWidths=col_width, style=style)
        return table

    @staticmethod
    def draw_bar(bar_data: list, ax: list, items: list):
        drawing = Drawing(500, 250)
        bc = VerticalBarChart()
        bc.x = 45
        bc.y = 45
        bc.height = 200
        bc.width = 350
        bc.data = bar_data
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 5000
        bc.valueAxis.valueMax = 26000
        bc.valueAxis.valueStep = 2000
        bc.categoryAxis.labels.dx = 2
        bc.categoryAxis.labels.dy = -8
        bc.categoryAxis.labels.angle = 20
        bc.categoryAxis.categoryNames = ax

        leg = Legend()
        # leg.fontName = 'font'
        leg.alignment = 'right'
        leg.boxAnchor = 'ne'
        leg.x = 475
        leg.y = 240
        leg.dxTextSpace = 10
        leg.columnMaximum = 3
        leg.colorNamePairs = items
        drawing.add(leg)
        drawing.add(bc)
        return drawing

    @staticmethod
    def draw_img(path):
        img = Image(path)
        img.drawWidth = 5*cm
        img.drawHeight = 8*cm
        return img