from game import Paper
import numpy as np
import random
import os


class DataGenArena:
    BASEDIR = 'player_files'

    def __init__(self, players, arena_name, size=(7, 7)):
        self.players = players
        self.arena_name = arena_name
        self.rows = size[0]
        self.cols = size[1]
        self.round_num = 0
        self.max_game_len = 2*self.rows*self.cols + self.rows + self.cols
        self.shuffle = True  # might not be the best way

    def play_match(self, p1, p2):
        game = Paper(p1, p2, self.rows, self.cols)
        game_states = []
        while game.winner() is None:
            game_state = game.grid
            game_state90 = np.rot90(game_state)
            game_state180 = np.rot90(game_state90)
            game_state270 = np.rot90(game_state180)
            game_state_flip = np.flip(game_state, 0)
            game_state_flip90 = np.flip(game_state90, 0)
            game_state_flip180 = np.flip(game_state180, 0)
            game_state_flip270 = np.flip(game_state270, 0)
            game_states.extend((game_state, game_state90, game_state180, game_state270,
                                game_state_flip, game_state_flip90, game_state_flip180, game_state_flip270))
        game_states = np.stack(game_states)
        game_results = [game.winner()]*len(game_states)
