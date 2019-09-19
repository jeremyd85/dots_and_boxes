from game import Paper
import random
import json
import os


class Arena:

    BASEDIR = 'saved_games'

    def __init__(self, players, arena_name, size=(7, 7)):
        self.active_players = players
        self.inactive_players = []
        self.rounds = []
        self.arena_name = arena_name
        self.rows = size[0]
        self.cols = size[1]
        self.round_num = 0
        random.shuffle(self.active_players)

    def play_match(self, p1, p2):
        match = {'round': self.round_num, 'players': [p1.name, p2.name], 'winner': None,
                 'size': [self.rows, self.cols], 'moves': []}
        game = Paper(p1, p2, self.rows, self.cols)
        while not game.winner():
            move = {'player': game.player1.name if game.turn == game.PLAYER1 else game.player2.name, 'grid': None}
            game.update()
            move['grid'] = list([list(row) for row in game.grid])
            match['moves'].append(move)
        if game.winner() == Paper.PLAYER1:
            winner, loser = p1, p2
        else:
            winner, loser = p2, p1
        self.active_players.remove(loser)
        self.inactive_players.append(loser)
        match['winner'] = winner.name
        return match

    def create_round(self):
        num_players = len(self.active_players)
        matches = []
        if num_players == 1:
            return []
        if num_players % 2 != 0:
            match = (self.active_players[0], self.active_players[1])
            matches.append(match)
        else:
            matches = [m for m in zip(self.active_players[::2], self.active_players[1::2])]
        return matches

    def play_round(self, p_round):
        self.round_num += 1
        for n, match in enumerate(p_round):
            result = self.play_match(match[0], match[1])
            print(result)
            self.save_result(result, n+1)

    def save_result(self, result, match_num):
        file_path = os.path.join(Arena.BASEDIR, self.arena_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = 'round{0}match{1}.json'.format(result['round'], match_num)
        file_path = os.path.join(file_path, file_name)
        with open(file_path, 'w+') as json_file:
            json.dump(result, json_file)