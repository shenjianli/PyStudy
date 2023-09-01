#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time
import pywhatkit
from loguru import logger

class HandWrite:
    def __init__(self):
        logger.add("log.txt")
        self.tag = "HandWrite"
        self.is_dev = True

    def log(self, log):
        if self.is_dev:
            print(self.tag, log)

    def start(self, text):
        self.log("start")
        if len(text) > 0:
            pywhatkit.text_to_handwriting(text)
            logger.info(text)
        self.log("end")

if __name__ == '__main__':
    hand_write = HandWrite()
    hand_write.start("Learning Python from the basics is extremely important.")