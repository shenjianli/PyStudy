#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os.path
import re
import time
import json
import requests
from loguru import logger
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib.parse
import zipfile
from selenium import webdriver
from selenium.webdriver.safari.options import Options
# http://hanyupinyin.org/
class PinYin:
    def __init__(self):
        self.url = "http://www.hanyupinyin.cn/biao/shengmu/b.html"
        self.mp3_base_url = "http://m.m.hanyupinyin.cn/mp3/"
        self.mp4_base_url = "http://stati.hanyupinyin.org/v/"
        self.base_url = "http://hanyupinyin.org"
        self.tag = "PinYin"
        logger.add("log.txt")
        self.is_dev = True
        self.save_path = "img"
        self.mp3_save_path = "mp3"
        self.mp4_save_path = "mp4"
        self.word_list_url = "biao"
        self.project_root_path = os.getcwd()
        self.base_shengdiao_url = "http://du.hanyupinyin.cn/shengdiao.html"
        self.mp3_shengdiao_base_url = "http://du.hanyupinyin.cn/du/pinyin/"

    @staticmethod
    def get_random_ua():
        ua = UserAgent()
        ua = ua.random
        return ua

    def download_word_and_zip(self,url):
        if self.is_dev:
            print("start")
        try:
            headers = {
                "X-Requested-Width": "XMLHttpRequest",
                "User-Agent": self.get_random_ua()
            }
            if len(url) > 0:
                req = requests.get(url, headers=headers)
                req.encoding = 'utf-8'
                content = req.text
                # if self.is_dev:
                #     print(f'content {content}')
                soup = BeautifulSoup(content, 'html.parser')
                print(soup.prettify())
                sections = soup.find_all(class_='large-8 medium-8 cell')
                if len(sections) > 0:
                    section = sections[0]
                    if self.is_dev:
                        print(f' section {section}')
                    if len(section) > 0:
                        word_soup = BeautifulSoup(str(section), 'html.parser')
                        word_sections = word_soup.find_all(class_='button hanyusm pinyinsm large')
                        if len(word_sections) > 0:
                            word = str(word_sections[0].text).replace(' ','')
                            final_label = ""
                            p_labels = re.findall('<p>\r\n(.*?)</p>', str(section))
                            if len(p_labels) > 0:
                                for label_data in p_labels:
                                    print(f'1 label_data = {label_data}')
                                    if (word + "：") in str(label_data):
                                        final_label = str(label_data)
                                        break

                            if len(p_labels) == 0 or len(final_label) <= 0:
                                p_labels = re.findall('<p>(.*?)</p>', str(section))
                                for label_data in p_labels:
                                    print(f'2 label_data = {label_data}')
                                    if (word + "：") in str(label_data):
                                        final_label = str(label_data)
                                        break

                            if len(p_labels) == 0 or len(final_label) <= 0:
                                p_labels = re.findall('<p class="text-center">(.*?)</p>', str(section))
                                for label_data in p_labels:
                                    print(f'3 label_data = {label_data}')
                                    if (word + "：") in str(label_data):
                                        final_label = str(label_data)
                                        break

                            if len(p_labels) == 0 or len(final_label) <= 0:
                                p_labels = re.findall('<p class="text-center">\r\n(.*?)</p>', str(section))
                                for label_data in p_labels:
                                    print(f'4 label_data = {label_data}')
                                    if (word + "：") in str(label_data):
                                        final_label = str(label_data)
                                        break

                            mp3_paths = re.findall('mp3="(.*?)"', str(section))
                            img_paths = re.findall('src="(.*?)"', str(section))
                            if len(word) > 0 and len(mp3_paths) > 0 and len(img_paths) > 0:
                                data = {}
                                label = final_label
                                label = label[label.rfind("：") + 1:]
                                mp3_path = self.mp3_base_url + str(mp3_paths[0])
                                img_path = self.base_url + str(img_paths[0])
                                print(f"拼音：{word}")
                                print(f'音频：{mp3_path}')
                                print(f'图片: {img_path}')
                                print(f'发音：{label}')
                                data['text'] = word
                                if len(img_path) > 0:
                                    img_name = img_path[img_path.rfind("/") + 1:]
                                    if self.is_dev:
                                        print(f"img url {img_path}")
                                        print(f"img name {img_name}")
                                    data['img'] = self.save_path + os.path.sep + img_name
                                    logger.info(f"img url {img_path}")
                                    self.save_images(img_path, img_name,word.replace('ü','v'))

                                if len(mp3_path) > 0:
                                    audio_name = mp3_path[mp3_path.rfind("/") + 1:]
                                    if self.is_dev:
                                        print(f"audio url {mp3_path}")
                                        print(f"audio name {audio_name}")
                                    data['mp3'] = self.mp3_save_path + os.path.sep + audio_name
                                    logger.info(f"audio url {mp3_path}")
                                    self.save_audio(mp3_path, audio_name,word.replace('ü','v'))
                                data['label'] = label
                                self.out_json_file(word.replace('ü','v'),data,word.replace('ü','v'))

                                self.generate_zip(self.project_root_path,word.replace('ü','v'))
                            else:
                                print(f"{url}缺少相关资源")
                                print(f"拼音：{word}")
                                print(f'音频：{mp3_paths}')
                                print(f'图片: {img_paths}')
                                print(f'发音：{final_label}')
                else:
                    print("未找到 large-8 medium-8 cell 标签")


        except Exception as e:
            print(e)

    def get_urls(self, url):
        try:
            headers = {
                "X-Requested-Width": "XMLHttpRequest",
                "User-Agent": self.get_random_ua()
            }
            if len(url) > 0:
                req = requests.get(url, headers=headers)
                req.encoding = 'utf-8'
                content = req.text
                soup = BeautifulSoup(content, 'html.parser')
                if self.is_dev:
                    print(soup.prettify())
                sections = soup.find_all(class_='con2 clearfix')
                if len(sections) > 0:
                    urls = {}
                    for section in sections:

                        section_soup = BeautifulSoup(str(section), 'html.parser')
                        if self.is_dev:
                            print(section_soup.prettify())

                        li_sections = section_soup.find_all("li")

                        if len(li_sections) > 0:
                            for li_section in li_sections:
                                if self.is_dev:
                                    print(f'li_section = {li_section}')
                                    print(f'text = {li_section.text}')
                                if len(li_section.text) < 6:
                                    hrefs = re.findall('href="(.*?)"', str(li_section))
                                    if self.is_dev:
                                        print(f'href = {hrefs}')
                                    if len(hrefs) > 0:
                                        urls[li_section.text] = urllib.parse.urljoin(self.base_url, str(hrefs[0]))
                    if self.is_dev:
                        print(urls)
                    logger.info(f'get_urls = {urls}')
                    return urls
                else:
                    print("con2 clearfix not found")
        except Exception as e:
            print(e)

    def save_images(self, src, name,dir):
        headers = {
            "X-Requested-Width": "XMLHttpRequest",
            "User-Agent": self.get_random_ua()
        }
        file_path = os.path.join(dir, self.save_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        try:
            img = requests.get(src, headers=headers)
            with open(file_path + os.path.sep + name, 'ab') as f:
                f.write(img.content)
                logger.info("{} 保存成功".format(name))
        except:
            pass


    def save_audio(self, src, name, dir):
        headers = {
            "X-Requested-Width": "XMLHttpRequest",
            "User-Agent": self.get_random_ua()
        }
        file_path = os.path.join(dir, self.mp3_save_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        try:
            img = requests.get(src, headers=headers)
            with open(file_path + os.path.sep + name, 'ab') as f:
                f.write(img.content)
                logger.info("audio {} 保存成功".format(name))
        except:
            pass


    def save_video(self, src, name, dir):
        headers = {
            "X-Requested-Width": "XMLHttpRequest",
            "User-Agent": self.get_random_ua()
        }
        file_path = os.path.join(dir, self.mp4_save_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        try:
            img = requests.get(src, headers=headers)
            with open(file_path + os.path.sep + name, 'ab') as f:
                f.write(img.content)
                logger.info("video {} 保存成功".format(name))
        except:
            pass

    def out_json_file(self,name,data, dir):
        file = os.path.join(dir,name)
        json_str = json.dumps(data,ensure_ascii=False)
        try:
            with open('{}.json'.format(file), 'w') as f:
                f.write(json_str)
        except Exception as ex:
            print(f'Error:{str(ex)}')
    def generate_zip(self,dist_dir, dist_name):

        zip_name = os.path.join(dist_dir, '{}.zip'.format(dist_name))
        print(f'zip name {zip_name}')
        zip = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
        time.sleep(2)
        target_dir = os.path.join(dist_dir,dist_name)
        print(f'target dir {target_dir}')
        for dir_path,dir_names,filenames in os.walk(target_dir):
            fpath = dir_path.replace(target_dir,"")
            fpath = fpath and fpath + os.sep or ''
            print(f'fpath {fpath}')
            print(f'dir_names {dir_names}')
            print(f'filenames {filenames}')

            for filename in filenames:
                zip.write(os.path.join(dir_path,filename), fpath + filename)
                print("{}压缩中...".format(filename))
        print('{}压缩成功'.format(zip_name))
        zip.close()

    def start(self):
        urls = self.get_urls(self.base_url)

        if urls is not None and len(urls) > 0:
            for text,url in urls.items():
                if self.is_dev:
                    print(f'{text}:{url}')
                if '（' not in text:
                    video_urls = self.get_video_url_dict(url)
                    if video_urls is not None and len(video_urls) > 0:
                        for img_url,video_url in video_urls.items():
                            # self.save_pinyin_img(url, img_url)
                            # self.save_pinyin_mp4(url,video_url)
                            # self.save_pinyin_audio(url, video_url)
                            print('')

        # 获取第一个元素
        # key, value = next(iter(urls.items()))
        # video_urls = self.get_video_url_dict(value)
        # img_key, video_value = next(iter(video_urls.items()))
        # print(key, value)
        # print(img_key,video_value)
        #
        # video_infos = self.get_mp4_and_text(video_value)
        # mp4_url = video_infos['mp4']
        # self.save_mp4_by_url(mp4_url)

    def test(self, req_url):
        if self.is_dev:
            print(f'start {req_url} ')
        self.get_pin_du_dict(req_url)


    def save_pinyin_mp4(self,url,video_url):
        if self.is_dev:
            print(f'{url} 的视频地址有 {video_url}')
        save_dir = url[url.rfind('/') + 1:url.rfind('.')]
        if self.is_dev:
            print(save_dir)
        word_info = self.get_mp4_and_text(video_url)
        if word_info is not None:
            if self.is_dev:
                print(f'mp4:{word_info["mp4"]}, data:{word_info["data"]}')
            mp4_url = word_info['mp4']
            if len(mp4_url) > 0:
                self.save_mp4_by_url(mp4_url, save_dir)

    def save_pinyin_img(self,url,img_url):
        if self.is_dev:
            print(f'{url} 的视频地址有 {img_url}')
        save_dir = url[url.rfind('/') + 1:url.rfind('.')]
        img_name = img_url[img_url.rfind('/') + 1:]
        if self.is_dev:
            print(save_dir)
        if len(img_url) > 0:
            self.save_images(img_url,img_name,save_dir)

    def save_pinyin_audio(self,url,video_url):
        if self.is_dev:
            print(f'{url} 的视频地址有 {video_url}')
        save_dir = url[url.rfind('/') + 1:url.rfind('.')]
        audio_url = ""
        video_end = video_url[video_url.rfind('/') + 1:]
        video_end_array = video_end.split('-')
        if len(video_end_array) == 3:
            audio_url = f'http://stati.hanyupinyin.org/p/{video_end_array[0] + video_end_array[1][0]}.mp3'
        elif len(video_end_array) == 2:
            audio_url = f'http://stati.hanyupinyin.org/p/{video_end_array[0]}.mp3'
        print(audio_url)
        if len(audio_url) > 0:
            audio_name = audio_url[audio_url.rfind('/') + 1:]
            if len(audio_url) > 0:
                self.save_audio(audio_url,audio_name,save_dir)
    def save_mp4_by_url(self,url, save_dir):
        if self.is_dev:
            print(f'start {url} ')
        mp4_name = url[url.rfind('/') + 1:]
        dir = url[url.rfind('/') + 1:url.rfind('.')]
        if self.is_dev:
            print(mp4_name, save_dir)
        self.save_video(url,mp4_name,save_dir)
    def get_mp4_and_text(self,req_url):
        try:
            content = self.get_content_net(req_url)
            if len(content) > 0:
                data_dict = {}
                soup = BeautifulSoup(content, 'html.parser')
                if self.is_dev:
                    print(soup.prettify())

                # 视频地址
                url_end = req_url[req_url.rfind('/')+1:]
                # http://stati.hanyupinyin.org/v/a1.mp4
                if self.is_dev:
                    print(url_end)
                if len(url_end) > 0:
                    split_urls = url_end.split('-')
                    mp4_end = ""
                    if len(split_urls) == 3:
                        mp4_end = split_urls[0] + split_urls[1][:1]
                    elif len(split_urls) == 2:
                        mp4_end = split_urls[0]
                    if len(mp4_end) > 0:
                        mp4_url = f'http://stati.hanyupinyin.org/v/{mp4_end}.mp4'
                        data_dict['mp4'] = mp4_url

                text_sections = soup.find_all(class_='pinyinCon')
                if len(text_sections) > 0:
                    text_section = text_sections[0]
                    p_soup = BeautifulSoup(str(text_section),'html.parser')
                    p_sections = p_soup.find_all('p')
                    if self.is_dev:
                        print(p_sections)
                    if len(p_sections) > 0:
                        p_data = []
                        for p_section in p_sections:
                            p_data.append(p_section.text)
                        data_dict['datas'] = p_data
            if self.is_dev:
                print(data_dict)
            logger.info(data_dict)
            return data_dict
        except Exception as e:
            print(e)
    def get_mp4_info(self,req_url):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--incognito')
            options.add_argument("--window-size=1920x1080") #I added this
            browser = webdriver.Safari(options = options)
            browser.get(req_url)
            browser.implicitly_wait(5)  # 等待页面加载完毕，最多等待5s

            content = browser.page_source
            # browser.quit()
            if len(content) > 0:
                data_dict = {}
                soup = BeautifulSoup(content, 'html.parser')
                if self.is_dev:
                    print(soup.prettify())

                # 视频地址
                sections = soup.find_all(id='jp_video_0')
                if self.is_dev:
                    print(sections)
                if len(sections) > 0:
                    section = sections[0]
                    mp4_urls = re.findall('src="(.*?)"', str(section))
                    if len(mp4_urls) > 0:
                        print(mp4_urls[0])
                        data_dict['mp4'] = mp4_urls[0]

                text_sections = soup.find_all(class_='pinyinCon')
                if len(text_sections) > 0:
                    text_section = text_sections[0]
                    p_soup = BeautifulSoup(str(text_section),'html.parser')
                    p_sections = p_soup.find_all('p')
                    if self.is_dev:
                        print(p_sections)
                    if len(p_sections) > 0:
                        p_data = []
                        for p_section in p_sections:
                            p_data.append(p_section.text)
                        data_dict['datas'] = p_data
            if self.is_dev:
                print(data_dict)
            return data_dict
        except Exception as e:
            print(e)

    # 获取网站内容
    def get_content_net(self,url):
        try:
            headers = {
                "X-Requested-Width": "XMLHttpRequest",
                "User-Agent": self.get_random_ua()
            }
            if len(url) > 0:
                req = requests.get(url, headers=headers)
                req.encoding = 'utf-8'
                return req.text
        except Exception as e:
            print(e)
            return ""

    # 获取图片与视频的对应地址
    def get_video_url_dict(self,req_url):
        try:
            content = self.get_content_net(req_url)
            if len(content) > 0:
                url_dict = {}
                soup = BeautifulSoup(content, 'html.parser')
                if self.is_dev:
                    print(soup.prettify())
                sections = soup.find_all(class_='play')

                if len(sections) > 0:
                    for section in sections:
                        if self.is_dev:
                            print(f' section {section}')
                        urls = re.findall('href="(.*?)"', str(section))
                        imgs = re.findall('src="(.*?)"', str(section))
                        if len(urls) > 0 and len(imgs):
                            url = urllib.parse.urljoin(self.base_url, urls[0])
                            url_dict[imgs[0]] = url
                            if self.is_dev:
                                print(urls, imgs)


                sheng_sections = soup.find_all(class_='con clearfix')
                if len(sheng_sections) > 0:
                    for section in sheng_sections:
                        if self.is_dev:
                            print(f' section {section}')
                        li_soup = BeautifulSoup(str(section), 'html.parser')
                        li_sections = li_soup.find_all('li')
                        for li_section in li_sections:
                            # if self.is_dev:
                            #     print(f'li_section {li_section}----{li_section.text}')
                            if "video.html" in str(li_section):
                                if self.is_dev:
                                    print(f'{li_section}')
                                hrefs = re.findall('href="(.*?)"',str(li_section))
                                imgs = re.findall('src="(.*?)"',str(li_section))
                                if len(hrefs) > 0 and len(imgs):
                                    if self.is_dev:
                                        print(hrefs, imgs)
                                    url = urllib.parse.urljoin(self.base_url, hrefs[0])
                                    url_dict[imgs[0]] = url
                if self.is_dev:
                    print(url_dict)
                logger.info(f'{req_url} 的视频地址有 {url_dict}')
                return url_dict
        except Exception as e:
            print(e)

    def get_pin_du_dict(self, req_url):
        try:
            content = self.get_content_net(req_url)
            if len(content) > 0:
                url_dict = {}
                soup = BeautifulSoup(content, 'html.parser')
                if self.is_dev:
                    print(soup.prettify())
                sections = soup.find_all(class_='con2 clearfix')

                if len(sections) > 0:
                    for section in sections:
                        if self.is_dev:
                            print(f' section {section}')
                        li_soup = BeautifulSoup(str(section), 'html.parser')
                        li_sections = li_soup.find_all('li')
                        if len(li_sections) > 0:
                            for li_section in li_sections:
                                if "/yinjie/" in str(li_section) and '.html' in str(li_section):
                                    if self.is_dev:
                                        print(f'{li_section}')
                                    hrefs = re.findall('href="(.*?)"', str(li_section))
                                    if len(hrefs) > 0:
                                        if self.is_dev:
                                            print(hrefs)
                                        url = urllib.parse.urljoin(self.base_url, hrefs[0])
                                        url_dict[li_section.text] = url
                if self.is_dev:
                    print(url_dict)
                logger.info(f'{req_url} 拼读拼音有 {url_dict}')
                return url_dict
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pinyin = PinYin()
    # pinyin.download_word_and_zip(pinyin.url)

    # pinyin.generate_zip(pinyin.project_root_path,'b')
    # pinyin.start_shengdiao()
    pinyin.test("http://www.hanyupinyin.org/yunmu/a.html")
    # pinyin.start()

