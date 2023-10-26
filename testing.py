GRID_SHAPE = (7, 6)


print("\n")
for i in range(GRID_SHAPE[1] - 1, -1, -1):
    print("|", end="")
    for j in range(-GRID_SHAPE[0] + 1, GRID_SHAPE[0]):
        print(f" {j},{i} |", end="")
    print("\n")


def cell_in_grid(i, j):
    return 0 <= i < GRID_SHAPE[0] and 0 <= j < GRID_SHAPE[1]


print(cell_in_grid(0, 0))
print(cell_in_grid(6, 5))
print(cell_in_grid(6, 7))
print(cell_in_grid(7, 7))
print(cell_in_grid(-5, 0))
print(cell_in_grid(8, 0))
