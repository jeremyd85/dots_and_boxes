"""
Visualiser
Based off arcade template
"""
import arcade
import json
import os
from game import Arena

SCREEN_TITLE = "Vis"
# may need to treat different kinds of cells differently
STATE_TO_COLOR = {-1: arcade.color.RED,
                  0: arcade.color.WHITE,
                  1: arcade.color.BLUE}
""",
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
    Visualizer Doc
    """

    def __init__(self, title, match=None, human=False, frame_rate=4):
        self.num_cells_down = 2 * match['size'][0] + 1
        self.num_cells_across = 2 * match['size'][1] + 1
        width = 2 * OUTSIDE_MARGIN + self.index_to_offset_from_outside_margin_to_corner(self.num_cells_across)
        height = 2 * OUTSIDE_MARGIN + self.index_to_offset_from_outside_margin_to_corner(self.num_cells_down)
        super().__init__(width, height, title)
        # move to setup

        self.frame_rate = frame_rate
        self.match = match
        self.turn = 0
        self.frame_count = 0
        self.update_rate = 120
        self.shape_list = None
        self.grid = [[0 for _ in range(self.num_cells_across)]
                     for _ in range(self.num_cells_down)]
        # could remove and just calc as needed
        self.cell_position = [[tuple(map(self.index_to_offset_from_outside_margin_to_corner, (x, y)))
                               for x in range(self.num_cells_across)]
                              for y in range(self.num_cells_down)]
        self.cell_size = None
        self.fill_shape_list()

        arcade.set_background_color(arcade.color.AMAZON)

    def fill_shape_list(self):
        self.shape_list = arcade.ShapeElementList()
        for row in range(self.num_cells_down):
            for column in range(self.num_cells_across):
                color = STATE_TO_COLOR[self.grid[row][column]]
                # using two different styles to do two similar things, should choose one style?
                height, width = self.index_to_length(row), self.index_to_length(column)

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
        if self.frame_count % self.frame_rate == 0 and self.turn < len(self.match["moves"]):
            self.turn += 1
            self.grid = self.match["moves"][self.turn-1]["grid"]
        self.fill_shape_list()


if __name__ == "__main__":
    arena_name = 'testing'
    arena_dir = os.path.join(Arena.BASEDIR, arena_name)
    if not os.path.exists(arena_dir):
        raise FileNotFoundError
    matches = os.listdir(arena_dir)
    # TODO support tournament in visualizer (stops after one match w/ error on close)
    ma = matches[0]
    match_path = os.path.join(arena_dir, ma)
    with open(match_path, "r") as read_file:
        match = json.load(read_file)
    game = Visualizer(SCREEN_TITLE, match, frame_rate=1)
    game.fill_shape_list()
    arcade.run()
    arcade.close_window()