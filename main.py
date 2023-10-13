import arcade
import arcade.color


SCREEN_SIZE = 720
GRID_SIZE = 100
BLOCK_SIZE = SCREEN_SIZE // GRID_SIZE


class Connect4(arcade.Window):
    def __init__(self) -> None:
        super(Connect4, self).__init__(width=SCREEN_SIZE, height=SCREEN_SIZE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
