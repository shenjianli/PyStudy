#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os.path
import re
import threading
import time
from multiprocessing import Pool, cpu_count

import requests
from loguru import logger
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

lock = threading.Lock()


class Wallpaper:
    def __init__(self):
        self.tag = "Wallpaper"
        logger.add("log.txt")
        self.is_dev = False
        self.save_path = "img"
        self.url = "https://wallhaven.cc/latest?page={}"

    def get_random_ua(self):
        ua = UserAgent()
        ua = ua.random
        if self.is_dev:
            logger.info(f'随机 ua 为： {ua}')
        return ua

    def mkdir(self, folder_name):
        path = os.path.join(self.save_path, folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
            logger.debug("创建成功{}".format(path))
            os.chdir(path)
            return True
        if self.is_dev:
            logger.debug("Folder has existed!")
        return False

    def save_images(self, src, name):
        headers = {
            "X-Requested-Width": "XMLHttpRequest",
            "User-Agent": self.get_random_ua()
        }
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        try:
            img = requests.get(src, headers=headers)
            with open(self.save_path + os.path.sep + name, 'ab') as f:
                f.write(img.content)
                logger.info("{} 保存成功".format(name))
        except:
            pass

    def clear(self, dir_path):
        if os.path.exists(dir_path):
            if os.path.isdir(dir_path):
                for d in os.listdir(dir_path):
                    path = os.path.join(dir_path, d)
                    if os.path.isdir(path):
                        self.clear(path)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                logger.info("remove the empty dir:{}".format(dir_path))

    def save_full_img(self, url):
        headers = {
            "X-Requested-Width": "XMLHttpRequest",
            "User-Agent": self.get_random_ua()
        }
        req = requests.get(url, headers=headers)
        content = req.text
        if self.is_dev:
            print(f'content {content}')
        soup = BeautifulSoup(content, 'lxml')
        sections = soup.find_all("section")
        if len(sections) > 0:
            section = sections[0]
            img_urls = re.findall('src="(.*?)"', str(section))
            if len(img_urls) > 0:
                img_url = img_urls[0]
                img_name = img_url[img_url.rfind("/") + 1:]
                if self.is_dev:
                    print(f"img url {img_url}")
                    print(f"img name {img_name}")
                logger.info(f"img url {img_url}")
                self.save_images(img_url, img_name)

    def get_urls(self, page_num):
        _urls = []
        for url in [self.url.format(page) for page in range(1, page_num)]:
            _urls.append(url)
        return _urls

    def run(self, url):
        if self.is_dev:
            logger.debug("start run")
        try:
            headers = {
                "X-Requested-Width": "XMLHttpRequest",
                "User-Agent": self.get_random_ua()
            }
            with lock:
                if len(url) > 0:
                    req = requests.get(url, headers=headers)
                    content = req.text
                    if self.is_dev:
                        print(f'content {content}')
                    soup = BeautifulSoup(content, 'lxml')
                    figures = soup.find_all("figure")
                    if len(figures) > 0:
                        for figure in figures:
                            time.sleep(2)
                            if self.is_dev:
                                print(f"figure:{figure}")
                            img_urls = re.findall('data-src="(.*?)"', str(figure))
                            net_urls = re.findall('<a class="preview" href="(.*?)"', str(figure))
                            if len(net_urls) > 0:
                                net_url = net_urls[0]
                                if self.is_dev:
                                    print(f"net url {net_url}")
                                self.save_full_img(net_url)
                            else:
                                if len(img_urls) > 0:
                                    img_url = img_urls[0]
                                    img_name = img_url[img_url.rfind("/") + 1:]
                                    # "https://w.wallhaven.cc/full/l8/wallhaven-l8z72l.png"
                                    # "https://w.wallhaven.cc/full/l8/l8z72l.jpg
                                    if self.is_dev:
                                        print(f"img url {img_url}")
                                        print(f"img name {img_name}")
                                    self.save_images(img_url, img_name)
        except Exception as e:
            print(e)

    def start(self, page_num):
        if self.is_dev:
            print("start")
        urls = self.get_urls(page_num)
        if self.is_dev:
            print(urls)
        pool = Pool(processes=cpu_count())
        try:
            pool.map(self.run, urls)
        except:
            time.sleep(30)
            pool.map(self.run, urls)
        if self.is_dev:
            print("over")


if __name__ == '__main__':
    wallpaper = Wallpaper()
    page_num = 5
    wallpaper.start(page_num)
