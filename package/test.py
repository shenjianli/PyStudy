#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import sys

cocos_path = "OxfordBooks/frameworks/runtime-src/proj.android-studio/app"
path = os.getcwd()[:os.getcwd().rfind(os.path.sep)] + os.path.sep + cocos_path
print(path)