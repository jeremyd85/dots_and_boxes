from game import Paper
import torch
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
import numpy as np
import random
import os

from players.nn_ai import NNAI

# TODO: split data generation and dataset?
class DataGenArena(Dataset):
    BASEDIR = 'player_files'

    def __init__(self, player, arena_name, size=(7, 7), matches=100, data=None):
        self.player = player
        self.arena_name = arena_name
        self.rows = size[0]
        self.cols = size[1]
        self.grid_size = (2*size[0]+1) * (2*size[1]+1)
        self.round_num = 0
        self.max_game_len = 2*self.rows*self.cols + self.rows + self.cols
        self.shuffle = True  # might not be the best way or necc
        if data is None:
            self.data, self.labels = self.play_matches(matches)
        else:
            self.data, self.labels = data

    def __getitem__(self, item):
        return self.data[item], self.labels[item]

    def __len__(self):
        return len(self.labels)

    def play_match(self):
        game = Paper(self.player, self.player, self.rows, self.cols)
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
            game.update()

        if self.shuffle:
            random.shuffle(game_states)
        pad_len = 8*self.max_game_len - len(game_states)
        pad = random.sample(game_states, pad_len)
        game_states.extend(pad)
        print(len(game_states))
        game_states = np.stack(game_states)
        game_results = [game.winner()]*len(game_states)
        return game_states, game_results

    def play_matches(self, matches=100):
        print("start")
        game_states, game_results = self.play_match()
        for i in range(1, matches):
            print('game', i)
            gs, gr = self.play_match()
            game_states, game_results = np.concatenate((game_states, gs)), game_results + gr
        game_states = np.reshape(game_states, (len(game_states), self.grid_size))
        return torch.from_numpy(game_states), torch.Tensor(game_results)



size = 5, 5
nm = (2*size[0]+1) * (2*size[1]+1)
player = NNAI("NN", None, size[0], size[1], 3)
# TODO: ew ew ew why?
data = DataGenArena(player, "test_data_gen", size, 10)
data = data.data, data.labels
dataset = DataGenArena(player, "test_data_gen", size, 10, data)
print("________________________________________________________")
train_loader = DataLoader(dataset=dataset,
                          batch_size=5,
                          shuffle=True,
                          num_workers=2)

for epoch in range(2):
    for i, data in enumerate(train_loader, 0):
        # get the inputs
        inputs, labels = data

        # wrap them in Variable
        inputs, labels = Variable(inputs), Variable(labels)

        # Run your training process
        print(epoch, i, "inputs", inputs.data, "labels", labels.data)


if __name__ == '__main__':
    pass
    # size = 5, 5
    # nm = (2*size[0]+1) * (2*size[1]+1)
    # player = NNAI("NN", None, size[0], size[1], 3)
    # A = DataGenArena(player, "test_data_gen", size, 6)

    """gs, gr = A.play_matches(10)
    print(len(gs), len(gr))
    print(type(gs), type(gr))
    print(sum(gr))
    gs = np.reshape(gs, (len(gs), nm))
    print(gs.shape)"""
