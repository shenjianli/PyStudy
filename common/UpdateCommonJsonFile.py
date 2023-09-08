#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os.path
import sys
import json
import requests

requests.packages.urllib3.disable_warnings()

class UpdateCommonJsonFile:
    def __init__(self):
        self.tag = "update common json file"
        self.is_dev = True
        self.is_in_project = False
        self.project_root_path = os.getcwd()
        self.staging_url = "https://staging-api.ihumand.com/oxford/client/get_common_res?"
        self.product_url = "https://oxfordapi.ihuman.com/oxford/client/get_common_res?"
        self.sign_file_name = "script/oxford_sign.txt"
        self.param_str = ""

    def log(self, msg):
        print(self.tag, msg)

    def start_sign(self, version):
        jar_path = "oxford_sign.jar"
        if self.is_in_project:
            jar_path = self.project_root_path + os.path.sep + "script" + os.path.sep + jar_path
        sign_cmd = f"java -jar {jar_path} -v {version}"
        os.system(sign_cmd)
        if self.is_dev:
            self.log("完成签名")

    def get_param_sign(self):
        if os.path.exists(self.sign_file_name):
            with open(self.sign_file_name, "r") as f:
                file_content = f.read()
                f.close()
                if len(file_content) > 10:
                    self.log(f"读取参数文件{file_content}")
                    return file_content
        return ""

    def get_version(self):
        file_name = "build.gradle"
        if self.is_in_project:
            file_name = self.project_root_path + os.path.sep + "build.gradle"
        config_file = open(file_name, "r")
        content = config_file.readlines()
        config_file.close()
        for temp in content:
            if "versionName = " in temp:
                version_no = temp.replace("versionName = ", "").replace("\"", "").replace("\n", "").replace(" ", "")
                self.log(f"从配置文件读取版本号：{version_no}")
                return version_no
        return "1.8.0"

    def start(self, channel):
        if self.is_dev:
            self.log("start")
        if len(self.param_str) < 10:
            version = self.get_version()
            self.start_sign(version)
            self.param_str = self.get_param_sign()
        if len(self.param_str) < 10:
            return
        if "product" in channel:
            res = requests.get(self.product_url + self.param_str, verify=False)
        elif "staging" in channel:
            res = requests.get(self.staging_url + self.param_str, verify=False)
        if self.is_dev:
            self.log(res.url)
        if res.status_code == 200:
            content = str(res.text)
            if self.is_dev:
                self.log(content)
            if len(content) > 30:
                data = json.loads(content)
                code = data['code']
                if code == 0:
                    self.save_json_file(content, channel)
                else:
                    self.log(f'{channel} 请求失败 {data["message"]}')
        else:
            self.log(f"{channel} 网络请求失败{res.status_code}")

    def save_json_file(self, content, channel):
        file_pre = ""
        is_save = True
        if "product" in channel:
            file_pre = "product"
        elif "staging" in channel:
            file_pre = "staging"
        if not self.is_in_project:
            file_path = f"{file_pre}_common.json"
        else:
            file_path = self.project_root_path + os.path.sep + "app" + os.path.sep + "src" + \
                        os.path.sep + "main" + os.path.sep + "assets" + os.path.sep + f"{file_pre}_common.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                file_content = f.read()
                f.close()
                if file_content == content:
                    is_save = False
                    self.log(f"{channel} -> {file_path} 文件已经是最新了，无需更新")

        if is_save:
            with open(file_path, "w") as f:
                f.write(content)
                f.close()
                self.log(f"{channel} 更新 {file_path} 文件成功")
                self.commit_file(file_path)

    def commit_file(self, file_path):
        os.system(f'git add {file_path}')
        os.system(f'git commit -m \'更新get_common_res json 文件\'')
        os.system(f'git push')
        self.log("提交代码执行完成")


# 可正常运行 产生common_res json文件
if __name__ == '__main__':
    updateCommonInfo = UpdateCommonJsonFile()
    for i in range(0, len(sys.argv)):
        print(f"第{i}参数为：{sys.argv[i]}")
    if len(sys.argv) == 1:
        updateCommonInfo.start("product")
        updateCommonInfo.start("staging")
    elif len(sys.argv) == 2:
        arg2 = sys.argv[1]
        if "product" in arg2:
            updateCommonInfo.start("product")
        elif "staging" in arg2:
            updateCommonInfo.start("staging")
        elif "all" in arg2:
            updateCommonInfo.start("product")
            updateCommonInfo.start("staging")
        else:
            print("输入有误")
    else:
        print("输入有误")