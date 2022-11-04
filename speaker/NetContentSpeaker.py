import re
import pyttsx3
import requests
from bs4 import BeautifulSoup


class NetContentSpeaker(object):
    def __init__(self):
        self.tag = "NetContentSpeaker"

    def log(self, log):
        print(self.tag, log)

    def start(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = []
        for i in range(len(soup.select('p'))):
            article = soup.select('p')[i]
            # temp = BeautifulSoup(str(article), "html.parser")
            matcher = re.compile(r"<p .*?><span .*?>(.*?)</span></p>", re.S)
            texts = re.findall(matcher, str(article))
            # article = article.getValue()
            if len(texts) > 0:
                text = texts[0]
                if "<strong " in text and "<span" in text:
                    continue
                elif "<strong " in text:
                    matcher = re.compile(r"<strong .*?>(.*?)</strong>", re.S)
                    contents = re.findall(matcher, str(text))
                    if len(contents) > 0:
                        content = contents[0]
                        if "<br" not in content and "-" not in content:
                            self.log(content)
                            articles.append(content)
                else:
                    self.log(text)
                    articles.append(text)

        result = " ".join(articles)
            # articles.append(article)
        # contents = " ".join(articles)
        self.log(result)
        self.play_text(result)

    def play_text(self, text):
        engine = pyttsx3.init()
        # voices = engine.getProperty('voices')
        # engine.setProperty('voice', voices[0].id)
        self.log("开始播放语音")
        engine.say(text)
        engine.runAndWait()
        self.log("播放语音结束")
        engine.stop()


if __name__ == '__main__':
    speaker = NetContentSpeaker()
    speaker.log("start")
    speaker.start("https://mp.weixin.qq.com/s/_DWfzFT4ClA3w3zb5qFENw")
    # speaker.play_text("中秋快乐")
    speaker.log("end")
