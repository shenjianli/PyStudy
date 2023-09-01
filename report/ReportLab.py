from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image

from report.Graphs import Graphs


class ReportLab(object):
    def __init__(self):
        self.tag = "report"
        pdfmetrics.registerFont(TTFont('font', 'font.TTF'))

    def log(self, msg):
        print(self.tag, msg)

    def start(self):
        self.log("开始")
        content = list()
        content.append(Graphs.draw_title('数据分析就业薪资'))
        content.append(Graphs.draw_img('log.jpeg'))
        content.append(Graphs.draw_text('众所周知，大数据分析师岗位是香饽饽，近几年数据分析热席卷了整个互联网行业，与数据分析的相关的岗位招聘、培训数不胜数。很多人前赴后继，想要参与到这波红利当中。那么数据分析师就业前景到底怎么样呢？'))
        content.append(Graphs.draw_title(''))
        content.append(Graphs.draw_little_title('不同级别的平均薪资'))

        data = [
            ('职位名称', '平均薪资', '较上年增加率'),
            ('数据分析师', '18.5K', '25%'),
            ('高级数据分析师', '25.5K', '14%'),
            ('资深数据分析师', '29.3K', '10%')
        ]
        content.append(Graphs.draw_table(*data))

        content.append(Graphs.draw_title(''))
        content.append(Graphs.draw_little_title('热门城市的就业情况'))

        b_data = [(25400, 12900, 20100, 20300, 20300, 17400), (15800, 9700, 12982, 9283, 13900, 7623)]
        ax_data = ['BeiJing', 'ChengDu', 'ShenZhen', 'ShangHai', 'HangZhou', 'NanJing']
        leg_items = [(colors.red, '平均薪资'), (colors.green, '招聘量')]

        content.append(Graphs.draw_bar(b_data, ax_data, leg_items))

        doc = SimpleDocTemplate('report.pdf', pagesize=letter)
        doc.build(content)


# 未成功
if __name__ == '__main__':
    pdfmetrics.registerFont(TTFont('font', 'font.TTF'))
    reportlab = ReportLab()
    reportlab.start()