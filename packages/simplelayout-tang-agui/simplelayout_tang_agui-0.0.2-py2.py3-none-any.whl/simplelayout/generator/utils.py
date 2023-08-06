"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    mdic = {"matrix": matrix}
    sio.savemat(file_name + '.mat', mdic)


def save_fig(matrix, file_name):
    plt.imshow(matrix)
    plt.savefig(file_name + '.jpg')
    # plt.show()


def make_dir(outdir):
    path = Path(outdir)
    # if not path.exists():
    path.mkdir(parents=True, exist_ok=True)
