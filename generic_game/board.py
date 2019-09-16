import numpy as np
import copy


class Board:

    def __init__(self, width=1, height=1):
        self.width = width
        self.height = height
        self._grid = None
        self.setup()

    @property
    def grid(self):
        return copy.deepcopy(self._grid)

    # TODO make index operations???

    def setup(self):
        # Make the grid state of a new game
        self._grid = np.full((self.width, self.height), np.inf)

    def update(self, new_grid):
        self._grid = new_grid

