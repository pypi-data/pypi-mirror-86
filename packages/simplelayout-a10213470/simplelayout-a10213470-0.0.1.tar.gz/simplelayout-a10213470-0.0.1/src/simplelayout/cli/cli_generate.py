import argparse
import sys


def get_options():
    parser = argparse.ArgumentParser()
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_grid", type=int)
    parser.add_argument("--unit_grid", type=int)
    parser.add_argument("--unit_n", type=int)
    parser.add_argument("--positions", type=int, nargs='+')
    parser.add_argument("--outdir", default='example_dir', type=str)
    parser.add_argument("--file_name", default='file_name', type=str)
    args = parser.parse_args()
    if args.board_grid % args.unit_grid != 0:
        sys.exit()
    if len(args.positions) != args.unit_n:
        sys.exit()
    for i in args.positions:
        if i < 1 or i > (args.board_grid/args.unit_grid)**2:
            sys.exit()
    options = parser.parse_args()
    return options
