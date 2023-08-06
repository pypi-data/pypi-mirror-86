import io
import os
import math
import struct
from collections import defaultdict
from tempfile import TemporaryDirectory
import sys
import operator

import msgpack
import numpy as np

import homcloud.alpha_shape3
import homcloud.alpha_shape2
import homcloud.periodic_alpha_shape3
from homcloud.index_map import IndexMapForAlphaFiltration
from homcloud.filtration import (
    Filtration, FiltrationWithIndex, FiltrationWithoutIndex
)
import homcloud.utils as utils
import homcloud.phat_ext as phat


def dict_simplices(simplices):
    return {simplex.key: simplex for simplex in simplices}


MINUS_INF = -sys.float_info.max


class AlphaShape(object):
    def create_filtration(self, no_square, save_boundary_map):
        simplices = [
            Simplex(alpha_simplex, i, no_square)
            for (i, alpha_simplex)
            in enumerate(sorted(self.simplices,
                                key=operator.attrgetter("birth_radius")))
        ]
        return AlphaFiltration(self.coordinates_of_vertices(), simplices,
                               dict_simplices(simplices), self.dim(),
                               save_boundary_map)

    def coordinates_of_vertices(self):
        return self.coordinates

    def subsets(self):
        subsets_simplices = defaultdict(list)
        for simplex in self.simplices:
            group_names = [v.group_name for v in simplex.vertices()]
            if group_names[0] == -1:
                continue
            if all(gn == group_names[0] for gn in group_names):
                subsets_simplices[group_names[0]].append(simplex)
        return {
            group_name: AlphaSubset(group_name, self.coordinates,
                                    simplices, self.dim())
            for (group_name, simplices) in subsets_simplices.items()
        }

    def all_subsets_acyclic(self):
        return all(subset.create_filtration(False, False).isacyclic()
                   for subset in self.subsets().values())

    def check_subsets_acyclicity(self):
        for subset in self.subsets().values():
            if not subset.create_filtration(False, False).isacyclic():
                message = "Subset {} is not acyclic".format(subset.group_name)
                raise(RuntimeError(message))

    def become_partial_shape(self):
        for subset in self.subsets().values():
            for simplex in subset.simplices:
                simplex.birth_radius = MINUS_INF

    @staticmethod
    def simplex_key(simplex):
        return tuple(sorted(v.vertex_index for v in simplex.vertices()))


class AlphaShape3(homcloud.alpha_shape3.AlphaShape3, AlphaShape):
    def __init__(self, points, weighted, rel_homology):
        super().__init__(points, weighted, rel_homology)
        self.coordinates = points[:, 0:3]
        self.simplices = self.vertices() + self.edges() + self.facets() + self.cells()

    @staticmethod
    def dim():
        return 3


class AlphaSubset(AlphaShape):
    def __init__(self, group_name, points, simplices, dim):
        self.group_name = group_name
        self.simplices = simplices
        self.coordinates = points
        self._dim = dim

    def dim(self):
        return self._dim


class AlphaShape2(homcloud.alpha_shape2.AlphaShape2, AlphaShape):
    def __init__(self, points, weighted, rel_homology):
        super().__init__(points, weighted, rel_homology)
        self.coordinates = points[:, 0:2]
        self.simplices = self.vertices() + self.edges() + self.faces()

    @staticmethod
    def dim():
        return 2


class Simplex(object):
    """A class representing simplex
    This class wraps PC2diphacomplex.alpha_simplex.{Vertex, Cell, Edge, Facet}.
    """

    def __init__(self, alpha_simplex, index, no_square=False):
        self.alpha_simplex = alpha_simplex
        self.index = index  # NOTE: This index is different from vertex's index
        self.key = AlphaShape.simplex_key(alpha_simplex)
        self.no_square = no_square
        self.true_birth_radius = self.birth_radius = \
            self.normalize_radius(alpha_simplex.birth_radius)

    def __repr__(self):
        return "alpha_filtration.Simplex(index={}, key={}, no_square={}, birth_radius={}, true_birth_radius={}".format(
            self.index, self.key, self.no_square, self.birth_radius, self.true_birth_radius
        )

    def boundary_keys(self):
        """Return list of frozensets of vertices of indices of boundary simplices"""
        if self.isvertex():
            return []
        return [self.key[0:n] + self.key[n + 1:] for n in range(len(self.key))]

    def signed_boundary_keys(self):
        def plusminus_alternative(length):
            return [(-1 if k % 2 else 1) for k in range(length)]

        unsigned = self.boundary_keys()
        return list(zip(plusminus_alternative(len(unsigned)), unsigned))

    def isvertex(self):
        """Return True if the simplex wraps a vertex.
        """
        return (isinstance(self.alpha_simplex, homcloud.alpha_shape2.Vertex) or
                isinstance(self.alpha_simplex, homcloud.alpha_shape3.Vertex) or
                isinstance(self.alpha_simplex, homcloud.periodic_alpha_shape3.Vertex))

    def normalize_radius(self, r):
        if self.no_square:
            return math.copysign(math.sqrt(abs(r)), r)
        else:
            return r

    @property
    def dim(self):
        """Return the dimension of the simplex"""
        return len(self.key) - 1


