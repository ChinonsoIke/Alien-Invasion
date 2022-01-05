import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """bullet class"""
    def __init__(self, screen, ship, ai_settings):
        """create bullet at ship's coordinates"""
        super().__init__()
        self.screen= screen

        # initialize bullet at 0,0 coordinates
        self.rect= pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx= ship.rect.centerx
        self.rect.top= ship.rect.top

        # store y coordinate of bullet as decimal
        self.y= float(self.rect.y)

        self.color= ai_settings.bullet_color
        self.speed_factor= ai_settings.bullet_speed_factor

    def update(self):
        """make bullet move up screen"""
        # update decimal position of bullet
        self.y -= self.speed_factor
        # update rect position
        self.rect.y= self.y

    def draw(self):
        """draw bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)