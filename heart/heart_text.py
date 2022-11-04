import re
import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from heart.HeartDB import HeartDB
from heart.UpdateDB import UpdateDB
from notify.WeChatNotification import WeChatPub


# http://www.hnbitebi.com/qh/001.html
# -------> 到  http://www.hnbitebi.com/
# http://www.hnbitebi.com/qh/999.html


class HeartText(object):
    def __init__(self):
        self.TAG = "heart text"
        self.hint_hours = '19'
        self.hint_min = '30'
        self.headers = {
            'referer': 'http://www.hnbitebi.com/hlist-11-1.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
        }
        self.base_url = "http://www.hnbitebi.com/qh/"
        self.heart_db = HeartDB()
        self.update_db = UpdateDB()
        self.wechat = WeChatPub()

    def log(self, tag, log):
        print(self.TAG, tag, log)

    def has_character(self, content):
        my_re = re.compile(r'[A-Za-z]', re.S)
        res = re.findall(my_re, content)
        if len(res):
            # self.log("has_character", '含有英文字符')
            return True
        else:
            # self.log("has_character", '不含有英文字符')
            return False

    def save_text(self, text, url):
        if '短信' in text:
            text = text.replace('短信', '微信')
        if len(text):
            self.log("save text", text)
            self.heart_db.insert_mysql_data(url, text)

    def start(self, url):
        # 发送请求
        response = requests.get(url=url, headers=self.headers)
        response.encoding = 'utf-8'
        html_data = response.text
        self.log("请求返回内容 ", html_data)
        soup = BeautifulSoup(html_data, "html.parser")
        div_data = soup.find("div", class_="con")
        self.log("div data", div_data)
        div_content = div_data.find("div")
        self.log("div_content", div_content)
        text_list = div_content.findAll("p")
        self.log("text_list", len(text_list))
        if len(text_list):
            for data in text_list:
                if not self.has_character(data.text):
                    # self.log("data", data.text)
                    if '、' in data.text:
                        final_text = data.text[data.text.find('、') + 1:]
                        # self.log("final text", final_text)
                        self.save_text(final_text, url)
                    elif '.' in data.text:
                        final_text = data.text[data.text.find('.') + 1:]
                        # self.log("final text", final_text)
                        self.save_text(final_text, url)
                    else:
                        # self.log("final text", data.text)
                        self.save_text(data.text, url)
                # else:
                # self.log("有字符", data.text)

    def start_1(self, url):
        # 发送请求
        response = requests.get(url=url, headers=self.headers)
        response.encoding = 'utf-8'
        html_data = response.text
        # self.log("请求返回内容 ", html_data)
        soup = BeautifulSoup(html_data, "html.parser")
        div_data = soup.find("div", class_="con")
        # self.log("div data", div_data)
        div_content = div_data.find("div")
        # self.log("div_content", div_content.text)
        if '\n' in div_content.text:
            # self.log("回车", div_content.text)
            matcher = re.compile(r'(.*?)\n', re.S)
            text_list = re.findall(matcher, div_content.text)
            self.log("text_list", len(text_list))
            if len(text_list):
                for data in text_list:
                    if len(data):
                        if '本文来源：' in data:
                            data = data[0:data.find('本文来源：')]
                            self.log("new data", data)
                        if not self.has_character(data):
                            # self.log("data", data.text)
                            if '、' in data:
                                final_text = data[data.find('、') + 1:]
                                # self.log("final text", final_text)
                                self.save_text(final_text, url)
                            elif '.' in data:
                                final_text = data[data.find('.') + 1:]
                                # self.log("final text", final_text)
                                self.save_text(final_text, url)
                            else:
                                # self.log("final text", data.text)
                                self.save_text(data, url)
                        # else:
                        # self.log("有字符", data.text)

    def cache_test(self, page_num):
        start_page = self.update_db.query_mysql_data()
        self.log("cache_test", "start page {}".format(start_page))
        sub_url = ""
        for index in range(0, page_num):
            self.log("index", index)
            final_num = start_page + index
            if final_num < 10:
                sub_url = "00{}.html".format(final_num)
            elif final_num < 100:
                sub_url = "0{}.html".format(final_num)
            elif final_num < 1000:
                sub_url = "{}.html".format(final_num)
            final_url = self.base_url + sub_url
            self.log("final url", final_url)
            self.start_1(final_url)
        self.update_db.insert_mysql_data(sub_url, start_page + page_num)
        self.log("cache_test", "next page num {}".format(start_page + page_num))

    def send_msg(self):
        data_item = self.heart_db.fetch_data_num(2)
        if data_item['code'] == 1:
            data_list = data_item['data']
            if len(data_list):
                for data in data_list:
                    content = data['content']
                    if len(content) > 5:
                        self.wechat.send_text_msg(content)
                        self.heart_db.update_heart_look(data['id'])
                        self.log("发送成功", content)
                        time.sleep(5)
            return 1
        else:
            return 0
        return 0

    def start_send_scheduler(self):
        heart_scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
        # corn 是周期  interval是间隔  date 是具体日期
        # 每间隔1分3秒执行一次
        # scheduler.add_job(print_time, 'interval', seconds=3, minutes=1)
        # 表示星期一到星期六，每天12：21执行一次
        heart_scheduler.add_job(heartText.send_msg, 'cron', hour=self.hint_hours, minute=self.hint_min)
        heart_scheduler.start()
        self.log("start_send_scheduler", "启动周期发送情话计划")

    def create_db_tables(self):
        self.heart_db.create_mysql_table()
        self.update_db.create_mysql_table()

    def delete_db_data(self):
        self.heart_db.delete_db_data()
        self.update_db.delete_db_data()


