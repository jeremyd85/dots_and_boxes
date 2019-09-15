import numpy as np


class Board:

    def __init__(self, width=1, height=1):
        self.width = width
        self.height = height
        self.grid = None
        self.setup()

    # TODO make index operations???

    def setup(self):
        # Make the grid state of a new game
        self.grid = np.full((self.width, self.height), np.inf)

    def update(self):
        # Update a grid based on external changes on the board's state
        # (Not sure if it will be useful)
        pass

