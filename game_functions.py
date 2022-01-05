import pygame
import sys
from time import sleep

from bullet import Bullet
from alien import Alien

def check_events(ai_settings, ship, screen, bullets, stats, play_button,
        aliens, score_board):
    """check for events that occur during the game"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, ship, screen, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y= pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y,
                aliens, bullets, ai_settings, screen, ship, score_board)

def check_play_button(stats, play_button, mouse_x, mouse_y,
        aliens, bullets, ai_settings, screen, ship, score_board):
    """check if mouse was clicked on play button"""
    button_clicked= play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # hide mouse cursor
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        ai_settings.initialize_dynamic_settings()
        stats.game_active= True

        score_board.prep_score_image()
        score_board.prep_highscore_image()
        score_board.prep_level_image()
        score_board.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(aliens, ai_settings, screen, ship)

def update_screen(ai_settings, ship, screen, bullets, aliens,
        stats, play_button, score_board):
    """update images and flip screen"""
    screen.fill(ai_settings.bg_color)
    # redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw()

    ship.blitme()
    aliens.draw(screen)
    score_board.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def check_keydown_events(event, ai_settings, ship, screen, bullets):
    """respond to keypresses"""
    # print(event)
    if event.key == pygame.K_RIGHT:
        ship.moving_right= True
    elif event.key == pygame.K_LEFT:
        ship.moving_left= True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, ship, screen, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right= False
    elif event.key == pygame.K_LEFT:
        ship.moving_left= False

def update_bullets(bullets, aliens, ai_settings, ship,
        screen, stats, score_board):
    """update bullets and delete old bullets"""
    bullets.update()

    # delete bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(bullets, aliens, ai_settings, ship,
        screen, stats, score_board)

def check_bullet_alien_collisions(bullets, aliens, ai_settings, ship,
        screen, stats, score_board):
    """check for bullet-alien collisions"""
    # delete bullets and aliens that have collided
    collisions= pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            score_board.prep_score_image()
            check_highscore(stats, score_board)

    if len(aliens) == 0:
        # destroy all bullets, increase speed and create new fleet
        bullets.empty()
        ai_settings.increase_speed()

        # add level
        stats.level += 1
        score_board.prep_level_image()

        create_fleet(aliens, ai_settings, screen, ship)

def fire_bullet(ai_settings, ship, screen, bullets):
    """create and fire new bullet if limit not reached"""
    # create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet= Bullet(screen, ship, ai_settings)
        bullets.add(new_bullet)

def create_fleet(aliens, ai_settings, screen, ship):
    """create new fleet of aliens"""
    # create an alien
    # spacing between aliens is equal to one alien width
    alien= Alien(ai_settings, screen)
    number_aliens_x= number_aliens(ai_settings, alien.rect.width)
    number_rows= get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    

    # create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        

def number_aliens(ai_settings, alien_width):
    """find the number of aliens that fit in a row"""
    available_space_x= ai_settings.screen_width - 2 * alien_width
    number_aliens_x= int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """create new alien and set position of alien"""
    alien= Alien(ai_settings, screen)
    alien_width= alien.rect.width
    alien.x= alien_width + 2 * alien_width * alien_number
    alien.rect.x= alien.x
    alien.rect.y= alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """get number of rows fleet can occupy"""
    available_space_y= (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows= int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(aliens, ai_settings, ship, stats, bullets,
        screen, score_board):
    """check if alien is at edge and 
        update position of all aliens in the fleet"""
    check_fleet_edges(aliens, ai_settings)
    aliens.update()

    # look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(aliens, ai_settings, ship, stats, bullets, screen, score_board)
    
    # check for alien ships reaching bottom
    check_aliens_reach_bottom(aliens, ai_settings, ship, stats, bullets,
        screen, score_board)

def ship_hit(aliens, ai_settings, ship, stats, bullets, screen, score_board):
    """respond to ship being hit"""
    if stats.ships_left > 0:
        # decrement ships by 1
        stats.ships_left -= 1

        # update ships left
        score_board.prep_ships()

        # remove any existing bullets and aliens
        bullets.empty()
        aliens.empty()

        # create a new fleet and center the ship
        create_fleet(aliens, ai_settings, screen, ship)
        ship.center_ship()
        # print(stats.ships_left)

        # pause
        sleep(0.5)
    else:
        stats.game_active= False
        pygame.mouse.set_visible(True)

def check_aliens_reach_bottom(aliens, ai_settings, ship, stats, bullets,
        screen, score_board):
    """check if any aliens reach the bottom of screen"""
    screen_rect= screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            # treat same as ship hit
            ship_hit(aliens, ai_settings, ship, stats, bullets,
                screen, score_board)
            break

def check_fleet_edges(aliens, ai_settings):
    """respond to any aliens reaching edge of screen"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(aliens, ai_settings)
            break

def change_fleet_direction(aliens, ai_settings):
    """drop entire fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_highscore(stats, score_board):
    """check for highscore"""
    if stats.score > stats.highscore:
        stats.highscore= stats.score
        score_board.prep_highscore_image()