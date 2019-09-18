from game import Pencil
import random  # Not needed for all players

class GenericAI(Pencil):
    """
    If you beat this AI in a match, your name will be get listed below by me (Jeremy):

    """

    def __init__(self, name):
        super().__init__(name)

    def play(self, paper):
        return random.choice(paper.possible_moves)
