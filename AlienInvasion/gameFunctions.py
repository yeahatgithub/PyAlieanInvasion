import pygame
import sys

def check_events(ship):
    '''处理键盘鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  #一直按下右箭头键，不会持续发送KEYDOWN类型的事件
            #print("check_event(), handle KEYDOWN")
            on_key_down(event, ship)
        elif event.type == pygame.KEYUP:  #是KEYUP, 不是K_UP
            on_key_up(event, ship)


def on_key_up(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def on_key_down(event, ship):
    if event.key == pygame.K_RIGHT:  # 是event.key, 不是event.type
        ship.moving_right = True
        # print("check_event(), handle K_RIGHT")
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True


def updateScreen(settings, screen, ship):
    # 设定屏幕背景色
    screen.fill(settings.bg_color)
    # 绘制飞船
    ship.paint()
    # 让最近绘制的屏幕可见
    pygame.display.flip()