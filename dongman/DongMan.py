import os.path
import re

import requests


class DongMan(object):
    def __init__(self):
        self.TAG = "dong_man"
        self.headers = {
            'referer': 'https://www.dongmanmanhua.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
        }

    def log(self, log):
        print(self.TAG, log)

    def start(self):
        for page in range(8, 0, -1):
            # 目录页面
            link = f"https://www.dongmanmanhua.cn/ANCIENTCHINESE/jianzunguilai/list?title_no=1639&page={page}"
            self.log(page)
            # 调用获取章节链接 / 漫画名字 / 章节名字 函数
            name, chapter_url_list, title_list = self.get_info(link)
            for chapter_url, chapter_title in zip(chapter_url_list,title_list):
                chapter_url = 'https:' + chapter_url
                img_url_list = self.get_img_url(chapter_url)
                num = 1
                for img_url in img_url_list:
                    title = chapter_title + str(num) + ".jpg"
                    self.save(name,title,img_url)
                    num += 1

    def save(self, name, title, img_url):
        file = f'img/{name}/'
        if not os.path.exists(file):
            os.makedirs(file)
        img_content = self.get_response(img_url).content
        with open(file + title, "wb") as f:
            f.write(img_content)
        self.log(name + title)

    def get_img_url(self,chapter_url):
        chapter_data = self.get_response(chapter_url).text
        img_url_list = re.findall('alt="image" class="_images _centerImg" data-url="(.*?)"',chapter_data)
        return img_url_list

    def get_info(self, link):
        # 调用发送请求
        html_data = self.get_response(link).text
        name = re.findall("title_title:'(.*?)'", html_data)[0]
        chapter_url_list = re.findall('data-sc-name="PC_detail-page_related-title-list-item".*?href="(.*?)"', html_data, re.S)
        title_list = re.findall('<span class="subj"><span>(.*?)</span></span>',html_data)
        self.log(chapter_url_list)
        return name, chapter_url_list, title_list

    def get_response(self, link):
        # 发送请求
        response = requests.get(url=link, headers=self.headers)
        return response


if __name__ == '__main__':
    dongman = DongMan()
    dongman.start()