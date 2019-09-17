from generic_game import Board
import numpy as np
import copy


class Paper(Board):

    def __init__(self, player1, player2, width=10, height=10):
        super().__init__(width*2+1, height*2+1)
        self.possible_moves = self.get_possible_moves()
        self.invalid_moves = []
        self.player1 = player1
        self.player2 = player2
        self.turn = -1

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
        return [tuple(i) for i in list(np.array([move for i in range(4)]) + np.array([(0, 1), (0, -1), (1, 0), (-1, 0)])) if self.is_valid(tuple(i))]

    def get_possible_moves(self):
        """ Get all possible moves on the paper

        :return: a list with all possible moves
        """

        return [(row, col) for row, col in
                [(i // self.height, i % self.width) for i in range(self.width*self.height)]
                if self.is_wall_spot((row, col)) and self.is_empty((row, col))]


    def draw(self, move):
        """ This is used to draw a line in the game (Used wrapper draw() for fun)

        :param move: tuple as (x, y) of where to draw a line
        :return: True if the move was valid
        """

        if move in self.possible_moves:
            self._grid[move] = 1
            claimed = False
            for player_spot in self.get_adjacents(move):
                if all([not self.is_empty(wall) for wall in self.get_adjacents(player_spot)]):
                    claimed = True
                    self._grid[player_spot] = self.turn
            if not claimed:
                self.turn *= -1
            return True
        return False

    def get_draw_state(self, move):
        """ Get a deepcopy of the this Table after taking a move

        :param move: (x, y) tuple of where to take a move
        :return: The Table after the move or None if the move failed
        """
        paper_copy = self.get_copy()
        return paper_copy if paper_copy.draw(move) else None

    def get_copy(self):
        paper_copy = copy.deepcopy(self)
        if self.turn == -1:
            paper_copy.player2 = copy.deepcopy(paper_copy.player1)
        else:
            paper_copy.player1 = copy.deepcopy(paper_copy.player2)
        return paper_copy

    def get_player_spots(self):
        return [(row, col) for row, col in
                [(i // self.height, i % self.width) for i in range(self.width*self.height)]
                if self.is_player_spot((row, col))]

    def get_scores(self):
        player_spots = self.get_player_spots()
        scores = {'p1': 0, 'p2': 0, 'total': len(player_spots)}
        for player_spot in player_spots:
            if self._grid[player_spot] == -1:
                scores['p1'] += 1
            elif self._grid[player_spot] == 1:
                scores['p2'] += 1
        return scores

    def winner(self):
        scores = self.get_scores()
        winning_score = scores['total'] // 2 + 1
        if scores['p1'] >= winning_score:
            return -1
        elif scores['p2'] >= winning_score:
            return 1
        else:
            return None

    def take_turn(self):
        if self.get_possible_moves():
            paper_copy = self.get_copy()
            if self.turn == -1:
                self.draw(self.player1.play(paper_copy))
            else:
                self.draw(self.player2.play(paper_copy))
        return self.winner()







