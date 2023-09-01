#!/usr/bin/python3
# -*- coding:utf-8 -*-
from loguru import logger
logger.debug("That's it, beautiful and simple logging!")

# 日志输出到文件
logger.add("file_{time}.log")
logger.debug("That's it, beautiful and simple logging!")

logger.add("file_2.log", rotation="12:00") # 每天12:00会创建一个新的文件
logger.debug("That's it, beautiful and simple logging!")

logger.add("file_1.log", rotation="1 MB") # 滚动大日志文件,一旦日志文件大小超过 1 MB 就会产生新的日志文件。
logger.debug("That's it, beautiful and simple logging!")
logger.add("file_3.log", compression="zip") # 压缩日志
logger.debug("That's it, beautiful and simple logging!")

logger.add("out.log", backtrace=True, diagnose=True) #支持Backtrace

def func(a, b):
    return a / b

def nested(c):
    try:
        func(5, c)
    except ZeroDivisionError:
        logger.exception("What?!")

nested(0)


