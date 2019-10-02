from game import Pencil
import random


class Brute(Pencil):

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

    def get_score(self, paper):
        p_score = paper.get_scores()
        t = (paper.size[0] * paper.size[1])
        w = t // 2 + 1
        p = p_score[paper.turn]
        o = p_score[paper.turn*-1]
        return ((p + 1) / (o + 1))

    def get_move_score(self, paper, depth=1):
        if len(paper.possible_moves) == 0 or depth == self.max_depth:
            return self.get_score(paper)
        if paper.turn != self.turn_num:
            paper.draw(paper.player1.fake_play(paper)) if paper.turn == paper.PLAYER1 else paper.draw(paper.player2.fake_play(paper))
        move_score = 0
        for move in paper.possible_moves:
            move_score += self.get_move_score(paper.get_draw_state(move), depth+1)
        return self.get_score(paper) + move_score

    def play(self, paper):
        self.turn_num = paper.turn
        random.shuffle(paper.possible_moves)
        move_scores = []
        max_walls = [self.get_max_walls(paper, move) for move in paper.possible_moves]
        priority = [3, 0, 1, 2]
        for i in priority:
            if i in max_walls:
                return paper.possible_moves[max_walls.index(i)]

        print("no idea how it got here...")
        return random.choice(paper.possible_moves)

        for m in paper.possible_moves:
            move_scores.append(self.get_move_score(paper.get_draw_state(m)))
        i = move_scores.index(max(move_scores))
        return paper.possible_moves[i]


    def fake_play(self, paper):
        random.shuffle(paper.possible_moves)
        max_walls = [self.get_max_walls(paper, move) for move in paper.possible_moves]
        priority = [3, 0, 1, 2]
        for i in priority:
            if i in max_walls:
                return paper.possible_moves[max_walls.index(i)]

        print("no idea how it got here...")
        return random.choice(paper.possible_moves)