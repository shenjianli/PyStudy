#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys
import platform
import requests


def get_name_version(module_str):
    module_str = module_str.replace("'", "").strip("\n")
    name = ""
    version = ""
    if len(module_str) > 0 and (":" in module_str):
        info_list = module_str.split(":")
        name = info_list[1]
        version = info_list[2]
    return name, version


class UpdateSdk(object):
    def __init__(self):
        self.tag = "update_sdk"
        self.is_dev = False
        # 如查在项目中 True 在demo中设为 False
        self.is_in_project = False
        self.url = "https://gitlab.dev.ihuman.com/mobile-public/iHumanSDK-android/-/raw/dev_publish/CHANGELOG.md"
        self.dependencies_file_name = "dependencies.gradle"
        self.project_root_path = os.getcwd()
        self.oxford_sdk = {
            "ihuman-core": "iHumanCoreVersion",
            "account-sim": "ihumanSimVersion",
            "aes256": "ihumanAes256Version",
            "cos": "iHumanCosVersion",
            "push": "iHumanPushVersion",
            "speecheval": "iHumanSpeechEvalVersion",
            "wx": "ihumanWeixinVersion",
            "qq": "ihumanQQVersion",
            "alipay": "ihumanAliVersion",
            "privacy": "iHumanPrivacyVersion",
            "environment": "iHumanEnvironmentVersion",
            "download": "iHumanDownloadVersion",
            "update": "ihumanUpdateVersion",
            "account-ui": "iHumanAccountUiVersion",
            "launch": "iHumanLaunchVersion",
            "channel-huawei": "ihumanChannelHuaweiVersion",
            "channel-xiaomi": "ihumanChannelXiaomiVersion",
            "channel-oppo": "ihumanChannelOppoVersion",
            "channel-vivo": "ihumanChannelVivoVersion",
            "channel-meizu": "ihumanChannelMeizuVersion",
            "mall": "ihumanMallVersion",
            "benefit": "ihumanBenefitVersion",
            "broadcast": "ihumanBroadcastVersion",
            "recommend": "ihumanRecommendVersion",
            "detect":"ihumanDetectVersion",
            "facebook":"ihumanFacebookVersion",
            "google":"ihumanGoogleVersion",
            "attribution":"ihumanAttributionVersion"
        }

    def log(self, log):
        print(self.tag, log)

    def start(self):
        if self.is_dev:
            self.log("start")
        res = requests.get(self.url)
        content = str(res.text)
        if self.is_dev:
            self.log(content)
        version_start = content.find("###")
        if self.is_dev:
            self.log(version_start)
        version_end = content.find("###", version_start + 3)
        if self.is_dev:
            self.log(version_end)
        new_version_p_str = content[version_start:version_end]
        if self.is_dev:
            self.log(new_version_p_str)

        start = new_version_p_str.find("###")
        end = new_version_p_str.find("\n")
        version_no = new_version_p_str[start + 3:end]
        self.log(f'最新版本:{version_no}')
        start = new_version_p_str.find("Feature")
        end = new_version_p_str.find(">")
        version_info = new_version_p_str[start:end]
        self.log(f'版本更新内容:{version_info}')

        start = new_version_p_str.find("groovy")
        start = new_version_p_str.find("groovy", start + 6)
        end = new_version_p_str.find("```", start)
        all_module_info = new_version_p_str[start + 6: end].strip("\n")
        if self.is_dev:
            self.log(f'sdk所有模块：{all_module_info}')
        module_info_list = all_module_info.split('\n')
        if self.is_dev:
            self.log(len(module_info_list))

        module_version_info = {}
        for module in module_info_list:
            name, version = get_name_version(module)
            oxford_module = self.oxford_sdk.get(name)
            if oxford_module is not None:
                module_version_info[name] = version
        if self.is_dev:
            self.log(module_version_info)
        is_update = self.write_dependencies_file(module_version_info)
        if is_update and self.is_in_project:
            self.commit_files()
        self.check_delete_module(module_version_info)

    def check_delete_module(self, module_version_info):
        for sdk_module, project_module in self.oxford_sdk.items():
            if sdk_module not in module_version_info.keys():
                self.log(f'sdk删除了库 {project_module}, 需要手动删除')

    def commit_files(self):
        dep_file_path = self.project_root_path + os.path.sep + self.dependencies_file_name
        os.system(f'git add {dep_file_path}')
        os.system(f'git commit -m \'sdk 更新提交\'')
        os.system(f'git push')
        self.log("sdk更新提交代码执行完成")

    def is_update_version(self, module_version_info, data):
        keys = module_version_info.keys()
        is_update = False
        oxford_module_name = ""
        oxford_module_version = ""
        for key in keys:
            oxford_module_name = self.oxford_sdk[key]
            if f'{oxford_module_name} =' in data:
                oxford_module_version = module_version_info[key]
                if not (oxford_module_version in data):
                    return True, oxford_module_name, oxford_module_version
        return is_update, oxford_module_name, oxford_module_version

    def write_dependencies_file(self, module_version_info):
        file_content = ""
        is_write = False
        file_path = self.project_root_path + os.path.sep + self.dependencies_file_name
        with open(file_path, 'r', encoding="utf-8") as f:
            for data in f:
                is_update, module_name, version = self.is_update_version(module_version_info, data)
                version = f'\"{version}\"\n'
                if is_update:
                    index = data.find('=')
                    old_version = data[index + 2:]
                    data = data.replace(old_version, version)
                    self.log(f'本次更新了{module_name}:{version}'.strip("\n"))
                    is_write = True
                file_content += data
        if is_write:
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(file_content)
                self.log("更新成功")
        else:
            self.log("已经是最新了")
        return is_write


if __name__ == '__main__':
    update = UpdateSdk()
    update.start()