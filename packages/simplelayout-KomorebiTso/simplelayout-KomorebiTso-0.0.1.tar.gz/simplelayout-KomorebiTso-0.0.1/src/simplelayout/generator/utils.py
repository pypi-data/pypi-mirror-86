"""
辅助函数
"""

from pathlib import Path# noqa
import matplotlib.pyplot as plt# noqa
import scipy.io as sio# noqa


def save_matrix(matrix, file_name):
    sio.savemat('%s.mat' % file_name, {'matrix': matrix})


def save_fig(matrix, file_name):
    plt.show()
    plt.imsave('%s.jpg' % file_name, matrix)


def make_dir(outdir):
    if not Path(outdir).exists():
        Path(outdir).mkdir(parents=True, exist_ok=True)
