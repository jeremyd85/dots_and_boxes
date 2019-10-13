from players import *
from players.nn_ai import NNAI
from visualizer import Visualizer
import arcade
import json
import os
from game import Arena

if __name__ == '__main__':
    rows = 4
    cols = 5
    players = [NNAI('NN0', n=rows, m=cols), NNAI('NN1', n=rows, m=cols)]
    players = [Brute('B'), NNAI('NN1', n=rows, m=cols)]
    players = players[::-1]

    # players = [Brute('Brute0'), Brute('Brute1')]

    arena = Arena(players, "testing", (rows, cols))
    r = arena.create_round()
    arena.play_round(r)

    # may remove
    file_path = os.path.join(Arena.BASEDIR, arena.arena_name)
    file_path = os.path.join(file_path, "round1match1.json")
    with open(file_path, "r") as read_file:
        match = json.load(read_file)
    sample_game = Visualizer("round1match1", match, frame_rate=1)
    # print(len(sample_game.match["moves"]))
    arcade.run()


