#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time

from loguru import logger
import requests
from lxml import etree
from fake_useragent import UserAgent


class ChickenSoup:
    def __init__(self):
        self.tag = "chicken soup"
        logger.add("log.txt")
        self.is_dev = True
        self.url = "https://www.nihaowua.com/home.html"

    def start(self):
        if self.is_dev:
            logger.debug("start")
        headers = {
            'User-Agent': self.get_random_ua()
        }
        count = 0
        with open('soup.txt', 'a') as f:
            while True:
                res = requests.get(url=self.url, headers=headers, timeout=30)
                res.encoding = 'utf-8'
                if self.is_dev:
                    print(res.text)
                selector = etree.HTML(res.content)
                xpath_reg = "//section/div/*/text()"
                results = selector.xpath(xpath_reg)
                content = results[0]
                f.write(content + '\n')
                if self.is_dev:
                    logger.info(content)
                count += 1
                if self.is_dev:
                    logger.info("****** 正在爬取中，这是第{}次爬取 *********".format(count))
                time.sleep(3)

    def get_random_ua(self):
        ua = UserAgent()
        result = ua.random
        if self.is_dev:
            print("ua:{}".format(result))
        return result


if __name__ == '__main__':
    chicken_soup = ChickenSoup()
    chicken_soup.start()
