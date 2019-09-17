from paper import Paper
from jeremy_ai import DestroyerOfJesse


def main():
    width = 5
    height = 5
    p1 = DestroyerOfJesse('AI1', 0)
    p2 = DestroyerOfJesse('AI2', 0)
    game = Paper(p1, p2, width, height)
    while game.take_turn() is None:
        print(game.grid)

    if game.winner() == -1:
        print(game.player1.name)
    else:
        print(game.player2.name)

main()