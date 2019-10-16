from players import *
from visualizer import Visualizer
import arcade
import json
import os
from game import Arena

from timeit import default_timer as Timer

if __name__ == '__main__':
    rows = 7
    cols = 7
    players = [NNAI('NN0', n=rows, m=cols), NNAI('NN1', n=rows, m=cols)]
    players = [GenericAI('1_generic'), NNAI('-1_nn', n=rows, m=cols, exploration_turns=3)]
    # players = players[::-1]

    # players = [Brute('Brute0'), Brute('Brute1')]

    arena = Arena(players, "testing", (rows, cols))
    r = arena.create_round()

    # super rigorous way of testing preformance
    t0 = Timer()
    arena.play_round(r)
    t1 = Timer()
    print(t1 - t0)

    # may remove
    file_path = os.path.join(Arena.BASEDIR, arena.arena_name)
    file_path = os.path.join(file_path, "round1match1.json")
    with open(file_path, "r") as read_file:
        match = json.load(read_file)
    sample_game = Visualizer("round1match1", match, frame_rate=8)
    # print(len(sample_game.match["moves"]))
    arcade.run()


