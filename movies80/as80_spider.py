#!/usr/bin/python3
# -*- coding:utf-8 -*-
from lxml import etree

import requests
from loguru import logger
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter


def get_random_ua():
    ua = UserAgent()
    return ua.random

class A80sSpider:
    def __init__(self):
        self.tag = "80s"
        logger.add("s80_log.txt")
        self.is_dev = True
        self.headers = {
            'User-Agent': get_random_ua()
        }
        self.total_page = 10
        self.start_page = 0

    def to_get_url(self,host, page_num):
        self.start_page = page_num
        req_host = "http://www.80s.tw"
        s = requests.Session()
        s.mount(host, HTTPAdapter(max_retries=10))
        res = s.get(host, headers=self.headers, timeout=10)
        res.encoding = 'utf-8'
        if self.is_dev:
            logger.debug(f'host = {host}, content = {res.content}')
        logger.info(f'{res.status_code} -->{page_num}:{self.total_page}')
        if res.status_code != 200:
            logger.info(f"请求失败 {res.status_code}")
            return
        html = etree.HTML(res.content)
        urls = html.xpath('//ul[@class="me1 clearfix"]/li/a/@href')
        titles = html.xpath('//ul[@class="me1 clearfix"]/li/a/@title')
        if self.is_dev:
            logger.debug(urls)
            logger.debug(titles)
        j = 0
        try:
            with open("all_v3.txt","at") as f:
                for url in urls:
                    url = req_host + url
                    res2 = s.get(url, headers=self.headers, timeout=10)
                    res2.encoding = 'utf-8'
                    if res2.status_code == 200:
                        html2 = etree.HTML(res2.content)
                        if self.is_dev:
                            logger.debug(f'url = {url}, content = {res2.content}')
                        try:
                            movie_url = html2.xpath('//span[@class="xunlei dlbutton1"]/a/@href')[0].strip()
                            img = html2.xpath('//div[@class="img"]/img/@src')[0].strip()
                            info = html2.xpath('//div[@class="clearfix"]/span/a/text()')[0]
                            #release_date = html2.xpath('//div[@class="clearfix"]/span/text()')
                            #time_long = html2.xpath('//div[@class="clearfix"]/span/text()')
                            #score = html2.xpath('//div[@style="float:left;margin-right:10px;"]/text()')
                            # content = html2.xpath('//div[@class="clearfix" @id="movie_content"]/text()')[0].strip()
                            # logger.info(f"info = {content}")
                        except:
                            continue
                        # logger.info(f"视频详情：url = {movie_url}, img = {img}, info = {info}, release_date = {release_date}")
                        # logger.info(f"视频详情：time_long = {time_long}, score = {score}, content = {content}")
                        f.write(url+" | " + titles[j] + " | " + movie_url + " | " + img + " | " + info + "\n")
                        j+= 1
                f.close()
        except Exception as e:
            print(e)


    def start(self, start, end):
        if self.is_dev:
            logger.debug("start")
        self.total_page = end
        num = start
        try:
            for i in range(start, end + 1):
                if i == 1:
                    host = "https://www.80s.tw/movie/list"
                else:
                    host = "https://www.80s.tw/movie/list/-----p/{}".format(i)
                self.to_get_url(host, i)
                num = i
        except Exception as e:
            # self.start(num,self.total_page)
            print(f"异常 {e}")
        if self.is_dev:
            logger.debug("end")

if __name__ == '__main__':
    s80 = A80sSpider()
    s80.start(1, 3)