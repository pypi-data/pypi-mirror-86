"""
数据生成的主要逻辑
"""


import numpy as np
import math


def generate_matrix(
    board_grid: int, unit_grid: int, unit_n: int, positions: list
) -> np.ndarray:

    """生成指定布局矩阵

    Args:
        board_grid (int): 布局板分辨率，代表矩形区域的边长像素数
        unit_grid (int): 矩形组件分辨率
        unit_n (int): 组件数
        positions (list): 每个元素代表每个组件的位置
    Returns:
        np.ndarray: 布局矩阵
    """
    board = np.zeros((board_grid, board_grid), dtype=int)
    unit = np.ones((unit_grid, unit_grid))
    for i in positions:
        x_start = math.ceil(i/(board_grid/unit_grid)-1) * unit_grid
        temp = int(i % (board_grid/unit_grid))-1
        if temp == -1:
            temp = int(board_grid/unit_grid)-1
        y_start = temp * unit_grid
        board[x_start:x_start+unit_grid, y_start: y_start+unit_grid] = unit

    return board
