

class Player:

    def __init__(self, game_state, player_id):
        # Give the player a deepcopy of a GameState where all other players are itself instead of opponents
        self.game_state = game_state
        self.player_id = player_id

    def play(self):
        # Action that the player is going to take (should be called from GameState)
        pass



