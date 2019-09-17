from game.pencil import Pencil
import random

class DestroyerOfJesse(Pencil):

    def __init__(self, name, max_depth):
        super().__init__(name)
        self.max_depth = max_depth

    def play(self, paper):
        return random.choice(paper.get_possible_moves())


        return [0]