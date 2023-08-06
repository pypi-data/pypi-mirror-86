import numpy as np


def generate_matrix(
    board_grid: int, unit_grid: int, unit_n: int, positions: list
) -> np.ndarray:

    matrix = np.zeros([board_grid, board_grid])
    num = board_grid // unit_grid
    for i in positions:
        row = (i-1)//num * unit_grid
        lin = ((i-1) % (num)) * unit_grid
        matrix[row:row+unit_grid, lin:lin +
               unit_grid] = np.ones([unit_grid, unit_grid])
    return matrix
