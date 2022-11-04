# -*- coding: UTF-8 -*-
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from os.path import exists

import requests
import json
import time
import base64
import hashlib

'''
OK
主要通过企业微信应用给企业成员发送消息
'''

CORP_ID = "ww26a52c0097ff9995"
SECRET = "gXLmvP1Hku6ucklf97JM6nvuPzjzO7ceWOYjrPvMDdE"


class WeChatPub:
    s = requests.session()

    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"
        rep = self.s.get(url)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)['access_token']

    def send_msg(self, content, title):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "Allen",  # 接收人
            "toparty": "1",  # 接收部门
            "totag": " TagID1 | TagID2 ",  # 通讯录标签id
            "msgtype": "textcard",
            "agentid": 1000002,  # 应用ID
            "textcard": {
                "title": title,
                "description": content,
                "url": "http://i.jandan.net/top",
                "btntxt": "更多"
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)

    def send_text_msg(self, content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "Allen",  # 接收人
            "toparty": "1",  # 接收部门
            "totag": " TagID1 | TagID2 ",  # 通讯录标签id
            "msgtype": "text",
            "agentid": 1000002,  # 应用ID
            "text": {
                "content":content
            }
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)

    def send_hint(self, content):
        send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.send_msg(
            f"<div class=\"gray\">{send_time}</div> <div class=\"normal\">注意！</div><div class=\"highlight\">" + content + "！</div>", content)

    def send_image(self, imgPath):
        if exists(imgPath):
            with open(imgPath, 'rb') as f:
                base64_data = base64.b64encode(f.read())
                image_data = str(base64_data,'utf-8')
                md = hashlib.md5()
                md.update(f.read())
                image_md5 = md.hexdigest()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        headers = {"Content-Type": 'application/json'}
        data = {
            'msgtype': 'image',
            'image': {
                'base64': image_data,
                'md5': image_md5
            }
        }
        # 发送请求
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            print("发送图片成功")


if __name__ == "__main__":
    wechat = WeChatPub()
    # timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # msg_content = "今日已执行签退"
    # wechat.send_msg(
    #     f"<div class=\"gray\">{timenow}</div> <div class=\"normal\">注意！</div><div class=\"highlight\">" + msg_content + "！</div>")
    # print('消息已发送！')
    # wechat.send_image("./img/fly.jpg")
    wechat.send_text_msg("有一种爱，会在不经意间刻骨；有一种相遇，会在天意安排下完成；有一个人，会让另一个人与幸福相随。感恩那种刻骨的爱情，它让人懂得了爱情的宝贵，同时也清楚了爱情的甜蜜。")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
