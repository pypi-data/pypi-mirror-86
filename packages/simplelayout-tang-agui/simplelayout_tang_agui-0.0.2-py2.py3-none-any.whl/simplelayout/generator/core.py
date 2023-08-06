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
    block_num = int(board_grid / unit_grid)
    random_matrix_block = np.zeros((block_num, block_num))
    random_matrix_reshape = random_matrix_block.reshape(1, -1)
    for i in range(unit_n):
        random_matrix_reshape[0, positions[i] - 1] = 1
    random_matrix_reverse = random_matrix_reshape.reshape(block_num, block_num)

    random_matrix = np.kron(random_matrix_reverse,
                            np.ones((unit_grid, unit_grid)))
    # random_matrix = np.zeros((board_grid, board_grid))
    # temp = (board_grid / unit_grid)
    # for i in range(unit_n):
    #     temp_x = int((positions[i] - 1) // temp * temp)
    #     temp_y = int((positions[i] - 1) % temp * temp)
    #     random_matrix[temp_x:temp_x + unit_grid,
    #                   temp_y:temp_y + unit_grid] = 1
    return random_matrix
