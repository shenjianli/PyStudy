import pyttsx3,PyPDF2
class PdfReader(object):
    def __init__(self):
        self.tag = "PdfReader"

    def log(self, log):
        print(self.tag, log)

    def start(self):
        pdfReader = PyPDF2.PdfFileReader(open('pdf_reader.pdf','rb'))
        speaker = pyttsx3.init()
        self.log("总页数{}".format(pdfReader.numPages))
        for page_num in range(pdfReader.numPages):
            text = pdfReader.getPage(page_num).extractText()
            speaker.say(text)
            self.log(f"播放 {page_num} 页 内容 : {text}")
            speaker.runAndWait()

        speaker.stop()


if __name__ == '__main__':
    pdfReader = PdfReader()
    pdfReader.start()