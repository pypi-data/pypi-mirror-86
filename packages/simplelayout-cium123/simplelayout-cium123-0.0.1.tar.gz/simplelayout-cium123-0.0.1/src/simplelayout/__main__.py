# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from .cli import get_options  # TODO: 保证不修改本行也可以正确导入
from .generator.utils import save_matrix, save_fig, make_dir
from .generator.core import generate_matrix


def main():
    # TODO 使用导入的函数按命令行参数生成数据，包括 mat 文件与 jpg 文件
    args = get_options()
    matrix = generate_matrix(
        args.board_grid, args.unit_grid, args.unit_n, args.positions)
    make_dir(args.outdir)
    path = args.outdir + '/'
    save_matrix(matrix, path + args.file_name)
    save_fig(matrix, path + args.file_name)


if __name__ == "__main__":
    main()
