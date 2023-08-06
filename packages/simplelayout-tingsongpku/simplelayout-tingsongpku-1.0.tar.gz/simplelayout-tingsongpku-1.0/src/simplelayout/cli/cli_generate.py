import argparse
import os


def get_options():
    parser = argparse.ArgumentParser()
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser.add_argument("-b", "--board_grid", type=int, help="board_length")
    parser.add_argument("-u", "--unit_grid", type=int, help="unit_length")
    parser.add_argument("--unit_n", type=int, help="unit numbers")
    parser.add_argument("--positions", nargs='+', type=int)  # nargs='+'
    parser.add_argument("-o", "--outdir", type=str, default="example_dir")
    parser.add_argument("--file_name", type=str, default="example")
    args = parser.parse_args()
    if args.board_grid % args.unit_grid != 0:
        print("mod error")
        # exit()
    #  positions = args.positions[:-1].split(' ')  # --positions 1 4
    print(args.positions)
    if len(args.positions) != args.unit_n:
        print("grid numbers error")
        # exit()
    else:
        for pos in args.positions:
            if int(pos) >= int(args.board_grid/args.unit_grid) ** 2:
                print("too large, error")
                print(pos, int(args.board_grid/args.unit_grid) ** 2)
                # exit()
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    return args
