import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb):
    '''处理键盘鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  #一直按下右箭头键，不会持续发送KEYDOWN类型的事件
            #print("check_event(), handle KEYDOWN")
            on_key_down(event, ship, bullets)
        elif event.type == pygame.KEYUP:  #是KEYUP, 不是K_UP
            on_key_up(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens,bullets, sb, mouse_x, mouse_y)


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


def updateScreen(settings, screen, stats, sb, ship, bullets, aliens, button):
    # 设定屏幕背景色
    screen.fill(settings.bg_color)
    # 绘制飞船
    ship.paint()
    #绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #绘制外星人
    aliens.draw(screen)
    if not stats.game_active:
        #开始按钮
        button.draw_button()
    #计分
    sb.show_score()

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


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_alien_bullet_collision(ai_settings, aliens, bullets, screen, ship, stats, sb)


def check_alien_bullet_collision(ai_settings, aliens, bullets, screen, ship, stats, sb):
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def update_aliens(ai_settings, game_stats, screen, ship, aliens, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    for alien in aliens.sprites():
        alien.update()   #这里修改外星人的位置，但没有显示
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        #下面的语句会修改外星人位置，使得上面的修改外星人位置失效——看不到碰撞的发生。
        ship_hit(ai_settings, game_stats, screen, ship, aliens, bullets, sb)
    #检查外星人到达屏幕底部
    check_aliens_bottom(ai_settings, game_stats, screen, ship, aliens, bullets, sb)

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


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """响应被外星人撞到的飞船"""
    print("ship left: ", stats.ships_left)
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,bullets,sb, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #重新计分
        sb.prep_ships()
        sb.prep_score()