if __name__ == '__main__':
    heartText = HeartText()
    print("1.创建需要表数据\n"
          "2.删除本地缓存数据\n"
          "3.根据列表初始数据\n"
          "4.根据地址初始化数据\n"
          "5.启动定时发送计划\n"
          "6.结束程序运行\n")
    cmd = int(input("输入执行命令序号：\n"))
    while cmd != -1:
        print("输入的命令是：", cmd)
        if cmd == 1:
            heartText.create_db_tables()
        elif cmd == 2:
            heartText.delete_db_data()
        elif cmd == 3:
            num = int(input("请输入缓存数据页数:(1-100)\n"))
            heartText.cache_test(num)
        elif cmd == 4:
            net_url = input("请输入网址\n")
            if len(net_url):
                heartText.start_1(net_url)
        elif cmd == 5:
            heartText.start_send_scheduler()
        time.sleep(1)
        print("1.创建需要表数据\n"
              "2.删除本地缓存数据\n"
              "3.根据列表初始数据\n"
              "4.根据地址初始化数据\n"
              "5.启动定时发送计划\n"
              "6.结束程序运行\n")
        cmd = int(input("输入执行命令序号：\n"))
    print("程序结束运行")
    # print(list_1)
    # heartText.start_1("http://www.hnbitebi.com/qh/001.html")

    # heartText.cache_test(1, 10)
    # heartText.start("http://www.hnbitebi.com/ty/11411.html")
    # heartText.start("http://www.hnbitebi.com/ty/11381.html")
    # heartText.start("http://www.hnbitebi.com/ty/11328.html")
    # heartText.start("http://www.hnbitebi.com/ty/11290.html")
    # heartText.start("http://www.hnbitebi.com/hj/11287.html")

    # heartText.start_1("http://www.hnbitebi.com/am/14809.html")
    # heartText.start_1("http://www.hnbitebi.com/gx/20888.html")
    # heartText.start_1("http://www.hnbitebi.com/am/18155.html")
    # heartText.start_1("http://www.hnbitebi.com/wh/18152.html")
    # heartText.start_1("http://www.hnbitebi.com/qs/21860.html")
    # heartText.start("http://www.hnbitebi.com/qh/21745.html")
