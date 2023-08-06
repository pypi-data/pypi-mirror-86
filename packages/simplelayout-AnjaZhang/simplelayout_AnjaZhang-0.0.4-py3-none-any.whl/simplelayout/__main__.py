# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from simplelayout.cli import get_options  # TODO: 保证不修改本行也可以正确导入
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix, save_fig, make_dir


def main():
    args = get_options()
    layout_mtx = generate_matrix(
        args.board_grid, args.unit_grid, args.unit_n, args.positions
    )
    make_dir(args.outdir)
    save_matrix(layout_mtx, args.outdir + "/" + args.file_name)
    save_fig(layout_mtx, args.outdir + "/" + args.file_name)
    # raise NotImplementedError  # TODO 使用导入的函数按命令行参数生成数据，包括 mat 文件与 jpg 文件
    return None


if __name__ == "__main__":
    main()
