import pygame
from pygame.sprite import Sprite
 
class Bullet(Sprite):
    """管理从船上发射的子弹的类"""

    def __init__(self, ai_game):
        """在飞船目前的位置制造一个子弹物体"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在(0,0)创建一个项目符号 rect，然后设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # 将子弹的位置存储为十进制值
        self.y = float(self.rect.y)

    def update(self):
        """把子弹移到屏幕上."""
        # 更新子弹的小数位置
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """把子弹画到屏幕上"""
        pygame.draw.rect(self.screen, self.color, self.rect)
