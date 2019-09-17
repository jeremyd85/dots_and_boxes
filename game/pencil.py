
class Pencil:
    """
    This is the player class for our game. It is called Pencil because this is a pencil and paper game... HA!
    If you make an AI to play this game, you need to inherit this class and make your AI. All AI's must have a name,
    and be capable of playing the game... That is why those are the only things in this base class.

    play is the entry point for your AI. paper is your copy of the Paper object that called it. You can do anything to
    this paper object without effecting the actual game. You are given this object so that you can have all the game
    information.

    Useful functions from paper (Look at paper.py for more detailed docs):
        get_possible_moves(): returns a list of all possible moves as a tuples, (row, col) on the grid.
        ^ If your move isn't in this list, you will break the game... Don't break the game

        Conditionals (useful when looking directly at paper.grid):
            is_valid(coord)
            is_player_spot(coord)
            is_wall_spot(coord)
            is_empty(coord)

        get_adjacents(coord): returns a list of coordinates around the coordinate in the parameter.

        draw(coord):

        get_draw_state(coord):

    """

    def __init__(self, name):
        self.name = name

    def play(self, paper):
        return paper.get_possible_moves()[0]

