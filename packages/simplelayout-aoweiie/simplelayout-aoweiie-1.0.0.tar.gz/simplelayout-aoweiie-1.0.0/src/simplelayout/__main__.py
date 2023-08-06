from simplelayout.generator.utils import save_matrix, save_fig, make_dir
from simplelayout.generator.core import generate_matrix
from simplelayout.cli import get_options  # TODO: 保证不修改本行也可以正确导入


def main():
    options = get_options()
    matrix = generate_matrix(options.board_grid,
                             options.unit_grid,
                             options.unit_n,
                             options.positions)
    make_dir(options.outdir)
    path = "{}/{}".format(options.outdir, options.file_name)
    save_matrix(matrix, path)
    save_fig(matrix, path)


if __name__ == "__main__":
    main()
