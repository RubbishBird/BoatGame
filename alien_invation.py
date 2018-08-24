#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/17 10:07
# @Author  : feng
# @Site    : 
# @File    : alien_invation.py
# @Software: PyCharm

import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    '''初始化游戏，并创建一个屏幕对象'''
    pygame.init()        #初始化背景设置
    ai_settings = Settings()        #创建Settings实例
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))        #创建一个名为screen的显示窗口，实参（1200,800）是一个元组，指定了游戏窗口的尺寸
    pygame.display.set_caption("Alien Invasion")

    #创建play按钮
    play_button = Button( screen, 'Play')

    #创建一个用于统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #创建一个存储外星人的编组
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #开始游戏的主循环
    while True:

        gf.check_events(ai_settings, screen,stats, ship, bullets, play_button,aliens, sb)
        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb)

run_game()