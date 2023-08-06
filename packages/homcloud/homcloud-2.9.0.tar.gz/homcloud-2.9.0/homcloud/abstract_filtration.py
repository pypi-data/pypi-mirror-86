import re
import math
import argparse

import msgpack
import numpy as np

from homcloud.utils import parse_bool
from homcloud.index_map import IndexMapForAbstractFiltration
import homcloud.phat_ext as phat
from homcloud.filtration import Filtration, FiltrationWithIndex
from homcloud.version import __version__
from homcloud.license import add_argument_for_license


def main(args=None):
    args = args or argument_parser().parse_args()
    with open(args.input) as f:
        filt = AbstractFiltrationWithIndex.load(f, args.save_boundary_map)
    filt.compute_diagram_and_save(args.output)


def argument_parser():
    p = argparse.ArgumentParser(description="Convert a description of boundary map to a PD")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-M", "--save-boundary-map",
                   default=True, type=parse_bool,
                   help="save boundary map into idiagram file")
    add_argument_for_license(p)
    p.add_argument("input", help="input file name")
    p.add_argument("output", help="output file name")
    return p


class AbstractFiltrationWithIndex(Filtration, FiltrationWithIndex):
    def __init__(self, boundary_map, index_map, save_boundary_map):
        self.boundary_map = boundary_map
        self.index_map = index_map
        self.save_boundary_map = save_boundary_map

    @staticmethod
    def load(f, save_boundary_map):
        loader = AbstractFiltrationLoader(f)
        loader.load()
        return loader.filtration(save_boundary_map)

    def build_phat_matrix(self):
        matrix = phat.Matrix(len(self.boundary_map), "none")
        for n, single in enumerate(self.boundary_map):
            dim = single[0]
            boundary = []
            for idx, coef in zip(single[1], single[2]):
                if coef % 2 != 0:
                    boundary.append(idx)
            matrix.set_dim_col(n, dim, sorted(boundary))

        return matrix

    def boundary_map_byte_sequence(self, *ignored):
        if not self.save_boundary_map:
            return None
        packer = msgpack.Packer(use_bin_type=True, autoreset=False)
        packer.pack_map_header(2)
        packer.pack("type")
        packer.pack("abstract")
        packer.pack("map")
        packer.pack_array_header(len(self.boundary_map))
        for boundary in self.boundary_map:
            packer.pack(boundary)
        return packer.bytes()

    def write_indexed_complex(self, output):
        raise(RuntimeError("Dipha is not supported by abstract filtration"))

    @staticmethod
    def favorite_algorithm():
        return "phat-twist"


class ParseError(RuntimeError):
    pass


class AbstractFiltrationLoader(object):
    def __init__(self, io):
        self.io = io
        self.autoid = False
        self.autosymbol = True
        self.nextid = 0
        self.lasttime = -math.inf
        self.boundary_information = []

    def load(self):
        for line in self.io:
            line = line.strip()
            if line == "" or self.iscomment(line):
                continue
            if self.is_optionline(line):
                self.parse_option(line)
                continue
            self.boundary_information.append(self.parse_line(line))
            self.nextid += 1

    def filtration(self, save_boundary_map):
        symbols = []
        levels = []
        boundary_map = []
        dims = []
        for (id, symbol, dim, time, indices, coefs) in self.boundary_information:
            symbols.append(symbol)
            levels.append(time)
            dims.append(dim)
            boundary_map.append([dim, indices, coefs])

        index_map = IndexMapForAbstractFiltration(np.array(levels, dtype=float),
                                                  max(dims), symbols)
        return AbstractFiltrationWithIndex(boundary_map, index_map, save_boundary_map)

    OPTIONS = [re.compile(r"autoid\s*:"), re.compile(r"autosymbol\s*:")]

    def is_optionline(self, line):
        return any(option.match(line) for option in self.OPTIONS)

    def parse_option(self, line):
        if self.boundary_information:
            raise(ParseError("Options must be above boundary information"))
        command, _, args = line.lower().partition(":")
        args = args.strip()
        if command == "autoid":
            self.autoid = parse_bool(args)
        if command == "autosymbol":
            self.autosymbol = parse_bool(args)

    @staticmethod
    def iscomment(line):
        return line.startswith("#")

    def parse_line(self, line):
        def check_id(id):
            if id != self.nextid:
                raise(ParseError("id must be incremental integers from 0"))

        def check_symbol(symbol):
            if not re.match(r"[a-zA-Z0-9_]+\Z", symbol):
                raise(ParseError("Invalid cell symbol {}".format(symbol)))

        def check_time(time):
            if time < self.lasttime:
                raise(ParseError("time must be monotone"))
            self.lasttime = time

        if line.count("=") != 1:
            raise(ParseError("\"=\" symbol is required"))

        leftstr, rightstr = line.split("=")

        indices, coefs = self.parse_boundary(rightstr)

        left = re.split(r"\s+", leftstr.strip())
        id = self.nextid if self.autoid else int(left.pop(0), 10)
        check_id(id)
        symbol = str(id) if self.autosymbol else left.pop(0)
        check_symbol(symbol)
        dim = int(left.pop(0), 10)
        time = float(left.pop(0))
        check_time(time)
        if left:
            raise(ParseError("Too much elements in a line: \"{}\"".format(line)))

        return id, symbol, dim, time, indices, coefs

    def parse_boundary(self, s):
        def parse_numbers(string):
            if string:
                return [int(n, 10) for n in re.split(r"\s+", string.strip())]
            else:
                return []

        if s.count(":") != 1:
            raise(ParseError("\":\" symbol is required"))
        indices_str, coef_str = re.split(r":", s.strip())
        return parse_numbers(indices_str), parse_numbers(coef_str)


if __name__ == "__main__":
    main()
