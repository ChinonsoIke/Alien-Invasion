import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """define attributes and behavior of ship"""
    def __init__(self, screen, ai_settings):
        """initialize the ship and get its starting position"""
        super().__init__()
        self.screen= screen
        self.ai_settings= ai_settings

        # load ship image and get its rect
        self.image= pygame.image.load('images/ship.bmp')
        self.rect= self.image.get_rect()
        self.screen_rect= self.screen.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.centerx= self.screen_rect.centerx
        self.rect.bottom= self.screen_rect.bottom

        # store a decimal value for the ship's center
        self.center= float(self.rect.centerx)

        # moving flag
        self.moving_right= False
        self.moving_left= False

    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right== True and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        
        if self.moving_left== True and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update rect.centerx from self.center
        self.rect.centerx= self.center

    def center_ship(self):
        """center ship on screen"""
        self.center= self.screen_rect.centerx