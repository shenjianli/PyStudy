#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 导入所需库
from tkinter import *
import datetime
import math

# 创建窗口对象
root = Tk()

# 创建画布对象
canvas = Canvas(root, width=400, height=400)

# 将画布添加到窗口中
canvas.pack()


def update_clock():
    now = datetime.datetime.now()
    hour = now.hour % 12
    minute = now.minute
    second = now.second

    hour_x = 200 + 50 * math.sin((hour * 30 + minute / 2) * math.pi / 180)
    hour_y = 200 - 50 * math.cos((hour * 30 + minute / 2) * math.pi / 180)
    minute_x = 200 + 75 * math.sin(minute * 6 * math.pi / 180)
    minute_y = 200 - 75 * math.cos(minute * 6 * math.pi / 180)
    second_x = 200 + 100 * math.sin(second * 6 * math.pi / 180)
    second_y = 200 - 100 * math.cos(second * 6 * math.pi / 180)

    canvas.delete('all')
    canvas.create_oval(50, 50, 350, 350, width=2)
    for i in range(1, 13):
        x1 = 200 + 125 * math.sin((i - 1) * 30 * math.pi / 180)
        y1 = 200 - 125 * math.cos((i - 1) * 30 * math.pi / 180)
        x2 = 200 + 100 * math.sin((i - 1) * 30 * math.pi / 180)
        y2 = 200 - 100 * math.cos((i - 1) * 30 * math.pi / 180)
        canvas.create_line(x1, y1, x2, y2, width=2)
        canvas.create_text(x1, y1, text=str(i), font=('Arial', 16, 'bold'))

    canvas.create_line(200, 200, hour_x, hour_y, width=5, fill='blue')
    canvas.create_line(200, 200, minute_x, minute_y, width=3, fill='green')
    canvas.create_line(200, 200, second_x, second_y, width=1, fill='red')

    root.after(1000, update_clock)


update_clock()

# 主循环
root.mainloop()