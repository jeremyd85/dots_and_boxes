import numpy as np
import copy


class Board:

    def __init__(self, rows=1, cols=1):
        self.rows = rows
        self.cols = cols
        self._grid = None
        self.setup()

    @property
    def grid(self):
        return copy.deepcopy(self._grid)

    def __getitem__(self, key):
        return self._grid[key]

    def setup(self):
        # Make the grid state of a new game
        self._grid = np.full((self.rows, self.cols), np.inf)

    def update(self):
        pass
