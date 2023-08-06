import argparse
import os
import struct
import io
import sys
import warnings

import msgpack
import numpy as np

from homcloud.version import __version__
from homcloud.index_map import IndexMap, MapType
import homcloud.utils as utils
from homcloud.alpha_filtration import MINUS_INF
from homcloud.license import add_argument_for_license


def main(args=None):
    warnings.warn("diagram_to_text is now obsolete. Please use homcloud.dump_diagram")
    args = args or argument_parser().parse_args()
    births, deaths, essential_births, index_map = load_diagram(args.input, args.degree)

    if args.output is None:
        output = sys.stdout
    else:
        output = open(args.output, "w")

    if index_map is None:
        print_pairs(output, births, deaths)
        print_pairs(output, essential_births, np.full_like(essential_births, np.inf))
    elif not args.show_birthdeath_info == "yes":
        print_pairs(output,
                    index_map.resolve_levels(essential_births),
                    np.full_like(essential_births,
                                 deathtime_essential_pair(index_map.levels_sign_flipped)))
        print_pairs(output,
                    index_map.resolve_levels(births), index_map.resolve_levels(deaths))
    elif index_map.type() == MapType.alpha:
        print_pairs_with_info(output, births, deaths, index_map, print_simplex)
    elif index_map.type() == MapType.bitmap:
        print_pairs_with_info(output, births, deaths, index_map, print_position)
    else:
        raise RuntimeError("Unknown input format")


def deathtime_essential_pair(levels_sign_flipped):
    if levels_sign_flipped is True:
        return -np.inf
    else:
        return np.inf


def argument_parser():
    p = argparse.ArgumentParser(description="Convert a diagram into text")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    p.add_argument("-d", "--degree", type=int, required=True)
    p.add_argument("-S", "--show-birthdeath-info", default="no",
                   help="show birth/death pixels/simplices  (yes/no, default: no)" +
                   " (Note: if yes, Essential birth-death pair is ignored)")
    p.add_argument("-o", "--output",
                   help="output file")
    p.add_argument("input", help="input file")
    return p

def determine_input_file_type(path):
    _, ext = os.path.splitext(path)
    if ext in [".diagram", ".idiagram"]:
        return ext
    else:
        return ".diagram"

def load_diagram(path, d):
    inputtype = determine_input_file_type(path)
    if inputtype == ".diagram":
        with open(path, "rb") as f:
            births, deaths, essential_births = load_dipha_diagram(f, d)
            return births, deaths, essential_births, None
    if inputtype == ".idiagram":
        with open(path, "rb") as f:
            data = next(msgpack.Unpacker(f, raw=False))
            births, deaths, essential_births = load_dipha_diagram(
                io.BytesIO(data["diagram"]), d
            )
            index_map = IndexMap.load_from_dict(data["index-map"])
            return births, deaths, essential_births, index_map

def load_dipha_diagram(f, d):
    num_pairs = utils.read_diagram_header(f)
    births = []
    deaths = []
    essential_births = []
    for _ in range(0, num_pairs):
        pair_d, birth, death = struct.unpack("qdd", f.read(24))
        if pair_d == d:
            births.append(birth)
            deaths.append(death)
        elif -pair_d - 1 == d:
            essential_births.append(birth)
    return births, deaths, essential_births

def print_pairs(output, births, deaths):
    for (birth, death) in zip(births, deaths):
        if birth != death and birth != MINUS_INF:
            output.write("{} {}\n".format(birth, death))

def print_position(output, index, index_map):
    coords = index_map.positions[index]
    output.write("(")
    output.write(",".join(str(c) for c in coords))
    output.write(")")

def print_simplex(output, index, index_map):
    def point_str(point):
        return "(" + ",".join(str(x) for x in index_map.points[point]) + ")"

    simplex = index_map.simplices[index]
    output.write("{")
    output.write(",".join(point_str(point) for point in simplex))
    output.write("}")

def print_pairs_with_info(output, births, deaths, index_map, print_birthdeath_info):
    for (birth_index, death_index) in zip(births, deaths):
        birth_index = int(birth_index)
        death_index = int(death_index)
        birth = index_map.resolve_level(birth_index)
        death = index_map.resolve_level(death_index)
        if birth == death or birth == MINUS_INF:
            continue
        output.write("{} {} ".format(birth, death))
        print_birthdeath_info(output, birth_index, index_map)
        output.write(" ")
        print_birthdeath_info(output, death_index, index_map)
        output.write("\n")

if __name__ == "__main__":
    main()
