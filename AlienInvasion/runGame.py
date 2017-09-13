import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import gameFunctions as gf
from alien import Alien

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

    #游戏主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ship, bullets)
        #更新飞船的位置
        ship.update()
        update_bullets(bullets)

        #绘制游戏画面
        gf.updateScreen(ai_settings, screen, ship, bullets, aliens)


def update_bullets(bullets):
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))


run_game()