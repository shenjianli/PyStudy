#!/usr/bin/python3
# -*- coding:utf-8 -*-
import re
import ssl

import urllib3
from loguru import logger
from fake_useragent import UserAgent
urllib3.disable_warnings()

def download(req_url, user_agent=UserAgent().random):
    logger.debug(f'Downloading:{req_url}')
    headers = {'User-agent': user_agent}
    http = urllib3.PoolManager(cert_reqs=ssl.CERT_NONE)
    try:
        resp = http.urlopen('GET', req_url, headers=headers, retries=5)
        html = resp.data.decode('gbk')
    except Exception as e:
        logger.debug(f'Download error:{e}')
        html = None
    return html

import urllib.parse
def crawl_sitemap(net_url):
    sitemap = download(net_url)
    links = re.findall('<a target="_blank" href="(.*?)"',sitemap)
    for link in links:
        link = urllib.parse.urljoin(net_url, link)
        logger.info(f'link={link}')

import re

def find_element(net_url):
    html = download(net_url)
    print(html)
    html = str(html).replace("\n","")
    datas = re.findall('<ul class="news-list">(.*?)</ul>', html)
    logger.info(datas)

from bs4 import BeautifulSoup

def bs_print_test():
    html = '<ul class=country><li>Area<li>Population</ul>'
    soup = BeautifulSoup(html, 'html.parser')
    fixed_html = soup.prettify()
    print(fixed_html)
    ul = soup.find('ul', attrs={'class':'country'})
    print(ul.find('li'))
    print(ul.findAll('li'))

def bs_print(net_url):
    html = download(net_url)
    soup = BeautifulSoup(html)
    print(soup.prettify())
    div = soup.find(attrs={'class':'section classification-section'})
    print(div)
    ul = div.find(attrs={'class':'news-list classification-nav clearfix'})
    print(ul)
    lis = ul.findAll('li')
    print(lis)
    for li in lis:
        print(li.find('a'))
        print(li.find('a').text)
        print(li.find('a').attrs['href'])
        print(urllib.parse.urljoin(net_url,li.find('a').attrs['href']))

import lxml.html
from lxml import etree
def test_lxml():
    broken_html = '<ul class=country><li>Area<li>Population</ul>'
    tree = lxml.html.fromstring(broken_html)
    fixed_html = lxml.html.tostring(tree, pretty_print=True)
    print(fixed_html)
    lis = tree.cssselect('li')
    print(lis)
    print(lis[0].text_content())


def lxml_print(net_url):
    html = download(net_url)
    tree = lxml.html.fromstring(html)
    fixed_html = lxml.html.tostring(tree, pretty_print=True)
    print(fixed_html)

    ehtml = etree.HTML(html)
    result = etree.tostring(ehtml).decode('utf-8')
    print(result)
    # 选择所有 ul 标签
    hrefs = ehtml.xpath('//ul[@class="news-list classification-nav clearfix"]/li/a/@href')
    href_texts = ehtml.xpath('//ul[@class="news-list classification-nav clearfix"]/li/a/text()')
    print(hrefs)
    print(href_texts)

    bao_hrefs = ehtml.xpath('//ul[@class="news-list"]/li/a[last()]/@href')
    bao_hrefs_texts = ehtml.xpath('//ul[@class="news-list"]/li/a[last()]/text()')
    print(bao_hrefs)
    print(bao_hrefs_texts)

    rmd_hrefs = ehtml.xpath('//ul[@class="rank-list recommend-list"]/li/a/@href')
    rmd_hrefs_content = ehtml.xpath('//ul[@class="rank-list recommend-list"]/li/a/@title')
    print(rmd_hrefs)
    print(rmd_hrefs_content)

    pass


if __name__ == '__main__':
    url = "https://xiaohua.zol.com.cn"
    # content = download(url)
    # logger.info(content)
    # crawl_sitemap(url)
    # find_element(url)
    # bs_print(url)
    # test_lxml()
    lxml_print(url)