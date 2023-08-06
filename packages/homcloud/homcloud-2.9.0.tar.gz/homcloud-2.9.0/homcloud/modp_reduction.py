import argparse
import sys
import math
import struct

from homcloud.version import __version__
import numpy as np

from homcloud.optimal_volume import prepare_signs
from homcloud.license import add_argument_for_license
from homcloud.diagram import PD
from homcloud.modp_reduction_ext import ModpMatrix


def build_matrix(p, dim, dic):
    signs = np.array(prepare_signs(dim, dic), dtype=int)
    num_cells = count_num_cells(dim, dic["map"])
    matrix = ModpMatrix(p, num_cells)

    for col_index, column in enumerate(dic["map"]):
        if dic["type"] == "abstract":
            d, row_indices, values = column
            values = values
        else:
            d, row_indices = column
            values = signs
        matrix.add_cell(d)
        row_indices = np.array(row_indices, dtype=int)
        values = np.array(values, dtype=int)
        argsorted = np.argsort(row_indices)
        for (row_index, value) in zip(row_indices[argsorted], values[argsorted]):
            matrix.add_boundary_coef(col_index, row_index, value)
    return matrix


def count_num_cells(dim, map):
    num_cells = [0] * (dim + 1)
    for d, *_ in map:
        num_cells[d] += 1
    return num_cells


def resolve_pair(index_map, d, birth, death):
    if death == -1:
        return -d - 1, index_map.resolve_level(birth), -math.inf
    else:
        return d, index_map.resolve_level(birth), index_map.resolve_level(death)


def resolve_pairs(index_map, pairs):
    for pair in pairs:
        d, birth, death = resolve_pair(index_map, *pair)
        if (birth != death) or (d < 0):
            yield d, birth, death


def build_ouptut_idiagram(f, index_map, pairs):
    resolved_pair = list(resolve_pairs(index_map, pairs))
    PD.write_dipha_diagram_header(f)
    f.write(struct.pack("q", len(resolved_pair)))
    for d, birth, death in resolved_pair:
        f.write(struct.pack("qdd", d, birth, death))


def main(args=None):
    args = args or argument_parser().parse_args()
    diagram = PD.load_from_indexed_diphafile(args.input, 0, True)
    matrix = build_matrix(args.p, diagram.index_map.dimension, diagram.boundary_map_dict)

    matrix.reduce_all()
    pairs = matrix.birth_death_pairs()

    if args.output:
        with open(args.output, "wb") as f:
            build_ouptut_idiagram(f, diagram.index_map, pairs)
    else:
        for d, birth, death in resolve_pairs(diagram.index_map, pairs):
            print(d, birth, death)


def argument_parser():
    p = argparse.ArgumentParser(description="Examine field problem")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    p.add_argument("-p", type=int, required=True, help="prime number")
    p.add_argument("-o", "--output", help="output file")
    p.add_argument("input", help="input file")
    return p


if __name__ == "__main__":
    sys.exit(main())
