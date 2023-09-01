#!/usr/bin/python3
# -*- coding:utf-8 -*-
from loguru import logger
from PIL import Image


class Image2Chat:
    def __init__(self):
        self.tag = "Image2Chat"
        logger.add("file_image_char.log")
        self.width = 120
        self.height = 90
        self.out = "output.txt"
        self.asscii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.")

    def get_char(self,r,g,b,alpha = 256):
        if alpha == 0:
            return ' '
        length = len(self.asscii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (255.0 + 1)/length
        return self.asscii_char[int(gray/unit)]

    def start(self, img_name):
        logger.info("start")
        im = Image.open(img_name)
        im = im.resize((self.width, self.height), Image.NEAREST)
        txt = ""
        for i in range(self.height):
            for j in range(self.width):
                txt += self.get_char(*im.getpixel((j,i)))
            txt += '\n'
        logger.info(txt)
        file_name = img_name[:img_name.find(".")]
        with open(file_name + "_" + self.out, "w") as f:
            f.write(txt)
        logger.info("over")


if __name__ == '__main__':
    image2char = Image2Chat()
    img_name = "girl.jpg"
    # img_name = "rabit.jpeg"
    image2char.start(img_name)
