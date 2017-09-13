import pygame

class Ship:
    '''飞船类，实现了飞船的大部分行为'''
    def __init__(self, ai_settings, screen):
        '''初始化飞船并设置其起始位置'''
        self.ai_settings = ai_settings
        self.screen = screen
        #加载飞船图片，获取其包围矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #屏幕的包围矩形
        self.screen_rect = screen.get_rect()

        #把飞船放置在屏幕底部的中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #向左/向右移动中吗？
        self.moving_right = False
        self.moving_left = False

    def paint(self):
        '''绘制飞船'''

        #在self.rect指定的位置绘制self.image
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''更新飞船的位置'''
        if self.moving_right == True and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.ai_settings.ship_speed_factor
        elif self.moving_left == True and self.rect.left > 0:
            self.rect.centerx -= self.ai_settings.ship_speed_factor