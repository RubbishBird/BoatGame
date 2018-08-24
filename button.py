#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 13:29
# @Author  : feng
# @Site    : 
# @File    : button.py
# @Software: PyCharm

import pygame.font          #导入模块pygame.font，让pygame能够将文本渲染到屏幕上

class Button():
    def __init__(self, screen, msg):
        '''初始化按钮的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width, self.height = 200,50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)   #指定使用什么字体来渲染文本，None表示默认字体，48指定字体的大小

        #创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0 ,self.width, self.height)
        self.rect.center = self.screen_rect.center

        #按钮的创建只需要一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''将msg渲染为图像，并使其在按钮上居中'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)   #调用font.render()将存储在msg中的文本转化为图像，True指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑）
        self.msg_image_rect = self.msg_image.get_rect()  #根据文本图像创建一个rect,并将其center属性设置为按钮的center属性
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color,self.rect)    #调用screen.fill()来绘制表示按钮的矩形
        self.screen.blit(self.msg_image, self.msg_image_rect)     #调用screen.blit()，并向它传递一幅图像以及与该图像相关联的rect对象