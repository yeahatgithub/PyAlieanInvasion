import pygame

class Ship:
    '''飞船类，实现了飞船的大部分行为'''
    def __init__(self, screen):
        '''初始化飞船并设置其起始位置'''

        self.screen = screen
        #加载飞船图片，获取其包围矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #屏幕的包围矩形
        self.screen_rect = screen.get_rect()

        #把飞船放置在屏幕底部的中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def paint(self):
        '''绘制飞船'''

        #在self.rect指定的位置绘制self.image
        self.screen.blit(self.image, self.rect)