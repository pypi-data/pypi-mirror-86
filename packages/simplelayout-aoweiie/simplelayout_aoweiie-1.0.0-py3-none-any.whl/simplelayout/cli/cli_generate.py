import argparse
import sys


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_grid', default=100, type=int,
                        help='布局板分辨率，代表矩形区域的边长像素数')
    parser.add_argument('--unit_grid', default=10, type=int,
                        help='矩形组件分辨率,能被布局板分辨率整除')
    parser.add_argument('--unit_n', default=3, type=int,
                        help='组件数量')
    parser.add_argument('--positions', nargs='*', default=[10, 50, 70], type=int,
                        help='组件位置')
    parser.add_argument('-o', '--outdir', default='example_dir', type=str,
                        help='输出结果的目录， 若目录不存在程序会自行创建')
    parser.add_argument('--file_name', default='example', type=str,
                        help='输出文件名（不包括文件类型后缀）')

    options = parser.parse_args()

    if (options.board_grid % options.unit_grid) != 0:
        sys.exit("组件分辨率不能整除布局板分辨率")

    if len(options.positions) != options.unit_n:
        sys.exit("组件位置和组件数量不一致")

    n_limit = (options.board_grid // options.unit_grid) ** 2
    if min(options.positions) < 1 or max(options.positions) > n_limit:
        sys.exit("组件位置超出范围")

    return options
