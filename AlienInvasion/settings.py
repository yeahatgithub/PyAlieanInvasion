class Settings:
    '''存储游戏程序用到的常量'''
    def __init__(self):
        #屏幕宽、高
        self.screen_width = 1200
        self.screen_height = 800
        #屏幕背景色
        self.bg_color = (230, 230, 230)
        self.caption = "外星人入侵"

        self.ship_speed_factor = 1.5

        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10

        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1