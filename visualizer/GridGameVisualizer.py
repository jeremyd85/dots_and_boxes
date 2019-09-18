"""
Visualiser
Based off arcade template
"""
import arcade
import json


SCREEN_TITLE = "Vis"
# may need to treat different kinds of cells differently
STATE_TO_COLOR = {-1: arcade.color.RED,
                  0: arcade.color.WHITE,
                  1: arcade.color.BLUE}
"""
                  2: arcade.color.GREEN,
                  3: arcade.color.BLUE,
                  4: arcade.color.PURPLE,
                  5: arcade.color.PINK,
                  6: arcade.color.GRAY,
                  7: arcade.color.BLACK}"""
# not used yet
CELL_TYPE = {"OO": 0,
             "OE": 1,
             "EO": 2,
             "EE": 3}

OUTSIDE_MARGIN = 50
CELL_MARGIN = 6

LITTLE_LENGTH = 8
BIG_LENGTH = 30


class Visualizer(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, n, m, title, match=None, human=False):
        self.num_cells_across = 2*m+1
        self.num_cells_down = 2*n+1
        width = 2 * OUTSIDE_MARGIN + self.index_to_offset_from_outside_margin_to_corner(self.num_cells_across)
        height = 2 * OUTSIDE_MARGIN + self.index_to_offset_from_outside_margin_to_corner(self.num_cells_down)
        super().__init__(width, height, title)
        # move to setup

        self.match = match
        self.turn = 0
        self.frame_count = 0
        self.update_rate = 120
        self.shape_list = None
        self.grid = [[0 for _ in range(self.num_cells_across)]
                     for _ in range(self.num_cells_down)]
        # could remove and just calc as needed
        self.cell_position = [[tuple(map(self.index_to_offset_from_outside_margin_to_corner, (x, y)))
                               for y in range(self.num_cells_across)]
                              for x in range(self.num_cells_down)]
        self.cell_size = None
        self.fill_shape_list()

        arcade.set_background_color(arcade.color.AMAZON)

    def fill_shape_list(self):
        self.shape_list = arcade.ShapeElementList()
        for row in range(self.num_cells_down):
            for column in range(self.num_cells_across):
                color = STATE_TO_COLOR[self.grid[row][column]]
                # using two different styles to do two similar things, should choose one style?
                width, height = self.index_to_length(row), self.index_to_length(column)
                # width, height = height, width
                x, y = self.cell_position[row][column]
                x, y = x + OUTSIDE_MARGIN, y + OUTSIDE_MARGIN
                current_rect = arcade.create_rectangle_filled(x+(width//2), y+(height//2), width, height, color)
                self.shape_list.append(current_rect)

    @staticmethod
    def index_to_offset_from_outside_margin_to_corner(index):
        a, b = (index+1)//2, index//2
        return a * LITTLE_LENGTH + b * BIG_LENGTH + index * CELL_MARGIN

    @staticmethod
    def index_to_length(index):
        return LITTLE_LENGTH if (index % 2) == 0 else BIG_LENGTH

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.shape_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # ew frame based logic
        self.frame_count += 1
        if self.frame_count % 10 == 0 and self.turn < 4:
            self.turn += 1
            self.grid = self.match["moves"][self.turn-1]["grid"]
        self.fill_shape_list()


def main():
    """ Main method """
    with open("test.json", "r") as read_file:
        match = json.load(read_file)
    game = Visualizer(1, 1, SCREEN_TITLE, match)
    game.fill_shape_list()
    arcade.run()


if __name__ == "__main__":
    main()
