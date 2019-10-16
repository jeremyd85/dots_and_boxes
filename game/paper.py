from generic_game import Board
import numpy as np
import copy


class Paper(Board):
    """
    This is a class that is the playing board for the game. All of the rules of the game are coded into
    this board. If you want to know the rules, check out the Wikipedia page:
    https://en.wikipedia.org/wiki/Dots_and_Boxes
    Since it is a paper based game, I made it called Paper! See what I did there??

    Let's make the game run. Look at main.py for how it is done there. Basics though:

        Start game with 2 players (Pencil objects) See what I did there?? Pencil... Paper... and
        a board size width and height.

            w = 7
            h = 7
            p1 = Pencil('some name')
            p2 = Pencil('some other name')
            paper = Paper(p1, p2, 7, 7)

        ^ That would make a 7 x 7 game with player1 and player2 as base Pencil objects.

            while not paper.winner():
                paper.take_turn()
                print(paper.grid)

        ^ This will now start a loop that will continually take a turn until there is
        a winner. (Turn switching is done automatically. Don't worry about it).

    If you want to make an AI to play this game, look at the docs for the Pencil class in pencil.py
    """

    # Values on the grid
    PLAYER1 = -1
    PLAYER2 = 1
    WALL = 1
    BLANK = 0

    def __init__(self, player1, player2, rows=10, cols=10):
        super().__init__(rows*2+1, cols*2+1)
        self.size = (rows, cols)
        self.possible_moves = self.get_possible_moves()
        self.invalid_moves = []
        self.player1 = player1
        self.player2 = player2
        self.turn = Paper.PLAYER1

    def setup(self):
        """ This function sets up the board. All initial values are zero"""

        self._grid = np.zeros((self.rows, self.cols))

    def update(self):
        """ Make a turn for the current player

        :return: True if there is a move
        """

        if self.possible_moves:
            paper_copy = self.get_copy()
            if self.turn == -1:
                self.draw(self.player1.play(paper_copy))
            else:
                self.draw(self.player2.play(paper_copy))
            return True
        return False

    def get_copy(self):
        """ Get a copy of this paper with the current player as both players

        :return: A deepcopy of this paper
        """

        # print(self.__dict__)  # paper holds an NNAI object and will call NNAI.__deepcopy__()
        paper_copy = copy.deepcopy(self)
        if self.turn == Paper.PLAYER1:
            paper_copy.player2 = copy.deepcopy(paper_copy.player1)
        else:
            paper_copy.player1 = copy.deepcopy(paper_copy.player2)
        return paper_copy

    @staticmethod
    def is_wall_spot(coord):
        """ Check if a coordinate is a wall spot

        :param coord: (row, col) coordinate on the paper
        :return: True if the coordinate is in a wall spot
        """

        return sum(coord) % 2 != 0

    @staticmethod
    def is_player_spot(coord):
        """ Check if a coordinate is a player spot

        :param coord: (row, col) coordinate on the paper
        :return: True if the coordinate is in a player spot
        """

        return coord[0] % 2 != 0 and coord[1] % 2 != 0

    def is_empty(self, coord):
        """ Check if a coordinate is empty (Paper.BLANK)

        :param coord: (row, col) coordinate on the paper
        :return: True if the coordinate is empty
        """

        return self._grid[coord] == Paper.BLANK

    def is_valid(self, coord):
        """ Check if the a coordinate is actionable and in bounds

        :param coord: (row, col) coordinate on the paper
        :return: True if the coordinate is in bounds and an actionable spot
        """

        return self.rows > coord[0] >= 0 and \
               self.cols > coord[1] >= 0 and \
               (self.is_player_spot(coord) or self.is_wall_spot(coord))

    def get_adjacents(self, coord):
        """ Get all valid coordinates adjacent to a certain coordinate

        :param coord: (row, col) coordinate on the paper
        :return: a list of coordinates adjacent to the coord
        """

        return [tuple(i) for i in list(np.array(
            [coord for _ in range(4)]) + np.array([(0, 1), (0, -1), (1, 0), (-1, 0)])) if self.is_valid(tuple(i))]

    def get_possible_moves(self):
        """ Get all possible moves on the paper

        :return: a list with all possible moves
        """

        return [(row, col) for row, col in
                [(i // self.cols, i % self.cols) for i in range(self.rows*self.cols)]
                if self.is_wall_spot((row, col)) and self.is_empty((row, col))]

    def get_player_spots(self):
        """ Get a list of all coordinates that can have a player

        :return: a list of coordinates that can take a player value
        """

        return [(row, col) for row, col in
                [(i // self.cols, i % self.cols) for i in range(self.cols*self.rows)]
                if self.is_player_spot((row, col))]

    def draw(self, coord):
        """ This is used to draw a line in the game (Added a wall)

        :param coord: tuple as (x, y) of where to draw a line
        :return: True if the move was valid
        """

        if coord in self.possible_moves:
            self.possible_moves.remove(coord)
            self.invalid_moves.append(coord)
            self._grid[coord] = Paper.WALL
            claimed = False
            for player_spot in self.get_adjacents(coord):
                if all([not self.is_empty(wall) for wall in self.get_adjacents(player_spot)]):
                    claimed = True
                    self._grid[player_spot] = self.turn
            if not claimed:
                self.turn *= -1
            return True
        return False

    def get_draw_state(self, coord):
        """ Get a deepcopy of the this Table after taking a move

        :param coord: (x, y) tuple of where to take a move
        :return: The Table after the move or None if the move failed
        """

        paper_copy = self.get_copy()
        return paper_copy if paper_copy.draw(coord) else None

    def get_scores(self):
        """ Get the scores for each player

        :return: dictionary of each player's score and the total number of players
        """

        player_spots = self.get_player_spots()
        scores = {'player1': 0, 'player2': 0, 'total': len(player_spots)}
        for player_spot in player_spots:
            if self._grid[player_spot] == Paper.PLAYER1:
                scores['player1'] += 1
            elif self._grid[player_spot] == Paper.PLAYER2:
                scores['player2'] += 1
        return scores

    def winner(self, early_exit=True):
        """ Get the player ID of the player that won if there is one

        :return: player ID of a player that won, 0 if there is a tie, None if there is no winner
        """
        # ties are not properly handled
        scores = self.get_scores()
        winning_score = scores['total'] // 2 + 1
        if scores['player1'] >= winning_score and early_exit:
            return Paper.PLAYER1
        elif scores['player2'] >= winning_score and early_exit:
            return Paper.PLAYER2
        elif scores['player1'] == scores['player2'] == (winning_score-1):
            return 0
        elif early_exit:
            return None
        elif not self.get_possible_moves():
            return Paper.PLAYER1 if scores['player1'] > scores['player2'] else Paper.PLAYER2
        else:
            return None
