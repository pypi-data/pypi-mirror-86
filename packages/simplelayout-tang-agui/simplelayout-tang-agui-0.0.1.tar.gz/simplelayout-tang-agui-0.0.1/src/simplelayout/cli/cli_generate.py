import argparse
import sys


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_grid", type=int, help="布局板分辨率")
    parser.add_argument("--unit_grid", type=int, help="矩形组件分辨率")
    parser.add_argument("--unit_n", type=int, help="组件数")
    parser.add_argument("--positions", nargs='+', type=int, help="位置")
    parser.add_argument("--outdir", default="example-dir", help="输出结果的目录")
    parser.add_argument("--file_name", default="example", help="输出文件名")

    options = parser.parse_args()
    if options.board_grid % options.unit_grid != 0:
        sys.exit("unit_grid不能被board_grid整除！")
    if (
        options.positions[0] != 1
        or len(options.positions) != options.unit_n
        or max(options.positions) >
        (options.board_grid / options.unit_grid) ** 2
    ):
        sys.exit("位置参数不符合要求！")
    return options
