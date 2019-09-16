from generic_game import Board
import numpy as np


class Paper(Board):

    def __init__(self, width=10, height=10):
        super().__init__(width, height)

    def setup(self):
        self._grid = np.zeros((self.width, self.height))

    @staticmethod
    def is_wall_spot(move):
        return sum(move) % 2 != 0

    @staticmethod
    def is_player_spot(move):
        return move[0] % 2 != 0 and move[1] % 2 != 0

    def is_empty(self, move):
        return self._grid[move] == 0

    def is_valid(self, move):
        return self.height > move[0] >= 0 and \
               self.width > move[1] >= 0 and \
               (self.is_player_spot(move) or self.is_wall_spot(move))

    def get_adjacents(self, move):
        return [m for m in [(move[0], move[1]-1), (move[0], move[1]+1), (move[0]-1, move[1]), (move[0]+1, move[1])]
                if self.is_valid(m)]






