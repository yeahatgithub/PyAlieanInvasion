import pygame
from pygame.sprite import Group
from gameStats import  GameStats

import gameFunctions as gf
from gameFunctions import update_bullets
from settings import Settings
from ship import Ship


def run_game():
    #初始化pygame
    pygame.init()
    ai_settings = Settings()

    #创建屏幕对象
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height) )
    #pygame.display.set_caption(Settings.caption)  #错误写法，不能用“类名.属性”
    pygame.display.set_caption(ai_settings.caption)
    #创建子弹编组
    bullets = Group()
    #外星人编队
    aliens = Group()

    #屏幕背景色
    bg_color = ai_settings.bg_color
    #创建飞船对象，加载飞船图片
    ship = Ship(ai_settings, screen)
    #创建外星编队
    gf.create_fleet(ai_settings, screen, ship, aliens)

    game_stats = GameStats(ai_settings)

    #游戏主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ship, bullets)
        #更新飞船的位置
        ship.update()
        #更新子弹位置
        gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
        #更新外星人位置
        gf.update_aliens(ai_settings, game_stats, screen, ship, aliens, bullets)

        #绘制游戏画面
        gf.updateScreen(ai_settings, screen, ship, bullets, aliens)


run_game()