class AlphaFiltrationBase(Filtration):
    def __init__(self, points, simplices, dict_simplices, dim, save_boundary_map):
        """
        Args:
        points -- list of N-d point coordinates
        simplices -- list of simplices, must be sorted by their birth_radius
        dict_simplices -- dictiorary: simplex.key -> simplex
        dim: -- dimension of the alpha filtration
        """
        self.points = points
        self.simplices = simplices
        self.dict_simplices = dict_simplices
        self.dim = dim
        self.save_boundary_map = save_boundary_map

    def write_dipha_complex(self, output):
        """"Write dipha bondary matrix data to file"""
        def write_dipha_header(num_simplices):
            """Write magic number, type, boundary/coboundary,
            num_simplices, and dimension
            """
            output.write(struct.pack("qqqqq", 8067171840, 0, 0, num_simplices, self.dim))

        def write_dimensions():
            """Write dimensions of each simplex"""
            for simplex in self.simplices:
                output.write(struct.pack("q", simplex.dim))

        def write_birth_radii():
            """Write birth radii for each simplex"""
            for simplex in self.simplices:
                output.write(struct.pack("d", simplex.birth_radius))

        def write_boundary_map_sizes():
            n = 0
            for simplex in self.simplices:
                output.write(struct.pack("q", n))
                n += len(simplex.boundary_keys())
            output.write(struct.pack("q", n))  # Write the number of all boundary elements

        def write_boundary_map():
            for simplex in self.simplices:
                for key in simplex.boundary_keys():
                    output.write(struct.pack("q", self.dict_simplices[key].index))

        write_dipha_header(len(self.simplices))
        write_dimensions()
        write_birth_radii()
        write_boundary_map_sizes()
        write_boundary_map()

    def isacyclic(self):
        def read_num_essential_pairs(f):
            num_ess_pairs = 0
            num_pairs = utils.read_diagram_header(f)
            for _ in range(num_pairs):
                pair_d, _, _ = struct.unpack("qdd", f.read(24))
                if pair_d < 0:
                    num_ess_pairs += 1
            return num_ess_pairs

        with TemporaryDirectory() as tmpdir:
            outpath = os.path.join(tmpdir, "tmp.diagram")
            self.compute_diagram_and_save(outpath)
            with open(outpath, "rb") as f:
                return read_num_essential_pairs(f) == 1


class AlphaFiltration(AlphaFiltrationBase, FiltrationWithoutIndex):
    def indexize(self, symbols=None):
        """Index-ize self and return index-ized filtration.
        self.simplices is modified (birth_radius is replaced
        by index value) in this method.
        """
        for simplex in self.simplices:
            simplex.birth_radius = simplex.index

        return IndexedAlphaFiltration(
            self.create_index_map(self.simplices, self.points, symbols, self.dim),
            self.points, self.simplices, self.dict_simplices, self.dim,
            self.save_boundary_map, self
        )

    @staticmethod
    def create_index_map(simplices, points, symbols, dim):
        """Return dictionary of indices.
        """
        return IndexMapForAlphaFiltration(
            np.array([simplex.true_birth_radius for simplex in simplices],
                     dtype=float),
            points,
            [list(simplex.key) for simplex in simplices],
            symbols,
            dim
        )

    @staticmethod
    def favorite_algorithm():
        return "dipha"


class IndexedAlphaFiltration(AlphaFiltrationBase, FiltrationWithIndex):
    def __init__(self, index_map, points, simplices, dict_simplices, dim,
                 save_boundary_map, orig):
        self.index_map = index_map
        AlphaFiltrationBase.__init__(
            self, points, simplices, dict_simplices, dim, save_boundary_map
        )

    def write_indexed_complex(self, output):
        """Write the dipha bondary matrix data with index-map information to output.
        """
        complex_buf = io.BytesIO()
        self.write_dipha_complex(complex_buf)

        output.write(msgpack.packb({
            "dipha-data": complex_buf.getvalue(),
            "index-map": self.index_map.to_dict(),
        }, use_bin_type=True))

    def build_phat_matrix(self):
        matrix = phat.Matrix(len(self.simplices), self.boundary_map_style())
        for simplex in self.simplices:
            boundary = [self.dict_simplices[key].index
                        for key in simplex.boundary_keys()]
            matrix.set_dim_col(simplex.index, simplex.dim, boundary)

        return matrix

    def boundary_map_style(self):
        return "simplicial" if self.save_boundary_map else "none"

    @staticmethod
    def favorite_algorithm():
        return "phat-twist"


class PeriodicBoundaryCondition(object):
    """
    """

    def __init__(self, xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, zmin=0.0, zmax=1.0):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def xrange(self):
        return (self.xmin, self.xmax)

    def yrange(self):
        return (self.ymin, self.ymax)

    def zrange(self):
        return (self.zmin, self.zmax)


class PeriodicAlphaShape3(homcloud.periodic_alpha_shape3.PeriodicAlphaShape3, AlphaShape):
    def __init__(self, points, weighted, rel_homology, boundary_condition):
        super().__init__(points, weighted, rel_homology, boundary_condition)
        self.coordinates = points[:, 0:3]
        vertices = self.vertices()
        cells = self.cells()
        facets = self.facets()
        edges = self.edges()
        self.simplices = vertices + edges + facets + cells

    @staticmethod
    def dim():
        return 3


def create_alpha_shape(points, dim, weighted=False, use_relative_homology=False, boundary_condition=None):
    if dim == 2:
        return AlphaShape2(points, weighted, use_relative_homology)
    if dim == 3:
        if boundary_condition is None:
            return AlphaShape3(points, weighted, use_relative_homology)
        elif isinstance(boundary_condition, PeriodicBoundaryCondition):
            return PeriodicAlphaShape3(points, weighted, use_relative_homology, boundary_condition)
        raise ValueError("type of boundary condition must be PeriodicBoundaryCondition or None")
    raise ValueError("dimension of a point cloud must be 2 or 3")
