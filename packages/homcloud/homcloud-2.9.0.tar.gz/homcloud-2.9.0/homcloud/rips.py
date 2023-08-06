import argparse
import struct

import numpy as np
import ripser

from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.filtration import (
    FiltrationWithIndex, FiltrationWithoutIndex
)
from homcloud.bitmap_filtration import invert_permutation
from homcloud.index_map import IndexMapForRips
from homcloud.utils import load_symbols


class RipsFiltrationBase(object):
    def __init__(self, matrix, upper_dim, upper_value):
        assert matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]
        self.matrix = matrix
        self.upper_dim = upper_dim
        self.upper_value = upper_value

    def write_dipha_complex(self, output):
        num_points = self.matrix.shape[0]

        def write_dipha_header():
            output.write(struct.pack("qqq", 8067171840, 7, num_points))

        def write_matrix():
            for k in range(num_points):
                for l in range(num_points):
                    output.write(struct.pack("d", self.matrix[k, l] * 2))

        write_dipha_header()
        write_matrix()

    def compute_diagram_and_save(self, outpath, parallels=1, algorithm=None):
        if not algorithm:
            algorithm = self.favorite_algorithm()

        if algorithm == "dipha":
            self.compute_diagram_by_dipha(
                outpath, parallels, self.upper_dim, self.upper_value
            )
        elif algorithm == "ripser":
            self.compute_diagram_by_ripser(
                outpath, self.upper_dim, self.upper_value
            )
        else:
            raise(ValueError("unknown algorithm: {}".format(algorithm)))

    def write_diagram(self, output, diagrams):
        def write_header(output, num_pairs):
            output.write(struct.pack("qqq", 8067171840, 2, num_pairs))

        def num_pairs(diagrams):
            return sum(map(lambda pairs: pairs.shape[0], diagrams))

        def write_diagram(output, dim, pairs):
            for k in range(pairs.shape[0]):
                birth = pairs[k, 0]
                death = pairs[k, 1]
                output.write(struct.pack("qdd", dim, birth, death))

        write_header(output, num_pairs(diagrams))
        for dim, pairs in enumerate(diagrams):
            write_diagram(output, dim, pairs)


class RipsFiltration(RipsFiltrationBase, FiltrationWithoutIndex):
    def compute_diagram_by_ripser(self, outpath, upper_dim, upper_value):
        if upper_value != np.inf:
            raise RuntimeError("upper_value is not supported by ripser now. This is because ripser returns a curious result when upper_value is given")
        diagrams = ripser.ripser(self.matrix, upper_dim, upper_value, 2, True)["dgms"]
        with open(outpath, "wb") as output:
            self.write_diagram(output, diagrams)

    def indexize(self, symbols):
        indices = np.triu_indices_from(self.matrix, 1)
        distances = self.matrix[indices]
        order = np.argsort(distances)
        iorder = invert_permutation(order)
        levels = np.concatenate(([0], distances[order]), axis=None)
        upper_index = np.searchsorted(levels, self.upper_value, "right")
        indexed_matrix = np.zeros_like(self.matrix)
        indexed_matrix[indices] = iorder + 1
        indexed_matrix[(indices[1], indices[0])] = iorder + 1
        edges = [["*"]] + list(zip(indices[0][order].tolist(),
                                   indices[1][order].tolist()))
        index_map = IndexMapForRips(levels, self.upper_dim, edges, symbols)
        return RipsFiltrationWithIndex(indexed_matrix, self.upper_dim,
                                       upper_index, index_map)

    def favorite_algorithm(self):
        if self.upper_value == np.inf:
            return "ripser"
        else:
            return "dipha"


class RipsFiltrationWithIndex(RipsFiltrationBase, FiltrationWithIndex):
    def __init__(self, indexed_matrix, upper_dim, upper_index, index_map):
        super().__init__(indexed_matrix, upper_dim, upper_index)
        self.index_map = index_map

    def compute_diagram_by_ripser(self, outpath, upper_dim, upper_value):
        raise(RuntimeError("Cannot use ripser with an indexed \"rips\" filtration"))

    @staticmethod
    def favorite_algorithm():
        return "dipha"


def main(args=None):
    args = args or argument_parser().parse_args()
    matrix = np.loadtxt(args.input)
    filtration = RipsFiltration(matrix, args.upper_degree, args.upper_value)

    vertex_symbols = load_symbols(args.vertex_symbols)
    if args.combine_index_map:
        filtration = filtration.indexize(vertex_symbols)
    filtration.compute_diagram_and_save(args.output, parallels=args.parallels,
                                        algorithm=args.algorithm)


def argument_parser():
    p = argparse.ArgumentParser(description="Compute a PD from Vietris-Rips filtration")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-d", "--upper-degree", type=int, required=True,
                   help="Maximum computed degree")
    p.add_argument("-u", "--upper-value", type=float, default=np.inf,
                   help="Maximum distance (default: +inf)")
    p.add_argument("-I", "--combine-index-map", default=False, action="store_true",
                   help="combine the index map with the output filtration")
    p.add_argument("--vertex-symbols", help="vertex symbols file")
    p.add_argument("--algortihm", default=None, help="algorithm (dipha, ripser)")
    p.add_argument("--parallels", default=1, type=int,
                   help="number of threads (default: 1)")
    add_argument_for_license(p)
    p.add_argument("input", help="input file")
    p.add_argument("output", help="output file")
    return p


if __name__ == "__main__":
    main()
