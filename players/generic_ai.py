from game import Pencil
import random  # Not needed for all players


class GenericAI(Pencil):

    def __init__(self, name):
        super().__init__(name)

    def play(self, paper):
        return random.choice(paper.get_possible_moves())
