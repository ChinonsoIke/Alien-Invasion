import pygame
from pygame.sprite import Group
from scoreboard import ScoreBoard


from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button

def run_game():
    #initialize game
    pygame.init()
    ai_settings= Settings()
    screen= pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # make play button
    play_button= Button(ai_settings, screen, 'Play')

    # create instance to store game stats
    stats= GameStats(ai_settings)

    # scoreboad
    score_board= ScoreBoard(ai_settings, screen, stats)

    # make ship, group of bullets and group of aliens
    ship= Ship(screen, ai_settings)
    bullets= Group()
    aliens= Group()

    # create fleet of aliens
    gf.create_fleet(aliens, ai_settings, screen, ship)

    # start the main loop for the game
    while True:
        # watch for keyboard and mouse events
        gf.check_events(ai_settings, ship, screen, bullets, stats,
            play_button, aliens, score_board)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, ship,
                screen, stats, score_board)
            gf.update_aliens(aliens, ai_settings, ship, stats, bullets,
                screen, score_board)

        # redraw screen during each pass of the loop and update screen
        gf.update_screen(ai_settings, ship, screen, bullets, aliens,
            stats, play_button, score_board)
        

run_game()
            