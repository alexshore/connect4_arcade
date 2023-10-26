import arcade
import arcade.key
from enum import Enum
from arcade.texture import cleanup_texture_cache
from arcade.tilemap.tilemap import _get_image_info_from_tileset
import numpy as np
import math

from numpy.core.arrayprint import format_float_scientific

GRID_SHAPE = (4, 4)

CELL_SIZE = 100

GRID_WIDTH = GRID_SHAPE[0] * CELL_SIZE
GRID_HEIGHT = GRID_SHAPE[1] * CELL_SIZE

CHECKER_RADIUS = 0.4 * CELL_SIZE

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
        self.grid = np.full(GRID_SHAPE, Checker.NONE)
        self.side = Checker.PRIMARY

    def switch_side(self):
        self.side = Checker(-self.side.value)

    def cell_in_grid(self, i, j):
        return 0 <= i < GRID_SHAPE[0] and 0 <= j < GRID_SHAPE[1]

    def is_drawn(self):
        return np.where(self.grid == Checker.NONE)[0].size == 0

    def is_won_diagonally(self):
        # up-right
        for i in range(-GRID_SHAPE[1] + 1, GRID_SHAPE[0]):
            count = 0

            for diag in range(GRID_SHAPE[1]):
                if not self.cell_in_grid(i + diag, diag):
                    count = 0
                    continue

                if self.grid[i + diag, diag] == self.side:
                    count += 1
                else:
                    count = 0

                if count == 4:
                    return True

        return False

    def is_won_vertically(self):
        for i in range(GRID_SHAPE[0]):
            count = 0

            for j in range(GRID_SHAPE[1]):
                if self.grid[i, j] == self.side:
                    count += 1
                else:
                    count = 0

                if count == 4:
                    return True

        return False

    def is_won_horizontally(self):
        for j in range(GRID_SHAPE[1]):
            count = 0

            for i in range(GRID_SHAPE[0]):
                if self.grid[i, j] == self.side:
                    count += 1
                else:
                    count = 0

                if count == 4:
                    return True

        return False

    def is_won(self):
        return self.is_won_vertically() or self.is_won_horizontally()

    def is_valid_move(self, column):
        return np.count_nonzero(self.grid[column] == Checker.NONE) != 0

    def make_move(self, column: int):
        if not self.is_valid_move(column):
            return

        self.grid[column][np.where(self.grid[column] == Checker.NONE)[0][0]] = self.side


class Connect4(arcade.Window):
    def __init__(self) -> None:
        super(Connect4, self).__init__(width=GRID_WIDTH, height=GRID_HEIGHT)
        arcade.set_background_color(COLORS["BACKGROUND"])

    def setup(self):
        self.game = Game()

        self.paused = False

        self.hovering = False

        self.mouse_x = 0
        self.mouse_y = 0

    def get_centre_of_cell(self, i, j):
        return (i * CELL_SIZE) + (CELL_SIZE // 2), (j * CELL_SIZE) + (CELL_SIZE // 2)

    def get_cell_from_coords(self, x, y):
        return x // CELL_SIZE, y // CELL_SIZE

    def draw_cell(self, i, j):
        x, y = self.get_centre_of_cell(i, j)
        # self.game.grid will always be an ndarray filled with Checker instances which all have a name attr
        arcade.draw_circle_filled(x, y, CHECKER_RADIUS, color=COLORS[self.game.grid[i, j].name])  # type: ignore

    def on_draw(self):
        self.clear()
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=0,
            bottom_left_y=0,
            width=GRID_WIDTH,
            height=GRID_HEIGHT,
            color=COLORS["GRID"],
        )
        for i in range(GRID_SHAPE[0]):
            for j in range(GRID_SHAPE[1]):
                self.draw_cell(i, j)

        if not self.paused and self.hovering:
            i, j = self.get_cell_from_coords(self.mouse_x, self.mouse_y)
            x, y = self.get_centre_of_cell(i, j)
            arcade.draw_circle_filled(
                center_x=x,
                center_y=y,
                radius=CHECKER_RADIUS,
                color=COLORS[self.game.side.name],
            )

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.Q:
                arcade.exit()
            case arcade.key.SPACE:
                self.setup()

    def on_mouse_enter(self, *args):
        self.hovering = True

    def on_mouse_leave(self, *args):
        self.hovering = False

    def on_mouse_motion(self, x, y, *args):
        self.hovering = True

        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, *args):
        if self.paused:
            return

        column, _ = self.get_cell_from_coords(x, y)
        self.game.make_move(column)

        if self.game.is_drawn() or self.game.is_won():
            self.paused = True

        self.game.switch_side()


def main():
    game = Connect4()
    game.setup()

    arcade.enable_timings()
    arcade.run()


if __name__ == "__main__":
    main()
