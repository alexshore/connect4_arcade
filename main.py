import arcade
import arcade.key
from enum import Enum
import numpy as np

GRID_SIZE = 700
CELL_COUNT = 7
CELL_SIZE = GRID_SIZE // CELL_COUNT
CHECKER_RADIUS = 0.4 * CELL_SIZE
BORDER_SIZE = 20

COLORS = {
    "GRID": arcade.color_from_hex_string("393E41"),
    "BACKGROUND": arcade.color_from_hex_string("F6F7EB"),
    "PRIMARY": arcade.color_from_hex_string("3F88C5"),
    "SECONDARY": arcade.color_from_hex_string("EB5D47"),
    "NONE": arcade.color_from_hex_string("7C878D"),
}


class Checker(Enum):
    NONE = 0
    PRIMARY = -1
    SECONDARY = 1


class Game:
    def __init__(self):
        self.grid = np.full((CELL_COUNT, CELL_COUNT), Checker.NONE)
        self.side = Checker.PRIMARY

    def switch_side(self):
        self.side = Checker(-self.side.value)

    def is_drawn(self):
        return np.where(self.grid == Checker.NONE)[0].size == 0

    def is_won(self):
        return False

    def is_valid_move(self, column):
        return np.count_nonzero(self.grid[column] == Checker.NONE) != 0

    def make_move(self, column: int, color: Checker):
        if not self.is_valid_move(column):
            return

        self.grid[column][np.where(self.grid[column] == Checker.NONE)[0][0]] = Checker(color.value)


class Connect4(arcade.Window):
    def __init__(self) -> None:
        super(Connect4, self).__init__(width=GRID_SIZE + BORDER_SIZE, height=GRID_SIZE + BORDER_SIZE)
        arcade.set_background_color(COLORS["BACKGROUND"])

    def setup(self):
        self.game = Game()

    def get_coords_of_cell(self, i, j):
        return (
            (i * CELL_SIZE) + (CELL_SIZE // 2) + (BORDER_SIZE // 2),
            (j * CELL_SIZE) + (CELL_SIZE // 2) + (BORDER_SIZE // 2),
        )

    def draw_cell(self, i, j):
        x, y = self.get_coords_of_cell(i, j)
        # self.game.grid will always be an ndarray filled with Checker instances which all have a name attr
        arcade.draw_circle_filled(x, y, CHECKER_RADIUS, color=COLORS[self.game.grid[i, j].name])  # type: ignore

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(
            center_x=BORDER_SIZE // 2 + GRID_SIZE // 2,
            center_y=BORDER_SIZE // 2 + GRID_SIZE // 2,
            width=GRID_SIZE,
            height=GRID_SIZE,
            color=COLORS["GRID"],
        )
        for i in range(CELL_COUNT):
            for j in range(CELL_COUNT):
                self.draw_cell(i, j)

    def on_update(self, delta_time):
        # TODO: figure out if I even need this??? this isn't a game based on updates over frames
        #       only thing coming to mind rn is attempt to make the checkers actually _fall_ but
        #       that seems super complicated esp. with how the grid is currently drawn
        ...

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.Q:
                arcade.exit()

    def on_mouse_motion(self, x, y, *args):
        # TODO: slightly translucent checker placed if mouse is in a specific section
        #         could make it so it only works inside a circle. but would require
        #         a slightly more complex calculation to figure the bounds for each
        #         circle
        ...

    def on_mouse_press(self, x, y, button, *args):
        # TODO: make a move based on mouse position
        ...


def main():
    game = Connect4()
    game.setup()

    arcade.enable_timings()
    arcade.run()


if __name__ == "__main__":
    main()
