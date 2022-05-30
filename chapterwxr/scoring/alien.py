import pygame
from pygame.sprite import Sprite
 
class Alien(Sprite):
    """“代表舰队中一个外星人的等级"""

    def __init__(self, ai_game):
        """初始化外星人，设置它的起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 载入外星人的图像，设置它的 rect 属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 启动屏幕左上角附近的每个新外星人
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人在屏幕边缘，返回 true"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """左右移动飞船"""
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x
