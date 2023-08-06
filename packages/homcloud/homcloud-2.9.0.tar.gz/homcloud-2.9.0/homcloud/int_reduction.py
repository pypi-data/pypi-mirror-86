import argparse
import sys
import logging

from homcloud.version import __version__
import numpy as np

from homcloud.optimal_volume import prepare_signs
from homcloud.license import add_argument_for_license
from homcloud.diagram import PD
import homcloud.int_reduction_ext as int_reduction_ext


def build_checker(dim, dic):
    signs = np.array(prepare_signs(dim, dic), dtype=int)
    num_cells = count_num_cells(dim, dic["map"])
    checker = int_reduction_ext.Checker(num_cells)

    for col_index, column in enumerate(dic["map"]):
        if dic["type"] == "abstract":
            d, row_indices, values = column
            values = values
        else:
            d, row_indices = column
            values = signs
        checker.add_cell(d)
        row_indices = np.array(row_indices, dtype=int)
        values = np.array(values, dtype=int)
        argsorted = np.argsort(row_indices)
        for (row_index, value) in zip(row_indices[argsorted], values[argsorted]):
            checker.add_boundary_coef(col_index, row_index, value)
    return checker


def count_num_cells(dim, map):
    num_cells = [0] * (dim + 1)
    for d, *_ in map:
        num_cells[d] += 1
    return num_cells


def main(args=None):
    # logging.basicConfig(level=logging.DEBUG)
    args = args or argument_parser().parse_args()
    logging.info("load")
    diagram = PD.load_from_indexed_diphafile(args.input, 0, True)
    logging.info("build-matrix")
    checker = build_checker(diagram.index_map.dimension, diagram.boundary_map_dict)

    logging.info("reduction")
    stop_coef, stop_index = checker.check()
    if stop_coef == 0:
        print("No Problem")
        return 0
    else:
        stop_time = diagram.index_map.resolve_level(stop_index)
        print("Problematic coef: {}, Problematic time: {}".format(stop_coef, stop_time))
        return 1


def argument_parser():
    p = argparse.ArgumentParser(description="Examine field problem")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    p.add_argument("input", help="input file")
    return p


if __name__ == "__main__":
    sys.exit(main())
