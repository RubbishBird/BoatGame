#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/17 11:30
# @Author  : feng
# @Site    : 
# @File    : ship.py
# @Software: PyCharm

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        '''初始化飞船，并设置其初始位置'''
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings           #将ai_setteings的值存储在一个属性中，以便能够在update()中调用它

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()         #加载图像后，使用get_rect()获取surface的属性rect
        self.screen_rect = screen.get_rect()      #将表示屏幕的矩形存储在self.screen_rect中

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性center中存储属性的最小值
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''根据移动标志调整飞船的位置'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > self.screen_rect.left:    #等价于if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        #让飞船在屏幕中央居中
        self.center = self.screen_rect.centerx