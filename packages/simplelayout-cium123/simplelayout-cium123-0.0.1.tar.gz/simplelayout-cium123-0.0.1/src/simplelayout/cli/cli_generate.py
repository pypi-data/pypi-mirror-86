import argparse


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--board_grid', help="Layout_panel_resolution", type=int)
    parser.add_argument(
        '--unit_grid', help="Rectangular_component_resolution", type=int)
    parser.add_argument('--unit_n', help="unit_of_Numbers", type=int)
    parser.add_argument('--positions', type=int, nargs='+',
                        help="position_of_units")
    parser.add_argument('--outdir', '--o', help="content_of_result", type=str)
    parser.add_argument('--file_name', help="name_of_file", type=str)
    options = parser.parse_args()
    return options
