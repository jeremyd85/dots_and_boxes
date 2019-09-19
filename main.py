from players import *
from visualizer import Visualizer
import arcade
import json
import os
from game import Arena

if __name__ == '__main__':
    rows = 3
    cols = 4
    players = [Brute("Jeremy"), Brute('Steve')]

    arena = Arena(players, "testing", (rows, cols))
    r = arena.create_round()
    arena.play_round(r)

    # may remove
    file_path = os.path.join(Arena.BASEDIR, arena.arena_name)
    file_path = os.path.join(file_path, "round1match1.json")
    with open(file_path, "r") as read_file:
        match = json.load(read_file)
    sample_game = Visualizer("round1match1", match, frame_rate=1)
    arcade.run()


