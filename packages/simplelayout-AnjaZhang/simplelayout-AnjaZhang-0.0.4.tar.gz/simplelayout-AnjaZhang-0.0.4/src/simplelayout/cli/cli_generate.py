import argparse


def get_options():
    parser = argparse.ArgumentParser()
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser.add_argument("--board_grid", type=int, help="layout pixel")
    parser.add_argument("--unit_grid", type=int, help="rectangle pixel")
    parser.add_argument("--unit_n", type=int, help="number of rectangles")
    parser.add_argument(
        "--positions", nargs="+", type=int, help="positions of rectangles"
    )
    parser.add_argument(
        "-o",
        "--outdir",
        type=str,
        default="example_dir1/example_dir2",
        help="rectangle point order number",
    )
    parser.add_argument(
        "--file_name", type=str, default="example", help="saved file name"
    )
    options = parser.parse_args()
    return options
