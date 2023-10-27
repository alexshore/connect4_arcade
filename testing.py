import numpy as np


def cell_in_grid(i, j):
    return 0 <= i < GRID_SHAPE[0] and 0 <= j < GRID_SHAPE[1]


GRID_SHAPE = (7, 6)
grid = np.full(GRID_SHAPE, 0, dtype=int)

cell = (-7, 5)

grid[cell] = 1

print(grid)
