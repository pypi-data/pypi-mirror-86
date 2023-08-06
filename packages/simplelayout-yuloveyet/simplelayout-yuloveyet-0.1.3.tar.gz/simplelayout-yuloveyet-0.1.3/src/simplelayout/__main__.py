# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from simplelayout.cli import get_options  # TODO: 保证不修改本行也可以正确导入
from simplelayout.generator import save_matrix, save_fig, make_dir
from simplelayout.generator import generate_matrix


def main():
    args = get_options()
    matrix = generate_matrix(
        args.board_grid, args.unit_grid, args.unit_n, args.positions)
    make_dir(args.outdir)
    # use '/' to seperate the path and name
    file_name = args.outdir + '/'+args.file_name
    save_matrix(matrix, file_name)
    save_fig(matrix, file_name)

    # raise NotImplementedError  # TODO 使用导入的函数按命令行参数生成数据，包括 mat 文件与 jpg 文件


if __name__ == "__main__":
    main()
