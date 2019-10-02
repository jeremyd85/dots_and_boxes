from players import *
from visualizer import Visualizer
import arcade
import json
import os
from game import Arena

if __name__ == '__main__':
    rows = 7
    cols = 7
    players = []
    for i in range(20):
        if i % 2 == 0:
            player = Brute("ai{0}".format(i))
        else:
            player = BruteV3("ai{0}".format(i))
        players.append(player)


    for i in range(100):
        players = [GenericAI('player1'), GenericAI('player2')]
        arena = Arena(players, "testing", (10, 10))
        winner = arena.play_match(players[0], players[1]).get('winner')
        print(winner)
    print("Done")


    # may remove
    # file_path = os.path.join(Arena.BASEDIR, arena.arena_name)
    # file_path = os.path.join(file_path, "round1match1.json")
    # with open(file_path, "r") as read_file:
    #     match = json.load(read_file)
    # sample_game = Visualizer("round1match1", match, frame_rate=1)
    # arcade.run()


