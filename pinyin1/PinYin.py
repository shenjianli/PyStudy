#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os.path
import shutil
import time

import re
import json
import requests
from loguru import logger
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib.parse
import zipfile
from selenium import webdriver
from moviepy.editor import *


# http://hanyupinyin.org/
class PinYin:
    def __init__(self):
        self.base_url = "http://hanyupinyin.org"
        self.tag = "PinYin"
        self.is_download = True
        self.is_dev = False
        self.img_save_path = "img"
        self.mp3_save_path = "mp3"
        self.mp4_save_path = "mp4"
        self.project_root_path = os.getcwd()
        self.sheng_diao_list = ['a', 'o', 'e', 'i', 'u', 'v']

    @staticmethod
    def get_random_ua():
        ua = UserAgent()
        ua = ua.random
        return ua

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
        file_path = os.path.join(dir, self.img_save_path)
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
            with open(file_path + os.path.sep + name, 'wb') as f:
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
            with open(file_path + os.path.sep + name, 'wb') as f:
                f.write(img.content)
                logger.info("video {} 保存成功".format(name))
        except:
            pass


    # 下载资源
    def download_res(self,url):

        video_urls = self.get_video_url_dict(url)
        if video_urls is not None and len(video_urls) > 0:
            for img_url, video_url in video_urls.items():
                # 下载拼音图片
                self.save_pinyin_img(url, img_url)
                # 下载拼音视频
                self.save_pinyin_mp4(url, video_url)
                # 下载拼音音频
                self.save_pinyin_audio(url, video_url)

        # 下载拼读mp3
        self.save_pin_du_mp3(url)


    def get_pin_yin_info(self,text, url):
        data = {'text': text}
        video_urls = self.get_video_url_dict(url)
        video_datas = []
        if video_urls is not None and len(video_urls) > 0:
            for img_url, video_url in video_urls.items():

                img = self.img_save_path + os.path.sep + img_url[img_url.rfind('/') + 1:]
                word = img_url[img_url.rfind('/') + 1:img_url.rfind('.')]
                video_data = {'word': word, 'img': img, 'mp3': self.get_mp3_info(video_url)}

                word_info = self.get_mp4_and_text(video_url)
                if word_info is not None:
                    mp4 = word_info["mp4"]
                    mp4 = self.mp4_save_path + os.path.sep + mp4[mp4.rfind('/') + 1:]
                    video_data['mp4'] = mp4
                    video_data['hints'] = word_info['datas']
                video_datas.append(video_data)

        data['video'] = video_datas

        pin_du_dict = self.get_pin_du_dict(url)
        pin_du_data = []
        if pin_du_dict is not None and len(pin_du_dict) > 0:
            for key, value in pin_du_dict.items():
                pin_du_dict_data = self.get_pin_du_data_dict(key)
                pin_du_data.append(pin_du_dict_data)
        data['pin_du'] = pin_du_data
        if self.is_dev:
            print(data)
        return data

    '''
    拼音标调规则
    ɑ、o、e、i、u、ü，标调按顺序，
    标调先找老大ɑ，老大不在找老二o，
    老二o不在找老三e，老三e不在找老四i，
    一直找到小弟弟ü，i、u并列标在后。    i和u都在时，表在后面的字母上。例如：liù、guǐ
    小i小i有礼貌，标调就摘帽。
    小ü见了j q x y，还把两点藏帽里。   
    解释：单韵母ü和j q x y一起拼的时候，要把ü上的两点去掉（读音还读ü），在标调。
    例如：jǔ（举）= j + ǖ，xué（学）=x + üé，qún（群）=q + ǘn，yuán（圆）=y+ü+án，yuan是整体认读音节，不需拼读。
    '''
    def start(self):

        logger.add("log.txt")

        urls = self.get_urls(self.base_url)
        sheng_mu_list = []
        yun_mu_list = []
        zheng_ti_list = []


        sheng_mu_data = []
        yun_mu_data = []
        zheng_ti_data = []
        datas = []
        word_list_data = []

        if urls is not None and len(urls) > 0:
            for text,url in urls.items():
                if self.is_dev:
                    print(f'{text}:{url}')
                if '（' not in text:
                    if 'shengmu' in url:
                        sheng_mu_list.append(text)
                    elif 'yunmu' in url:
                        yun_mu_list.append(text)
                    elif 'ztrdyj' in url:
                        zheng_ti_list.append(text)
                else:
                    word_list_data.append(text)

        print('声母字母表:{}'.format(sheng_mu_list))
        print('韵母字母表:{}'.format(yun_mu_list))
        print('整体认读字母表:{}'.format(zheng_ti_list))

        if urls is not None and len(urls) > 0:
            for text,url in urls.items():

                if self.is_dev:
                    print(f'{text}:{url}')
                if '（' not in text:

                    # 下载资源
                    if self.is_download:
                        self.download_res(url)

                    # 解析拼读，生成json
                    data = self.get_pin_yin_info(text,url)
                    if 'shengmu' in url:
                        sheng_mu_data.append(data)
                    elif 'yunmu' in url:
                        yun_mu_data.append(data)
                    elif 'ztrdyj' in url:
                        zheng_ti_data.append(data)
                    datas.append(data)
                else:
                    word_list_data.append(text)


        print('最终数据:{}'.format(datas))
        self.out_json_file("pinyin", datas, "")
        json_str = json.dumps(datas, ensure_ascii=False)
        logger.info('最终数据:{}'.format(json_str))


        print('声母:{}'.format(sheng_mu_data))
        self.out_json_file("shengmu", sheng_mu_data, "")
        json_str = json.dumps(sheng_mu_data, ensure_ascii=False)
        logger.info('声母:{}'.format(json_str))

        print('韵母:{}'.format(yun_mu_data))
        self.out_json_file("yunmu",yun_mu_data,"")
        json_str = json.dumps(yun_mu_data, ensure_ascii=False)
        logger.info('韵母:{}'.format(json_str))

        print('整体认读:{}'.format(zheng_ti_data))
        self.out_json_file("zhengti", zheng_ti_data, "")
        json_str = json.dumps(zheng_ti_data, ensure_ascii=False)
        logger.info('整体认读:{}'.format(json_str))

        print('字母表:{}'.format(word_list_data))
        self.out_json_file("zimubiao", word_list_data, "")
        json_str = json.dumps(word_list_data, ensure_ascii=False)
        logger.info('字母表:{}'.format(json_str))

    @staticmethod
    def out_json_file(name, data, dir):
        file = os.path.join(dir,name)
        json_str = json.dumps(data,ensure_ascii=False)
        try:
            with open('{}.json'.format(file), 'w+') as f:
                f.write(json_str)
        except Exception as ex:
            print(f'Error:{str(ex)}')

    def get_mp3_info(self,video_url):
        audio_url = ""
        video_end = video_url[video_url.rfind('/') + 1:]
        video_end_array = video_end.split('-')
        if len(video_end_array) == 3:
            audio_url = self.mp3_save_path + os.path.sep + f'{video_end_array[0] + video_end_array[1][0]}.mp3'
        elif len(video_end_array) == 2:
            audio_url = self.mp3_save_path + os.path.sep + f'{video_end_array[0]}.mp3'
        return audio_url

    def save_pin_du_mp3(self, req_url):
        pin_du_dict = self.get_pin_du_dict(req_url)
        if pin_du_dict is not None and len(pin_du_dict) > 0:
            for key, value in pin_du_dict.items():
                if self.is_dev:
                    print(key, value)
                for index in range(4):
                    mp3_url = 'http://stati.hanyupinyin.org/p/{}.mp3'.format((key + str(index + 1)))
                    self.save_audio(mp3_url, '{}.mp3'.format((key + str(index + 1))), key)
                    if self.is_dev:
                        print(mp3_url)

    def save_pinyin_mp4(self,url,video_url):
        if self.is_dev:
            print(f'{url} 的视频地址有 {video_url}')
        save_dir = url[url.rfind('/') + 1:url.rfind('.')]
        if self.is_dev:
            print(save_dir)
        word_info = self.get_mp4_and_text(video_url)
        if word_info is not None:
            if self.is_dev:
                print(f'mp4:{word_info["mp4"]}, data:{word_info["datas"]}')
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
        if self.is_dev:
            print(audio_url)
        if len(audio_url) > 0:
            audio_name = audio_url[audio_url.rfind('/') + 1:]
            if len(audio_url) > 0:
                self.save_audio(audio_url,audio_name,save_dir)
    def save_mp4_by_url(self,url, save_dir):
        if self.is_dev:
            print(f'start {url} ')
        mp4_name = url[url.rfind('/') + 1:]
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
            # options = Options()
            # options.add_argument('--headless')
            # options.add_argument('--incognito')
            # options.add_argument("--window-size=1920x1080") #I added this
            browser = webdriver.Safari()
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
                        if self.is_dev:
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

    '''
       拼音标调规则
       ɑ、o、e、i、u、ü，标调按顺序，
       标调先找老大ɑ，老大不在找老二o，
       老二o不在找老三e，老三e不在找老四i，
       一直找到小弟弟ü，i、u并列标在后。    i和u都在时，表在后面的字母上。例如：liù、guǐ
       小i小i有礼貌，标调就摘帽。
       小ü见了j q x y，还把两点藏帽里。   
       解释：单韵母ü和j q x y一起拼的时候，要把ü上的两点去掉（读音还读ü），在标调。
       例如：jǔ（举）= j + ǖ，xué（学）=x + üé，qún（群）=q + ǘn，yuán（圆）=y+ü+án，yuan是整体认读音节，不需拼读。
       '''
    def get_pin_du_data_dict(self, pin_du_word):

        sheng_mu_list = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's',
         'y', 'w']

        yun_mu_list = ['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'iu', 'ie', 've', 'er', 'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong']

        data = {'word': pin_du_word}

        pinyin_array = []
        word = ""
        for index in range(len(pin_du_word)):
            # 记录上个字符串
            temp_word = word
            # 新的字符串
            word += pin_du_word[index]
            if word not in sheng_mu_list and word not in yun_mu_list:
                pinyin_array.append(temp_word)
                word = pin_du_word[index]

        pinyin_array.append(word)
        data['list'] = pinyin_array

        sheng_diao_index = 0
        for char in self.sheng_diao_list:
            for index in range(len(pinyin_array)):
                if char in pinyin_array[index]:
                    sheng_diao_index = index
                    break
            if sheng_diao_index != 0:
                break
        data['index'] = sheng_diao_index
        if self.is_dev:
            print(data)
        return data

    # 剪切前4秒的无用视频
    def handle_mp4_video(self):
        dir = self.project_root_path
        for dir_path,dir_name,file_names in os.walk(dir):
            if 'mp4' in dir_path and len(file_names) > 0:
                for mp4_file in file_names:
                    if '.mp4' in mp4_file:
                        mp4_file_path = dir_path + os.path.sep +  mp4_file
                        print(mp4_file_path)
                        self.handle_mp4_file(mp4_file_path)

    @staticmethod
    def handle_mp4_file(file_path):
        final_file_path = file_path
        video_clip = VideoFileClip(file_path).subclip(t_start=4)
        os.remove(file_path)
        video_clip.write_videofile(final_file_path, audio_codec='aac')
        logger.info('视频处理 {} 完成'.format(final_file_path))

    def delete_files(self):
        for dir_path, dir_name, file_names in os.walk(self.project_root_path):
            print(dir_path,dir_name,file_names)
            if dir_name is not None and len(dir_name) > 0:
                for dir in dir_name:
                    shutil.rmtree(dir)
            if file_names is not None and len(file_names) > 0:
                for file in file_names:
                    if '.py' not in file:
                        os.remove(file)

    def zip(self, zip_dir, zip_name):
        zip_name = os.path.join(zip_dir, '{}.zip'.format(zip_name))
        print(f'zip name {zip_name}')
        zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        time.sleep(2)
        for dir_path, dir_names, filenames in os.walk(zip_dir):
            print(dir_path,dir_names,filenames)
            fpath = dir_path.replace(zip_dir, "")
            fpath = fpath and fpath + os.sep or ''
            print(f'fpath {fpath}')
            for filename in filenames:
                if '.py' not in filename and '.txt' not in filename and '.DS_Store' not in filename and '.zip' not in filename:
                    zip.write(os.path.join(dir_path, filename), fpath + filename)
                    print("{}压缩中...".format(filename))
        print('{}压缩成功'.format(zip_name))
        zip.close()

if __name__ == '__main__':

    pinyin = PinYin()
    # 删除无用文件
    pinyin.delete_files()
    # 下载资源及生成json文件
    pinyin.start()
    # 处理无用视频片段
    pinyin.handle_mp4_video()
    # 打包zip
    pinyin.zip(pinyin.project_root_path,"pinyin")

    # 测试使用
    # pinyin.download_word_and_zip(pinyin.url)
    # pinyin.generate_zip(pinyin.project_root_path,'b')
    # pinyin.start_shengdiao()
    # pinyin.delete_files()


