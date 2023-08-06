"""
数据生成的主要逻辑
"""


import numpy as np


def generate_matrix(
    board_grid: int, unit_grid: int, unit_n: int, positions: list
) -> np.ndarray:
    x = np.zeros([board_grid, board_grid])
    for i in positions:
        cols = ((i - 1) % int(board_grid / unit_grid)) * unit_grid
        rows = ((i - 1) // int(board_grid / unit_grid)) * unit_grid
        x[rows:rows + unit_grid, cols:cols + unit_grid] = 1
    return x
