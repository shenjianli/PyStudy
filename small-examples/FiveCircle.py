import turtle as p


def draw_circle(x,y,c = 'red'):
    p.pu() # 抬起画笔
    p.goto(x,y) # 绘制圆的起始位置
    p.pd()# 放下画笔
    p.color(c)
    p.circle(30,360)


def set_draw():
    p.pensize(3) # 设置画笔尺寸

def start():
    set_draw()
    draw_circle(0,0, 'blue')
    draw_circle(60,0, 'black')
    draw_circle(120,0, 'red')
    draw_circle(90,-30, 'green')
    draw_circle(30, -30, 'yellow')

    p.done()

if __name__ == '__main__':
    start()