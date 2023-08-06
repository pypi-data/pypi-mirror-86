"""
数据生成的主要逻辑
"""


import numpy as np


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
    layout_map = np.zeros([board_grid, board_grid])
    num = board_grid // unit_grid
    for i in positions:
        i = i - 1
        left = i // num * unit_grid
        bottom = (i % num) * unit_grid
        layout_map[left:left + unit_grid, bottom : bottom + unit_grid] = np.ones([unit_grid, unit_grid])# noqa
    return layout_map
