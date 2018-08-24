#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/17 14:51
# @Author  : feng
# @Site    : 
# @File    : game_functions.py
# @Software: PyCharm


import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event,ai_settings, screen, ship, bullets):
    #相应按键
    if event.key == pygame.K_RIGHT:           #确认按下的是不是键盘右箭头
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:         #确认按下的是不是键盘左箭头
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, ship, bullets, play_button, aliens, sb):
    '''相应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen , stats, ship, play_button, mouse_x, mouse_y, aliens, bullets, sb)

def check_play_button(ai_settings, screen , stats, ship, play_button, mouse_x, mouse_y, aliens, bullets, sb):
    '''在玩家点击play按钮时开始游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()     #重置游戏设置
        pygame.mouse.set_visible(False)     #隐藏光标
        stats.reset_stats()   #重置游戏统治信息
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        #sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb):
    '''更新屏幕上的图像，并切换到新屏幕'''
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)       #使用ai_settings来访问背景色
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()          #调用ship.blitme()将飞船绘制到屏幕上，确保它出现在背景前面
    aliens.draw(screen)
    sb.show_score()         #显示得分
    #如果游戏处于非活动状态，就绘制button按钮
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()  # 让最近绘制的屏幕可见

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    #更新子弹的位置
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
    # 检查是否有子弹击中外星人，如果有，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #如果整群外星人被消灭，就提升一个等级
        #删除现有的子弹，并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    #如果还没有达到限制，就发射一颗子弹
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    #计算每行可容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #创建一个外星人，并将其放在当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    #创建外星人群
    #创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    '''有外星人到达边缘时，采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''将整群外星人下移，并改变他们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''相应外星人被撞到的飞船'''
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #显示还剩下多少飞船
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停0.5秒
        sleep(2)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)   #显示鼠标


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''检查是否有外星人到达了屏幕的底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''检查是否有外星人位于屏幕边缘，并更新整群外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    # 检查是否有外星人到达了屏幕的底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def check_high_score(stats, sb):
    #检查是否诞生新的最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()