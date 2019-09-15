import copy


class GameState:

    def __init__(self, board=None, players=None):
        self.board = board
        self.players = players
        self.turn = 0

    def get_possible_actions(self):
        # returns list of possible actions
        pass

    def take_action(self, action):
        # takes the action on the current state
        pass

    def get_action_state(self, action):
        # takes an action on a new deepcopy state
        return copy.deepcopy(self).take_action(action)

    def is_terminal(self):
        # is the game over?
        pass

    def get_scores(self):
        # unsure if necessary
        # returns current score
        pass

    def get_reward(self):
        # if terminal state give reward
        pass

    def update(self):
        # really unsure if necessary
        pass
