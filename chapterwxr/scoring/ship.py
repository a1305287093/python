import pygame
 
from pygame.sprite import Sprite
 
class Ship(Sprite):
    """管理飞船的类"""
 
    def __init__(self, ai_game):
        """初始化飞船并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载船舶图像并得到正确的
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 在屏幕的底部中心开始每一艘新船
        self.rect.midbottom = self.screen_rect.midbottom

        # 为船舶的水平位置存储一个十进制值
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志更新船只位置"""
        # 更新飞船的 x 值，而不是最新值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 从 self. x 更新 rect 对象
        self.rect.x = self.x

    def blitme(self):
        """把飞船画到它现在的位置"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """把飞船对准屏幕"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
