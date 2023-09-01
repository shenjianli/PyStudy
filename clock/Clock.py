#!/usr/bin/python3
# -*- coding:utf-8 -*-

import turtle as t
import datetime as d

class Clock:
    def __init__(self):
        self.tag = "Clock"
        t.title("申氏钟表")
        t.screensize(bg="#006400")
        # t.bgpic('./clock.gif')

    # 抬表针跳到一个地方
    def skip(self,step):
        t.penup()
        t.forward(step)
        t.pendown()
    def draw_clock(self, radius):
        t.speed(0)
        t.mode("logo")
        t.hideturtle()
        t.pensize(7)
        t.home() #回到圆点
        for j in range(60):
            self.skip(radius)
            if j % 5 == 0:
                t.forward(20)
                self.skip(-radius - 20)
            else:
                t.dot(5)
                self.skip(-radius)
            t.right(6)

    def make_point(self,point_name, len):
        t.penup()
        t.home()
        t.begin_poly()
        t.back(0.1 * len)
        t.forward(len * 1.1)
        t.end_poly()
        poly = t.get_poly()
        t.register_shape(point_name, poly)

    def draw_point(self):
        global hour_point, min_point, sec_point,font_writer
        self.make_point("hour_point", 100)
        self.make_point("min_point", 120)
        self.make_point("sec_point", 140)

        hour_point = t.Pen()
        hour_point.shape("hour_point")
        hour_point.shapesize(1, 1, 6)

        min_point = t.Pen()
        min_point.shape("min_point")
        min_point.shapesize(1, 1, 4)

        sec_point = t.Pen()
        sec_point.shape("sec_point")
        sec_point.pencolor('red')

        font_writer = t.Pen()
        font_writer.pencolor('gray')
        font_writer.hideturtle()

    def get_week(self,weekday):
        week_name = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
        return week_name[weekday]

    def get_date(self, year, month, day):
        return "%s-%s-%s" %(year, month, day)

    def get_real_time(self):
        curr = d.datetime.now()
        curr_year = curr.year
        curr_month = curr.month
        curr_day = curr.day
        curr_hour = curr.hour
        curr_minute = curr.minute
        curr_second = curr.second
        curr_weekday = curr.weekday()

        t.tracer(False)
        sec_point.setheading(360/60 * curr_second)
        min_point.setheading(360/60 * curr_minute)
        hour_point.setheading(360/12 * curr_hour + 30/60 * curr_minute)

        font_writer.clear()
        font_writer.home()
        font_writer.penup()
        font_writer.forward(80)
        # 用turtle写文字
        font_writer.write(self.get_week(curr_weekday), align="center", font=("Courier", 14, "bold"))
        font_writer.forward(-160)
        font_writer.write(self.get_date(curr_year, curr_month, curr_day), align="center", font=("Courier", 14, "bold"))
        t.tracer(True)
        print(curr_second)
        t.ontimer(self.get_real_time, 1000)  # 每隔1000毫秒调用一次realTime()
    def start(self):
        print(self.tag, "start")
        t.tracer(False)
        self.draw_clock(160)
        self.draw_point()
        self.get_real_time()
        t.tracer(True)
        t.mainloop()


if __name__ == '__main__':
    time_clock = Clock()
    time_clock.start()