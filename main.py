import arcade
from enum import Enum
import numpy as np


GRID_SHAPE = (7, 6)
CELL_SIZE = 100
GRID_WIDTH = GRID_SHAPE[0] * CELL_SIZE
GRID_HEIGHT = GRID_SHAPE[1] * CELL_SIZE
CHECKER_RADIUS = 0.4 * CELL_SIZE


class Checker(Enum):
    NONE = 0
    PRIMARY = -1
    SECONDARY = 1


COLORS = {
    Checker.PRIMARY: (63, 136, 197),
    Checker.SECONDARY: (235, 93, 71),
    Checker.NONE: (124, 135, 141),
}

"""
thoughts:
    - could have just used one class, didn't really need to separate game and board logic though it does allow for easy instant resetting
    - couple functions i don't really like:
        - is_won_diagonally (could be made far more efficient i.e. not looping as many times by reducing start cell possibilities)
        - make_move (uses hard to follow functions with unclear returns to make the move, fix in TODO)
    - need to actually add something saying the game is won/drawn
    - could be interesting to also add a minmax algorithm driven opponent
        - points? obv points to win but also points for a threat of a win? 
        - should create a positions dict so not to calculate the same position multiple times
        - prune any branches that instantly give the opponent a win
"""


class Game:
    def __init__(self):
        self.grid = np.full(GRID_SHAPE, Checker.NONE)
        self.side = Checker.PRIMARY

    def switch_side(self) -> None:
        self.side = Checker(-self.side.value)

    def is_cell_in_grid(self, cell: tuple[int, int]) -> bool:
        return 0 <= cell[0] < GRID_SHAPE[0] and 0 <= cell[1] < GRID_SHAPE[1]

    def is_drawn(self) -> bool:
        return np.where(self.grid == Checker.NONE)[0].size == 0

    def is_won_diagonally(self) -> bool:
        # up-right
        for i in range(-GRID_SHAPE[1], GRID_SHAPE[0]):
            count = 0

            for offset in range(GRID_SHAPE[1]):
                if not self.is_cell_in_grid(cell=(i + offset, offset)):
                    count = 0
                    continue

                if self.grid[i + offset, offset] == self.side:
                    count += 1
                else:
                    count = 0

                if count == 4:
                    return True

        # up-left
        for i in range(GRID_SHAPE[0] + GRID_SHAPE[1], -1, -1):
            count = 0

            for offset in range(GRID_SHAPE[1]):
                if not self.is_cell_in_grid(cell=(i - offset, offset)):
                    count = 0
                    continue

                if self.grid[i - offset, offset] == self.side:
                    count += 1
                else:
                    count = 0

                if count == 4:
                    return True

        return False

    def is_won_vertically(self) -> bool:
        for i in range(GRID_SHAPE[0]):
            count = 0

            for offset in range(GRID_SHAPE[1]):
                if self.grid[i, offset] == self.side:
                    count += 1
                else:
                    count = 0

                if count == 4:
                    return True

        return False

    def is_won_horizontally(self) -> bool:
        for j in range(GRID_SHAPE[1]):
            count = 0

            for offset in range(GRID_SHAPE[0]):
                if self.grid[offset, j] == self.side:
                    count += 1
                else:
                    count = 0

                if count == 4:
                    return True

        return False

    def is_won(self) -> bool:
        return self.is_won_horizontally() or self.is_won_vertically() or self.is_won_diagonally()

    def is_valid_move(self, column: int) -> bool:
        # checks for at least 1 cell with a Checker.NONE in it
        return np.count_nonzero(self.grid[column] == Checker.NONE) != 0

    def make_move(self, column: int) -> None:
        if not self.is_valid_move(column):
            return

        # this works really well but is also completely unreadable if you don't know how the np.where() func works
        #   and even if you do know how it works its still not great.
        # TODO: replace with a simple readable loop checking for first empty space
        self.grid[column][np.where(self.grid[column] == Checker.NONE)[0][0]] = self.side


class Connect4(arcade.Window):
    def __init__(self) -> None:
        super(Connect4, self).__init__(width=GRID_WIDTH, height=GRID_HEIGHT)
        arcade.set_background_color((57, 62, 65))

    def setup(self) -> None:
        self.game = Game()

        self.paused = False
        self.mouse_x = 0
        self.mouse_y = 0

    # --- overloaded methods ---

    def on_draw(self) -> None:
        self.clear()
        for i in range(GRID_SHAPE[0]):
            for j in range(GRID_SHAPE[1]):
                self.draw_checker(cell=(i, j))

        if not self.paused:
            self.draw_mouse_hover()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.Q:
                arcade.exit()
            case arcade.key.SPACE:
                self.setup()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if self.paused or button != arcade.MOUSE_BUTTON_LEFT:
            return

        column, _ = self.get_cell_of_mouse()
        self.game.make_move(column)

        if self.game.is_drawn() or self.game.is_won():
            self.paused = True

        self.game.switch_side()

    # --- custom methods ---

    def get_cell_of_mouse(self) -> tuple[int, int]:
        return self.mouse_x // CELL_SIZE, self.mouse_y // CELL_SIZE

    def get_centre_of_cell(self, cell: tuple[int, int]) -> tuple[int, int]:
        return (cell[0] * CELL_SIZE) + (CELL_SIZE // 2), (cell[1] * CELL_SIZE) + (CELL_SIZE // 2)

    def is_mouse_inside_checker(self, center_x: int, center_y: int) -> bool:
        # check if distance from center of circle to mouse (using pythag) is less than radius
        # https://math.stackexchange.com/questions/198764/how-to-know-if-a-point-is-inside-a-circle
        return (self.mouse_x - center_x) ** 2 + (self.mouse_y - center_y) ** 2 <= CHECKER_RADIUS**2

    def draw_checker(self, cell: tuple[int, int]) -> None:
        center_x, center_y = self.get_centre_of_cell(cell)
        arcade.draw_circle_filled(
            center_x=center_x,
            center_y=center_y,
            radius=CHECKER_RADIUS,
            color=COLORS[self.game.grid[cell]],
        )

    def draw_mouse_hover(self) -> None:
        cell = self.get_cell_of_mouse()

        if not self.game.is_cell_in_grid(cell):
            return

        if self.game.grid[cell] is not Checker.NONE:
            return

        center_x, center_y = self.get_centre_of_cell(cell)

        if not self.is_mouse_inside_checker(center_x, center_y):
            return

        arcade.draw_circle_filled(
            center_x=center_x,
            center_y=center_y,
            radius=CHECKER_RADIUS,
            color=(*COLORS[self.game.side], 160),
        )


def main() -> None:
    game = Connect4()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
