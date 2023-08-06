"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    # TODO: 存储 matrix 到 file_name.mat, mdict 的 key 为 "matrix"
    # save_name = Path(outdir, file_name+'.mat')
    save_name = Path(file_name+'.mat')
    sio.savemat(save_name, mdict={"matrix": matrix})
    # raise NotImplementedError


def save_fig(matrix, file_name):
    # TODO: 将 matrix 画图保存到 file_name.jpg
    fig = plt.figure(figsize=(3, 3), dpi=300)
    plt.imshow(matrix, cmap='Blues')
    plt.axis('equal')
    plt.axis('off')
    plt.title('simple_layout')
    # plt.show(im)

    # save_name = Path(outdir, file_name+'.jpg')
    save_name = file_name+'.jpg'
    fig.savefig(save_name, dpi=300)
    plt.close()
    # raise NotImplementedError


def make_dir(outdir):
    # TODO: 当目录 outdir 不存在时创建目录
    if not Path(outdir).exists():
        Path(outdir).mkdir(parents=True, exist_ok=True)
    # raise NotImplementedError
