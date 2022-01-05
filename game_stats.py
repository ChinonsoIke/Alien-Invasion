class GameStats():
    """track stats for Alien Invasion"""
    def __init__(self, ai_settings):
        self.ai_settings= ai_settings
        self.reset_stats()
        # start game in an inactive state
        self.game_active= False

        self.highscore= 0

    def reset_stats(self):
        """initialize stats"""
        self.ships_left= self.ai_settings.ship_limit
        self.score= 0
        self.level= 1