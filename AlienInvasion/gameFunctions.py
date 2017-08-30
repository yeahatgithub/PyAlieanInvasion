import pygame
import sys

def chick_events():
    '''处理键盘鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def updateScreen(settings, screen, ship):
    # 设定屏幕背景色
    screen.fill(settings.bg_color)
    # 绘制飞船
    ship.paint()
    # 让最近绘制的屏幕可见
    pygame.display.flip()