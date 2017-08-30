import sys
import pygame
from settings import Settings
from ship import Ship
import gameFunctions as gf

def run_game():
    #初始化pygame
    pygame.init()
    ai_settings = Settings()

    #创建屏幕对象
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height) )
    #pygame.display.set_caption(Settings.caption)  #错误写法，不能用“类名.属性”
    pygame.display.set_caption(ai_settings.caption)

    #屏幕背景色
    bg_color = ai_settings.bg_color
    #创建飞船对象，加载飞船图片
    ship = Ship(screen)

    #游戏主循环
    while True:
        #监视键盘和鼠标事件
        gf.chick_events()
        #绘制游戏画面
        gf.updateScreen(ai_settings, screen, ship)


run_game()