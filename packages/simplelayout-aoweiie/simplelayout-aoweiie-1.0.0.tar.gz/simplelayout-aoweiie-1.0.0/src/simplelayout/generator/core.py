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

    unit_len = board_grid // unit_grid
    board_unit = np.zeros((unit_len * unit_len,))  # 压缩布局先用一维向量表示
    positions = [x-1 for x in positions]  # 原来位置从1开始，转成从0开始
    board_unit[positions] = 1
    board_unit = board_unit.reshape(unit_len, unit_len)  # 把布局reshape成方形

    unit = np.ones((unit_grid, unit_grid))  # 单个组件
    return np.kron(board_unit, unit)
