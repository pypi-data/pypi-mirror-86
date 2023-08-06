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
    layout_mtx = np.zeros((board_grid, board_grid))
    unit_n_total = board_grid / unit_grid
    assert board_grid % unit_grid == 0, "布局板分辨率需被组件分辨率整除!"
    assert len(positions) == unit_n, "组件数与给定位置不一致！"
    assert (int(max(positions)) <= unit_n_total ** 2) and (
        int(min(positions) >= 1)
    ), "给定位置范围不对！"
    for pos in positions:
        pos_r = math.floor((pos - 1) / unit_n_total)
        pos_c = (pos - 1) % unit_n_total
        layout_mtx[
            int(pos_r * unit_n_total):int((pos_r + 1) * unit_n_total),
            int(pos_c * unit_n_total):int((pos_c + 1) * unit_n_total),
        ] = 1
    return layout_mtx  # TODO: 实现布局矩阵的生成
