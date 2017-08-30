import sys
import pygame
from settings import Settings
from ship import Ship

def run_game():
    #初始化pygame
    pygame.init()
    aiSettings = Settings()

    #创建屏幕对象
    screen = pygame.display.set_mode((aiSettings.screen_width, aiSettings.screen_height) )
    #pygame.display.set_caption(Settings.caption)  #错误写法，不能用“类名.属性”
    pygame.display.set_caption(aiSettings.caption)

    #屏幕背景色
    bg_color = aiSettings.bg_color
    #创建飞船对象，加载飞船图片
    ship = Ship(screen)

    #游戏主循环
    while True:
        #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        #设定屏幕背景色
        screen.fill(bg_color)
        #绘制飞船
        ship.paint()

        #让最近绘制的屏幕可见
        pygame.display.flip()

run_game()