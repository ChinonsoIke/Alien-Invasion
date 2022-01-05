import pygame.font
from pygame.sprite import Group

from ship import Ship

class ScoreBoard():
    """class to keep scores"""
    def __init__(self, ai_settings, screen, stats):
        self.screen= screen
        self.screen_rect= screen.get_rect()
        self.ai_settings= ai_settings
        self.stats= stats

        # set text color and font
        self.text_color= (30,30,30)
        self.font= pygame.font.SysFont(None, 27)

        # prepare score image
        self.prep_score_image()
        self.prep_highscore_image()
        self.prep_level_image()
        self.prep_ships()

    def prep_score_image(self):
        """turn score into image"""
        rounded_score= round(self.stats.score, -1)
        score_str= "SCORE- {:,}".format(rounded_score)
        self.score_image= self.font.render(score_str,
            True, self.text_color, self.ai_settings.bg_color)

        self.score_rect= self.score_image.get_rect()
        self.score_rect.right= self.screen_rect.right - 20
        self.score_rect.top= 20

    def show_score(self):
        """draw score to screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highscore_image, self.highscore_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # draw ships
        self.ships.draw(self.screen)

    def prep_highscore_image(self):
        """turn highscore into image"""
        rounded_score= round(self.stats.highscore, -1)
        score_str= "HIGHSCORE- {:,}".format(rounded_score)
        self.highscore_image= self.font.render(score_str,
            True, self.text_color, self.ai_settings.bg_color)

        self.highscore_rect= self.highscore_image.get_rect()
        self.highscore_rect.centerx= self.screen_rect.centerx
        self.highscore_rect.top= 20

    def prep_level_image(self):
        """turn level into image"""
        level_str= 'LEVEL- ' + str(self.stats.level)
        self.level_image= self.font.render(level_str,
            True, self.text_color, self.ai_settings.bg_color)

        self.level_rect= self.level_image.get_rect()
        self.level_rect.right= self.screen_rect.right - 20
        self.level_rect.top= self.score_rect.bottom + 10

    def prep_ships(self):
        """show ships left"""
        self.ships= Group()
        for ship_number in range(self.stats.ships_left):
            ship= Ship(self.screen, self.ai_settings)
            ship.rect.x= 10 + ship_number * ship.rect.width
            ship.rect.y= 10
            self.ships.add(ship)