# -*- coding: utf-8 -*-
import screen
from screen import Point
import devices
import utime
import random
import _thread

import Turtle.init_turtle as init_turtle
import Turtle.waffle_turtle as turtle
import Turtle.globalvar as gl

under_x = [65,75,85,95,105,115]
under_y = [30,40,50,60,70,80,90,100,110,120,130,140,150]
underwater = [65,90]

def show_temperature():
    tem = devices.temperature()
    p_tem_t = screen.Point(10,90)
    if tem >= 42.0 and tem < 48.0:
        screen.print(p_tem_t, str(tem), clr = 0xa800, bg = 0x0000, direction = screen.ROTATE_90)
    elif tem >= 36.0 and tem < 42.0:
        screen.print(p_tem_t, str(tem), clr = 0xf800, bg = 0x0000, direction = screen.ROTATE_90)
    elif tem >= 30.0 and tem < 36.0:
        screen.print(p_tem_t, str(tem), clr = 0xfce0, bg = 0x0000, direction = screen.ROTATE_90)
    elif tem >= 24.0 and tem < 30.0:
        screen.print(p_tem_t, str(tem), clr = 0xffe0, bg = 0x0000, direction = screen.ROTATE_90)
    elif tem >= 18.0 and tem < 24.0:
        screen.print(p_tem_t, str(tem), clr = 0x07ff, bg = 0x0000, direction = screen.ROTATE_90)
    elif tem >= 12.0 and tem < 18.0:
        screen.print(p_tem_t, str(tem), clr = 0x02ff, bg = 0x0000, direction = screen.ROTATE_90)
    elif tem >= 6.0 and tem < 12.0:
        screen.print(p_tem_t, str(tem), clr = 0x001f, bg = 0x0000, direction = screen.ROTATE_90)
    elif tem >= 0.0 and tem < 6.0:
        screen.print(p_tem_t, str(tem), clr = 0x0010, bg = 0x0000, direction = screen.ROTATE_90)
    else:
        screen.print(p_tem_t, str(tem), clr = 0x0000, bg = 0x0000, direction = screen.ROTATE_90)

def show_humidity():
    hum = devices.humidity()
    p_hum_t = screen.Point(25,105)
    screen.print(p_hum_t, str(round(hum,2)) + '%', clr = 0xffff,bg = 0x0000, direction = screen.ROTATE_90)

def sonar():
    #深海雷达
    p12 = screen.Point(64,80)
    screen.circle(p12,10,0xffff)
    screen.circle(p12,20,0xffff)
    screen.circle(p12,30,0xffff)
    screen.circle(p12,10,0x0000)
    screen.circle(p12,40,0xffff)
    screen.circle(p12,20,0x0000)
    screen.circle(p12,50,0xffff)
    screen.circle(p12,30,0x0000)
    screen.circle(p12,60,0xffff)
    submarine()
    screen.circle(p12,40,0x0000)
    screen.circle(p12,70,0xffff)
    screen.circle(p12,50,0x0000)
    screen.circle(p12,80,0xffff)
    screen.circle(p12,60,0x0000)
    screen.circle(p12,90,0xffff)
    screen.circle(p12,70,0x0000)
    screen.circle(p12,80,0x0000)
    screen.circle(p12,90,0x0000)
    deletesubmarine()

def submarine():
    #潜艇
    x = random.choice(under_x)
    y = random.choice(under_y)
    p1 = screen.Point(x,y)
    p2 = screen.Point(x-10,y-20)
    p3 = screen.Point(x-3,y-10)
    p4 = screen.Point(x-7,y-15)
    p5 = screen.Point(x-10,y-15)
    p6 = screen.Point(x-5,y)
    p7 = screen.Point(x,y+2)
    p8 = screen.Point(x-10,y+2)
    p9 = screen.Point(x-5,y+6)
    p10 = screen.Point(x-9,y+12)
    p11 = screen.Point(x-17,y+19)
    screen.round_rect(p2, p1, 7, 0x07ff)
    screen.rect(p4, p3, 0x07ff)
    screen.triangle(p5, 5, 6, 230, 0x07ff)
    # screen.round_rect(p6, p7, 2, 0x07ff)
    # screen.round_rect(p6, p8, 2, 0x07ff)
    screen.fill_rect(p6, p7, 0x07ff)
    screen.fill_rect(p6, p8, 0x07ff)
    screen.circle(p9,2,0x07ff)
    screen.circle(p10,3,0x07ff)
    screen.circle(p11,4,0x07ff)
    underwater[0] = x
    underwater[1] = y

def deletesubmarine():
    x_d = underwater[0]
    y_d = underwater[1]
    p1 = screen.Point(x_d,y_d)
    p2 = screen.Point(x_d-10,y_d-20)
    p3 = screen.Point(x_d-3,y_d-10)
    p4 = screen.Point(x_d-7,y_d-15)
    p5 = screen.Point(x_d-10,y_d-15)
    p6 = screen.Point(x_d-5,y_d)
    p7 = screen.Point(x_d,y_d+2)
    p8 = screen.Point(x_d-10,y_d+2)
    p9 = screen.Point(x_d-5,y_d+6)
    p10 = screen.Point(x_d-9,y_d+12)
    p11 = screen.Point(x_d-17,y_d+19)
    screen.round_rect(p2, p1, 7, 0x0000)
    screen.rect(p4, p3, 0x0000)
    screen.triangle(p5, 5, 6, 230, 0x0000)
    # screen.round_rect(p6, p7, 2, 0x07ff)
    # screen.round_rect(p6, p8, 2, 0x07ff)
    screen.fill_rect(p6, p7, 0x0000)
    screen.fill_rect(p6, p8, 0x0000)
    screen.circle(p9,2,0x0000)
    screen.circle(p10,3,0x0000)
    screen.circle(p11,4,0x0000)

def uptitle():
    screen.on()
    screen.fill(0x0000)
    #温度+湿度
    p_tem = screen.Point(10,153)
    p_hum = screen.Point(25,153)
    screen.print(p_tem, 'temperature:',clr = 0xffff, bg = 0x0000, direction = screen.ROTATE_90)
    screen.print(p_hum,'humidity:',clr = 0xffff, bg = 0x0000, direction = screen.ROTATE_90)

def retitle():
    p_tem = screen.Point(10,153)
    p_hum = screen.Point(25,153)
    screen.print(p_tem, 'temperature:',clr = 0xffff, bg = 0x0000, direction = screen.ROTATE_90)
    screen.print(p_hum,'humidity:',clr = 0xffff, bg = 0x0000, direction = screen.ROTATE_90)

def show():
    show_temperature()
    show_humidity()

def underweather_start():
    count = 0
    uptitle()
    sonar()
    retitle()
    show()
    # submarine()
    while True:
        count += 1
        show()
        # show_temperature()
        # show_humidity()
        # _thread.start_new_thread(show_temperature,())
        # _thread.start_new_thread(show_humidity,())
        # if count % 15 == 0:
        #     sonar()
        #     deletesubmarine()
        #     submarine()
        #     retitle()
        # _thread.start_new_thread(show,())
        if count % 30 == 0:
            # sonar()
            _thread.start_new_thread(sonar,())
            # _thread.start_new_thread(deletesubmarine,())
            # _thread.start_new_thread(submarine,())
            retitle()

