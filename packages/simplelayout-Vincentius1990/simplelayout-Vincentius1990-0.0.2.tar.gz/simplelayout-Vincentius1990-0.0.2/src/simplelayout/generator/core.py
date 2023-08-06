"""
数据生成的主要逻辑
"""

import numpy as np
import matplotlib.pyplot as plt


def generate_matrix(
    board_grid: int, unit_grid: int, unit_n: int, positions: list
) -> np.ndarray:
    matrix = np.zeros((board_grid, board_grid))
    for item in positions:
        board_unit_n = board_grid/unit_grid
        if item % board_unit_n == 0:
            row_n = int(item/board_unit_n - 1)
            column_n = board_unit_n - 1
        else:
            row_n = int(item/board_unit_n)
            column_n = int(item % board_unit_n - 1)
        print(row_n, column_n)
        row_begin = int(row_n*unit_grid)
        column_begin = int(column_n*unit_grid)
        print(row_begin, row_begin + unit_grid,
              column_begin, column_begin + unit_grid)
        matrix[row_begin:row_begin + unit_grid,
               column_begin:column_begin + unit_grid] = 1
    plt.imshow(matrix)
    plt.savefig('matrix')
    return matrix

    """生成指定布局矩阵

    Args:
        board_grid (int): 布局板分辨率，代表矩形区域的边长像素数
        unit_grid (int): 矩形组件分辨率
        unit_n (int): 组件数
        positions (list): 每个元素代表每个组件的位置
    Returns:
        np.ndarray: 布局矩阵
    """
    # raise NotImplementedError  # TODO: 实现布局矩阵的生成
