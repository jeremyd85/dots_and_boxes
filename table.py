
import copy

from paper import Paper


class Table():

    def __init__(self, paper, players=None):
        self.paper = paper
        self.players = players
        self.turn = -1

    def get_possible_moves(self):
        """ Get all possible moves on the paper

        :return: a list with all possible moves
        """

        w = self.paper.width
        h = self.paper.height
        return [(r, c) for r, c in [(i // h, i % w) for i in range(w*h)]
                if Paper.is_wall_spot((r, c)) and self.paper.is_empty((r, c))]

    def draw(self, move):
        """ This is used to draw a line in the game (Used wrapper draw() for fun)

        :param move: tuple as (x, y) of where to draw a line
        :return: True if the move was valid
        """

        if move in self.get_possible_moves():
            action_grid = self.paper.grid
            action_grid[move] = 1
            self.paper.update(action_grid)
            for m in self.paper.get_adjacents(move):
                if all([True if not self.paper.is_empty(wall) else False for wall in self.paper.get_adjacents(m)]):
                    action_grid[m] = self.turn
            if action_grid != self.paper.grid:
                self.paper.update(action_grid)
                # TODO change active player
            return True
        return False

    def get_draw_state(self, move):
        """ Get a deepcopy of the this Table after taking a move

        :param move: (x, y) tuple of where to take a move
        :return: The Table after the move or None if the move failed
        """
        new_table = copy.deepcopy(self)
        return new_table if new_table.draw(move) else None

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


t = Table(Paper(5, 5))

t.draw((0, 1))
t.draw((0, 0))
new_state = t.get_draw_state((1, 0))
new_state.draw((1, 2))
new_state.draw((2, 1))
print(t.paper.grid)
print(new_state.paper.grid)