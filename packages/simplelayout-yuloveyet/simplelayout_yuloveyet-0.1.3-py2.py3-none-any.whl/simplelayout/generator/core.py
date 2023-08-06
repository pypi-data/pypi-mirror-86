"""
数据生成的主要逻辑
"""


import numpy as np


def generate_matrix(
    board_grid: int, unit_grid: int, unit_n: int, positions: list
):
    matrix_samples = np.zeros((board_grid, board_grid), dtype=int)
    centre = np.zeros((unit_n, 2), dtype=int)
    size = int(unit_grid/2)
    nums = board_grid/unit_grid
    for k in range(unit_n):
        # position : 1 to nums
        ly = np.mod(positions[k]-1, nums)*unit_grid+size
        lx = np.floor((positions[k]-1)/nums)*unit_grid+size
        centre[k, :] = [lx, ly]
        for i in range(centre[k, 0]-size+1,
                       centre[k, 0]+size+1, 1):
            for j in range(centre[k, 1]-size+1,
                           centre[k, 1]+size+1, 1):
                # ! from left to right firstly, then top to bottom
                matrix_samples[i-1, j-1] = 1

    return matrix_samples
    """生成指定布局矩阵
-> np.ndarray
    Args:
        board_grid (int): 布局板分辨率，代表矩形区域的边长像素数
        unit_grid (int): 矩形组件分辨率
        unit_n (int): 组件数
        positions (list): 每个元素代表每个组件的位置
    Returns:
        np.ndarray: 布局矩阵
    """

    raise NotImplementedError  # TODO: 实现布局矩阵的生成
