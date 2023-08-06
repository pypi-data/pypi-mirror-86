"""
辅助函数
"""

from pathlib import Path# noqa
import matplotlib.pyplot as plt# noqa
import scipy.io as sio# noqa


def save_matrix(matrix, file_name):
    # TODO: 存储 matrix 到 file_name.mat, mdict 的 key 为 "matrix"
    # raise NotImplementedError
    sio.savemat('%s.mat' % file_name, {'matrix': matrix})


def save_fig(matrix, file_name):
    # TODO: 将 matrix 画图保存到 file_name.jpg
    # raise NotImplementedError
    plt.imshow(matrix)
    plt.show()
    plt.imsave('%s.jpg' % file_name, matrix)


def make_dir(outdir):
    # TODO: 当目录 outdir 不存在时创建目录
    if not Path(outdir).exists():
        Path(outdir).mkdir(parents=True, exist_ok=True)
