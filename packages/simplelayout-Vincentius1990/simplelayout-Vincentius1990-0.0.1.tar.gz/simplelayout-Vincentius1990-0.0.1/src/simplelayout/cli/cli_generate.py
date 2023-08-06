import argparse
import sys


def get_options():
    parser = argparse.ArgumentParser()
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser.add_argument("--board_grid", type=int,
                        help="the board_grid")
    parser.add_argument("--unit_grid", type=int,
                        help="the unit_grid")
    parser.add_argument("--unit_n", type=int,
                        help="the number_of_unit")
    parser.add_argument("--positions", type=int, nargs='+',
                        help="the positions")
    parser.add_argument("-o", "--outdir", type=str, default='/example_dir',
                        help="the outdir")
    parser.add_argument("--file_name", type=str, default='example',
                        help="the file_name")
    options = parser.parse_args()
    n = options.board_grid/options.unit_grid
    if options.board_grid % options.unit_grid != 0:
        sys.exit('不能整除')
    elif len(options.positions) != options.unit_n:
        sys.exit('组件数量错误')
    elif min(options.positions) < 1 | max(options.positions) > n**2:
        sys.exit('组件编号超出范围')
    else:
        return options
