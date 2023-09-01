#!/usr/bin/python3
# -*- coding:utf-8 -*-

import tkinter
import math
import time

class Clock:
    def __init__(self):
        self.tag = "Clock"
        self.x = 150
        self.y = 150
        self.length = 40
        self.root = tkinter.Tk()

    def creating_all_function_trigger(self):
        self.create_canvas_for_shapes()
        self.creating_background()
        self.creating_sticks()
    def start(self):
        print(self.tag, "start")
        self.creating_all_function_trigger()

    def creating_background(self):
        self.image = tkinter.PhotoImage(file='clock_bg.jpeg')
        self.canvas.create_image(151, 124, image=self.image)
        pass

    def create_canvas_for_shapes(self):
        self.canvas = tkinter.Canvas(self, bg='black')  # 创建画布对象，并将其添加到主视窗中
        self.canvas.pack(expand='yes', fill='both')  # 将画布填充整个窗口
        pass

    def creating_sticks(self):
        pass


if __name__ == '__main__':
    time_clock = Clock()
    time_clock.start()