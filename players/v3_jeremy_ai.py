from game import Pencil
import random
import numpy as np

class BruteV3(Pencil):

    def __init__(self, name, max_depth=0):
        super().__init__(name)
        self.max_depth = 3
        self.turn_num = 0

    def get_adj_player_spots(self, paper, wall_coord):
        adjacents = paper.get_adjacents(wall_coord)
        return [p for p in adjacents if paper.is_player_spot(p)]

    def get_wall_count(self, paper, player_spot):
        walls = paper.get_adjacents(player_spot)
        return sum([paper[wall] for wall in walls])

    def get_gap_walls(self, paper, player_spot):
        walls = paper.get_adjacents(player_spot)
        return [wall for wall in walls if paper.is_empty(wall)]


    def shares_gap(self, paper, player_spot1, player_spot2):
        if not paper.is_player_spot(player_spot1) or not paper.is_player_spot(player_spot2):
            return False
        p1_walls = paper.get_adjacents(player_spot1)
        p2_walls = paper.get_adjacents(player_spot2)
        for wall in p1_walls:
            if wall in p2_walls and paper.is_empty(wall):
                return True
        return False


    def get_neighbor_players(self, paper, player_spot):
         return [tuple(i) for i in list(np.array(
            [player_spot for _ in range(4)]) + np.array([(0, 2), (0, -2), (2, 0), (-2, 0)])) if paper.is_valid(tuple(i))]

    def get_max_walls(self, paper, wall_coord):
        wall_counts = []
        player_spots = self.get_adj_player_spots(paper, wall_coord)
        for player_spot in player_spots:
            walls = paper.get_adjacents(player_spot)
            wall_counts.append(sum([paper[wall] for wall in walls]))
        return max(wall_counts)

    def get_two_path(self, paper, player_spot, prev_player_spot=None, path=None):
        if not path:
            path = []
        player_walls = paper.get_adjacents(player_spot)
        gaps = [wall for wall in player_walls if paper.is_empty(wall) and wall not in path]
        if len(gaps) == 0:
            return path
        else:
            path.extend(gaps)
        adj_players = self.get_neighbor_players(paper, player_spot)
        for adj_player in adj_players:

            if adj_player != prev_player_spot and \
                    self.shares_gap(paper, player_spot, adj_player) and \
                    self.get_wall_count(paper, adj_player) == 2:
                path.extend(self.get_two_path(paper, adj_player, player_spot, path))
        return path

    def gap_in_path(self, gaps, path):

        gap_count = 0
        for gap in gaps:
            if gap in path:
                gap_count += 1

    def can_add_path(self, paper, player_spot, paths):
        player_walls = paper.get_adjacents(player_spot)
        if sum([paper[wall] for wall in player_walls]) != 2:
            return False
        if not paths:
            return True
        for path in paths:
            for wall in player_walls:
                if wall in path:
                    return False
        return True

    def two_wall_paths(self, paper):
        paths = []
        player_spots = paper.get_player_spots()
        for player_spot in player_spots:
            if self.can_add_path(paper, player_spot, paths):
                paths.append(self.get_two_path(paper, player_spot, None, []))
        return paths

    def play(self, paper):
        self.turn_num = paper.turn
        random.shuffle(paper.possible_moves)
        max_walls = [self.get_max_walls(paper, move) for move in paper.possible_moves]
        priority = [3, 0, 1, 2]
        for i in priority:
            if i in max_walls:
                if i == 2:
                    paths = self.two_wall_paths(paper)
                    min_path_length = -1
                    min_path = paths[0]
                    for n, path in enumerate(paths):
                        if len(path) < min_path_length:
                            min_path = path
                    return min_path[0]
                return paper.possible_moves[max_walls.index(i)]
        
        print("no idea how it got here...")
        return random.choice(paper.possible_moves)