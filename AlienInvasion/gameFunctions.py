import pygame
import sys
from bullet import Bullet
from alien import Alien

def check_events(ship, bullets):
    '''处理键盘鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  #一直按下右箭头键，不会持续发送KEYDOWN类型的事件
            #print("check_event(), handle KEYDOWN")
            on_key_down(event, ship, bullets)
        elif event.type == pygame.KEYUP:  #是KEYUP, 不是K_UP
            on_key_up(event, ship)


def on_key_up(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def on_key_down(event, ship, bullets):
    if event.key == pygame.K_RIGHT:  # 是event.key, 不是event.type
        ship.moving_right = True
        # print("check_event(), handle K_RIGHT")
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ship)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(bullets, ship):
    # 生成一颗子弹
    if len(bullets) < ship.ai_settings.bullets_allowed:
        bullet = Bullet(ship.ai_settings, ship.screen, ship)
        bullets.add(bullet)


def updateScreen(settings, screen, ship, bullets, aliens):
    # 设定屏幕背景色
    screen.fill(settings.bg_color)
    # 绘制飞船
    ship.paint()
    #绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #绘制外星人
    aliens.draw(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人编队'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = how_many_aliens_per_line(ai_settings, alien.rect.width)
    number_aliens_y = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人编队
    for row_cnt in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, alien_number, row_cnt, aliens, screen)


def create_alien(ai_settings, alien_number, row_cnt, aliens, screen):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien.rect.height + 2 * alien.rect.height * row_cnt
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def how_many_aliens_per_line(ai_settings, alien_width):
    # 计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -  (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_alien_bullet_collision(ai_settings, aliens, bullets, screen, ship)


def check_alien_bullet_collision(ai_settings, aliens, bullets, screen, ship):
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def update_aliens(ai_settings, aliens):
    check_fleet_edges(ai_settings, aliens)
    for alien in aliens.sprites():
        alien.update()


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

