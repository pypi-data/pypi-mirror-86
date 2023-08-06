"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    # TODO: 存储 matrix 到 file_name.mat, mdict 的 key 为 "matrix"
    sio.savemat(file_name + ".mat", {"matrix": matrix})
    return None


def save_fig(matrix, file_name):
    # TODO: 将 matrix 画图保存到 file_name.jpg
    plt.imshow(matrix, aspect="equal")
    plt.axis("off")
    plt.savefig(file_name + ".jpg", bbox_inches="tight", pad_inches=0.0)
    return None


def make_dir(outdir):
    # TODO: 当目录 outdir 不存在时创建目录
    p = Path(outdir)
    p.mkdir(exist_ok=True, parents=True)
    return None
