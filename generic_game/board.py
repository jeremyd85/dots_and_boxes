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

    def __getitem__(self, key):
        return self._grid[key]

    def setup(self):
        # Make the grid state of a new game
        self._grid = np.full((self.height, self.width), np.inf)

    def update(self):
        pass
