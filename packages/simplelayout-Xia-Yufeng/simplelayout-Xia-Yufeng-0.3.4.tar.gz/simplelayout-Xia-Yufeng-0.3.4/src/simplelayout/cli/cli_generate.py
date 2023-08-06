import argparse


def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument('--board_grid', type=int, help='board_grid')
    parser.add_argument('--unit_grid', type=int, help='unit_grid')
    parser.add_argument('--unit_n', type=int, help='unit_n')
    parser.add_argument('--positions', type=int, nargs='+', help='positions')
    parser.add_argument('--outdir', type=str, help='outdir')
    parser.add_argument('--file_name', type=str, help='file_name')

    options = parser.parse_args()
    return options
