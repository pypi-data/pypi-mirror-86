"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    mdict = {'matrix': matrix}
    sio.savemat(file_name+'.mat', mdict)


def save_fig(matrix, file_name):
    plt.imsave(file_name+'.jpg', matrix, cmap='gray')


def make_dir(outdir):
    path = Path(outdir)
    path.mkdir(parents=True, exist_ok=True)
