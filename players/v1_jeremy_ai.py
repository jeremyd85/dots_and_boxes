from game import Pencil
import random


class BruteV1(Pencil):

    def __init__(self, name, max_depth=0):
        super().__init__(name)
        self.max_depth = 3
        self.turn_num = 0

    def get_adj_player_spots(self, paper, wall_coord):
        adjacents = paper.get_adjacents(wall_coord)
        return [p for p in adjacents if paper.is_player_spot(p)]

    def get_max_walls(self, paper, wall_coord):
        wall_counts = []
        player_spots = self.get_adj_player_spots(paper, wall_coord)
        for player_spot in player_spots:
            walls = paper.get_adjacents(player_spot)
            wall_counts.append(sum([paper[wall] for wall in walls]))
        return max(wall_counts)

    def play(self, paper):
        self.turn_num = paper.turn
        random.shuffle(paper.possible_moves)
        max_walls = [self.get_max_walls(paper, move) for move in paper.possible_moves]
        priority = [3, 0, 1, 2]
        for i in priority:
            if i in max_walls:
                return paper.possible_moves[max_walls.index(i)]
        
        print("no idea how it got here...")
        return random.choice(paper.possible_moves)