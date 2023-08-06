# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from simplelayout.cli import get_options  # TODO: 保证不修改本行也可以正确导入
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix
from simplelayout.generator.utils import save_fig
from simplelayout.generator.utils import make_dir


def main():
    arg = get_options()
    board = generate_matrix(arg.board_grid, arg.unit_grid,
                            arg.unit_n, arg.positions)
    make_dir(arg.outdir)
    save_matrix(board, arg.outdir + '/' + arg.file_name)
    save_fig(board, arg.outdir + '/' + arg.file_name)


if __name__ == "__main__":
    main()
