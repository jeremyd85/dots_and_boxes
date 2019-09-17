from game import Paper
from players import *
import random


class Arena:

    def __init__(self, players, size=(7, 7)):
        self.width = size[0]
        self.height = size[1]
        self.active_players = players
        random.shuffle(self.active_players)
        self.inactive_players = []
        self.rounds = []
        self.round_num = 1

    def create_round(self):
        matches = []
        if len(self.active_players) == 1:
            return self.active_players
        num_matches = len(self.active_players) // 2 if len(self.active_players) % 2 == 0 else 1
        for match_num in range(num_matches):
            match = [self.active_players[match_num], self.active_players[:-match_num]]
            matches.append(match)
        self.rounds.append(matches)
        return matches

    def play_match(self, match):
        p1 = match[0]
        p2 = match[1]
        game = Paper(p1, p2, self.width, self.height)
        while not game.winner():
            game.take_turn()
        if game.winner() == -1:
            self.active_players.remove(p2)
            self.inactive_players.append(p2)
            return p1
        else:
            self.active_players.remove(p1)
            self.inactive_players.append(p1)
            return p2

    def play_round(self, r):
        winners = []
        for m in r:
            winners.append(self.play_match(m))
        return winners

    def start(self):
        winners = []
        r = self.create_round()
        while len(r) > 1:
            winners.append(self.play_round(r))
            r = self.create_round()
        return self.rounds


def main():
    # num_players = 8
    # players = []
    # for i in range(num_players):
    #     player_name = 'ai{0}'.format(i)
    #     players.append(GenericAI(player_name))
    # arena = Arena(players)
    # rounds = arena.start()
    #
    # for n, r in enumerate(rounds):
    #     print('round {0}:'.format(n + 1))
    #     for match in r:
    #         print('{0} vs. {1}'.format(match[0].name, match[1].name))



    width = 5
    height = 5
    p1 = DestroyerOfJesse('AI1', 0)
    p2 = DestroyerOfJesse('AI2', 0)
    game = Paper(p1, p2, width, height)
    while game.take_turn() is None:
        input()
        print(game.grid)

    if game.winner() == -1:
        print(game.player1.name)
    else:
        print(game.player2.name)

main()