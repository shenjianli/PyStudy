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
from moviepy.editor import *

# http://www.hanyupinyin.cn
class PinYin:
    def __init__(self):
        self.url = "http://www.hanyupinyin.cn/biao/shengmu/b.html"
        self.mp3_base_url = "http://m.m.hanyupinyin.cn/mp3/"
        self.base_url = "http://www.hanyupinyin.cn"
        self.tag = "PinYin"
        logger.add("log.txt")
        self.is_dev = True
        self.save_path = "img"
        self.mp3_save_path = "mp3"
        self.word_list_url = "biao"
        self.project_root_path = os.getcwd()
        self.base_shengdiao_url = "http://du.hanyupinyin.cn/shengdiao.html"
        self.mp3_shengdiao_base_url = "http://du.hanyupinyin.cn/du/pinyin/"
        self.ke_ben_url = "http://www.hanyupinyin.cn/pinyintu/keben.html"

    def get_random_ua(self):
        ua = UserAgent()
        ua = ua.random
        if self.is_dev:
            logger.info(f'随机 ua 为： {ua}')
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

    def get_urls(self,url):
        try:
            headers = {
                "X-Requested-Width": "XMLHttpRequest",
                "User-Agent": self.get_random_ua()
            }
            url = urllib.parse.urljoin(self.base_url,url)
            if len(url) > 0:
                req = requests.get(url, headers=headers)
                req.encoding = 'utf-8'
                content = req.text
                # if self.is_dev:
                #     print(f'content {content}')
                soup = BeautifulSoup(content, 'html.parser')
                # print(soup.prettify())
                sections = soup.find_all(class_='button hanyu05 pinyin05')
                if len(sections) > 0:
                    urls = []
                    for section in sections:
                        if self.is_dev:
                            print(f' section {section}')
                        hrefs = re.findall('href="(.*?)"', str(section))
                        if len(hrefs) > 0:
                            urls.append(urllib.parse.urljoin(self.base_url,str(hrefs[0])))
                    print(urls)
                    return urls
                else:
                    print("未找到 large-8 medium-8 cell 标签")


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
            with open(file_path + os.path.sep + name, 'wb') as f:
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
                logger.info("{} 保存成功".format(name))
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
        urls = self.get_urls(self.word_list_url)
        if urls is not None and len(urls) > 0:
            for url in urls:
                self.download_word_and_zip(url)

    def start_shengdiao(self):
        try:
            headers = {
                "X-Requested-Width": "XMLHttpRequest",
                "User-Agent": self.get_random_ua()
            }
            if len(self.base_shengdiao_url) > 0:
                req = requests.get(self.base_shengdiao_url, headers=headers)
                req.encoding = 'utf-8'
                content = req.text
                # if self.is_dev:
                #     print(f'content {content}')
                soup = BeautifulSoup(content, 'html.parser')
                print(soup.prettify())
                sections = soup.find_all(class_='expanded button-group large')
                if len(sections) > 0:
                    for section in sections:
                        if self.is_dev:
                            print(f' section {section}')
                        text_words = re.findall('mp3">(.*?)</a>', str(section))
                        mp3_urls = re.findall('mp3="(.*?)"', str(section))
                        print(f'mp3 = {mp3_urls}')
                        print(f'words = {text_words}')

                        if 0 < len(mp3_urls) == len(text_words) > 0:
                            word_data = {}
                            datas = []
                            dir_name = ""
                            for index in range(0, len(mp3_urls)):
                                data = {}
                                dir_name = mp3_urls[index]
                                dir_name = dir_name[:dir_name.rfind('.mp3') - 1]
                                print(f'dir_name = {dir_name}')
                                print(f'{index} mp3 = {mp3_urls[index]}, text = {text_words[index]}')
                                mp3_url = urllib.parse.urljoin(self.mp3_shengdiao_base_url,mp3_urls[index])
                                self.save_audio(mp3_url,mp3_urls[index],dir_name)
                                data["text"] = text_words[index]
                                data['mp3'] = self.mp3_save_path + os.path.sep + mp3_urls[index]
                                datas.append(data)
                            word_data['text'] = dir_name
                            word_data['data'] = datas
                            self.out_json_file(f'shengdiao_{dir_name}',word_data,dir_name)
                else:
                    print("未找到 expanded button-group large 标签")


        except Exception as e:
            print(e)

    def start_ke_ben(self):
        try:
            headers = {
                "X-Requested-Width": "XMLHttpRequest",
                "User-Agent": self.get_random_ua()
            }
            if len(self.ke_ben_url) > 0:
                req = requests.get(self.ke_ben_url, headers=headers)
                req.encoding = 'utf-8'
                content = req.text
                soup = BeautifulSoup(content, 'html.parser')

                sections = soup.find_all(class_='large-8 medium-8 cell')
                if len(sections) > 0:
                    for section in sections:
                        if self.is_dev:
                            print(f' section {section}')
                        # img_soup = BeautifulSoup(str(section), 'html.parser')
                        # img_labels = img_soup.find_all('img')
                        img_labels = re.findall('<img alt="" src="(.*?)"', str(section))
                        print("img")
                        print(img_labels)
                        if img_labels is not None and len(img_labels) > 0:
                            ken_ben_data = []
                            for img in img_labels:
                                img_url = urllib.parse.urljoin(self.base_url,img)
                                img_name = img_url[img_url.rfind('/') + 1:]
                                self.save_images(img_url,img_name,"")
                                ken_ben_data.append(img_name)

                        self.out_json_file('kenben',ken_ben_data,'')
                else:
                    print("未找到 large-8 medium-8 cell 标签")
        except Exception as e:
            print(e)
if __name__ == '__main__':
    pinyin = PinYin()
    # pinyin.download_word_and_zip(pinyin.url)

    # pinyin.generate_zip(pinyin.project_root_path,'b')

    # 下载课本图文
    # pinyin.start_ke_ben()
    # 下载声调
    pinyin.start_shengdiao()
    # 下载资源
    pinyin.start()

