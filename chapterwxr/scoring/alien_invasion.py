import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """整体类管理游戏行为."""

    def __init__(self):
        """初始化游戏，创建游戏资源."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # 创建一个实例来存储游戏统计数据
        # 创建一个记分板
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建play按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """启动主程序打开游戏窗口"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """当玩家点击游戏时，开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重设游戏设置
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计数据
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 除掉剩下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            
            # 建立一支新的舰队，并以飞船为中心
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """对关键的释放做出反应"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一个新的子弹，并将其添加到子弹组"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置，去掉旧子弹"""
        # 更新子弹位置
        self.bullets.update()

        # 处理掉那些消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """子弹与外星人碰撞后响应"""
        # 排除任何子弹和外星人的碰撞
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 销毁现有子弹，建立新的舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 增加等级
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        检查舰队是否处于边缘，然后更新舰队中所有外星人的位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 寻找外星人与飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 寻找在屏幕底部的外星人
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """看看有没有外星人到过屏幕底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 当成是飞船被撞
                self._ship_hit()
                break

    def _ship_hit(self):
        """回应被外星人击中的飞船"""
        if self.stats.ships_left > 0:
            # 减少船舶左侧，并更新记分板
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # 除掉剩下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            
            # 建立一支新的舰队，并以飞船为中心
            self._create_fleet()
            self.ship.center_ship()
            
            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """创造外星人舰队"""
        # 创造一个外星人，然后找出一排外星人的数量
        # 每个外星人之间的距离等于一个外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # 确定适合显示在屏幕上的外星人行数
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # 创造全部的外星人舰队
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创造一个外星人并把它放在一排"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """如果检测到有外星人到达边缘，方向进行改变."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """外星人向屏幕下侧移动，并改变方向."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，然后翻到新的屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 画出得分信息
        self.sb.show_score()

        # 如果游戏处于非活动状态，则画出播放按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # 做一个游戏实例，然后运行游戏
    ai = AlienInvasion()
    ai.run_game()
