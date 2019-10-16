import torch
import torch.nn as nn
import torch.nn.functional as F

import os
from game import Arena
import json
from game import Pencil
import random

# I need to learn more about profiling properly
from timeit import default_timer as Timer
import functools
import multiprocessing


def flatten(t):
    t = t.reshape(1, -1)
    t = t.squeeze()
    return t


# """
class Network(nn.Module):
    def __init__(self, n, m):
        super().__init__()
        # n, m = 3, 3
        width, height = 2*n+1, 2*m+1
        layer1, layer2 = 120, 60
        self.activation = F.relu
        self.fc1 = nn.Linear(in_features=width*height, out_features=layer1)
        self.fc2 = nn.Linear(in_features=layer1, out_features=layer2)
        self.out = nn.Linear(in_features=layer2, out_features=1)

    def forward(self, t):
        t = flatten(t)
        # hidden layer 1
        t = self.activation(self.fc1(t))

        # hidden layer 2
        t = self.activation(self.fc2(t))

        # output layer
        t = torch.tanh(self.out(t))
        return t
# """


class NNAI(Pencil):
    def __init__(self, name, network=None, n=3, m=3, exploration_turns=0):
        super().__init__(name)
        # self.network = network if network is not None else Network(n, m)
        self.network = Network(n, m)
        self.player_id = None  # may not be the correct way to do this
        self.exploration_turns = exploration_turns
        # self.pool = multiprocessing.Pool()
        # investigate overriding __deepcopy__, __getstate__, __setstate__

    def _evaluate(self, move, paper):
        next_state = paper.get_draw_state(move)
        # TODO _grid reference?
        next_state = torch.Tensor(next_state._grid)
        # find best value of all moves from perspective of first player
        canon_val = self.network(next_state).item()
        return paper.turn * canon_val

    def play(self, paper):
        moves = paper.possible_moves
        if self.exploration_turns > 0:
            self.exploration_turns -= 1
            return random.choice(moves)
        # super rigorous way of testing preformance
        # t0 = Timer()
        # prepare for possible parallelization
        # self.pool.close()
        # self.pool.join()
        # move_vals = self.pool.map(functools.partial(self._evaluate, paper=paper), moves)
        # https://stackoverflow.com/questions/25382455/python-notimplementederror-pool-objects-cannot-be-passed-between-processes
        # move_vals = list(map(functools.partial(self._evaluate, paper=paper), moves))
        # t1 = Timer()
        move_vals = [self._evaluate(move, paper) for move in moves]

        # print(len(move_vals))
        best_index = move_vals.index(max(move_vals))
        # t2 = Timer()
        # print(t1 - t0, t2-t1)
        return moves[best_index]


if __name__ == '__main__':
    arena_name = 'testing'
    file_path = os.path.join(Arena.BASEDIR, arena_name)
    file_path = os.path.join(file_path, "round1match1.json")
    file_path = os.path.join("..", file_path)
    with open(file_path, "r") as read_file:
        match = json.load(read_file)

    TURN = len(match["moves"]) - 1
    STATE = match["moves"][TURN]["grid"]

    # TODO this is hard coded
    network = Network(3, 4)
    print(len(STATE[0]))
    s = torch.tensor(STATE)
    print(s.type())
    s = flatten(s)
    print(s)
    print(network(s).item())
    print(network(s).item())
