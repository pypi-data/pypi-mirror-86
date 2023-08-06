"""HomCloud python interface

This module provides the interface to HomCloud from python program.

The API document is written by sphinx with Napolen.
http://www.sphinx-doc.org/ja/stable/ext/napoleon.html
"""
from tempfile import NamedTemporaryFile, TemporaryDirectory
import shutil
import subprocess
import sys
import os
from itertools import chain
import warnings

import numpy as np
from forwardable import forwardable
import matplotlib.pyplot as plt
from PIL import Image
import json
import msgpack

import homcloud.alpha_filtration as alpha_filtration
import homcloud.pict.binarize as binarize
import homcloud.diagram as homdiag
import homcloud.plot_PD as plot_PD
import homcloud.full_ph_tree as full_ph_tree
import homcloud.index_map as index_map
import homcloud.utils as utils
import homcloud.pict.utils as pict_utils
from homcloud.optimal_volume import (
    VolumeOptimalCycleFinder
)
import homcloud.optimal_volume as optvol
from homcloud.full_ph_tree import SpatialSearcher
import homcloud.vectorize_PD as vectorize_PD
import homcloud.view_index_pict as view_index_pict
import homcloud.plot_PD_slice as plot_PD_slice
import homcloud.pict.tree as pict_tree
import homcloud.paraview_interface as pv_interface
import homcloud.pict.optimal_one_cycle as pict_opt1cyc
import homcloud.pict.slice3d as pict_slice3d
import homcloud.idiagram2diagram as idiagram2diagram
import homcloud.pict.distance_transform as pict_distance_transform
import homcloud.int_reduction as int_reduction
import homcloud.abstract_filtration as abstract_filtration
from homcloud.visualize_3d import ParaViewSimplexDrawer
from homcloud.license import LICENSE_TERMS


_tempdir_path = None


def tempdir():
    global _tempdir_path
    if not _tempdir_path:
        _tempdir_path = TemporaryDirectory()

    return _tempdir_path


def tempfile(suffix):
    file = NamedTemporaryFile(suffix=suffix, dir=tempdir().name, delete=False)
    file.close()
    return file.name


def example_data(name):
    """Returns example data.

    Returns the tetrahedron 3D pointcloud for name == "tetrahedron".

    Args:
        name: Name of the data

    Examples:
        >>> import homcloud.interface as hc
        >>> hc.example_data("tetrahedron")
        array([[ 0.,  0.,  0.],
               [ 8.,  0.,  0.],
               [ 5.,  6.,  0.],
               [ 4.,  2.,  6.]])
    """
    if name == "tetrahedron":
        return np.array([
            [0.0, 0.0, 0.0],
            [8.0, 0.0, 0.0],
            [5.0, 6.0, 0.0],
            [4.0, 2.0, 6.0],
        ])
    if name == "bitmap_01_5x5x5":
        return np.array([
            [[0, 0, 1, 1, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 1, 1]],
            [[0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 1, 0]],
            [[0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]],
            [[0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]],
            [[1, 1, 1, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 1, 1, 0, 0]]
        ], dtype=bool)
    if name == "bitmap_levels_5x5":
        return np.array([
            [0, 0, 1, 1, 1],
            [0, 4, 0, 5, 1],
            [0, 8, 0, 3, 1],
            [0, 0, 4, 7, 1],
            [0, 0, 2, 1, 1],
        ], dtype=int)

    raise ValueError("Unknown example name: %s" % name)


def distance_transform(pict, signed=False, metric="manhattan",
                       periodicity=None, obstacle=None, VI=None, V=None):
    """Distance transform.

    Args:
        pict (numpy.ndarray): A binary picture. dtype must be bool.
        signed (bool): True for signed distance transform
        metric (string): Metric. The following metrics are available:
            "manhattan", "chebyshev", "euclidean", "mahalanobis"
        periodicity (None or list of bool): Periodic boundary condition
        obstacle (None or numpy.ndarray): Obstacle bitmap
        VI (None or numpy.ndarray): Inverse matrix for Mahalanobis metric
        V (None or numpy.ndarray): Matrix for Mahalanobis metric

    Returns:
        An ndarray object.

    Example:
        >>> import homcloud.interface as hc
        >>> import numpy as np
        >>> bitmap = np.array([[0, 1, 0, 0], [1, 1, 0, 1]], dtype=bool)
        >>> hc.PDList.from_bitmap_levelset(hc.distance_transform(bitmap, True))
        -> Returns a new PDList

    Remarks:
        The current implementation for periodic BC is a simple periodic image
        copy method. Hence the performance is not so good.
        The developers of HomCloud plan to implove the efficiency
        in the future.
    """
    return pict_distance_transform.distance_transform(
        pict, metric, signed, periodicity=periodicity, obstacle=obstacle, VI=VI, V=V
    )


class PDList(object):
    """Collection of 0th,1st,..,and q-th persitence diagrams.

    In HomCloud, diagrams for all degrees coming from a filtration
    are combined into a single file. This class is the interface to
    the file.

    Args:
       path (string): The pathname to a diagram file
       type (string): Type of diagram file. One of the following:
           "diagram", "idiagram", or None (autodetected)
       cache (bool): :meth:`dth_diagram` is cached if True.
       negate (bool): If true all birth/death time sholud be negated.
           This value is true only if you use a diagram which is *not* indexed.
    """

    def __init__(self, path, type=None, cache=False, negate=False):
        self.path = path
        self.type = type
        self.diagrams = dict() if cache else None
        self.index_map = None
        self.negate = negate

    def __repr__(self):
        return "PDList(path=%s)" % self.path

    @staticmethod
    def from_alpha_filtration(pointcloud,
                              weight=False, no_squared=False,
                              subsets=False, check_acyclicity=False,
                              algorithm=None, parallels=1, vertex_symbols=None,
                              save_to=None, indexed=True,
                              save_boundary_map=False, periodicity=None):
        """Compute PDList by using an alpha filtration from a point cloud.

        Args:
            pointcloud (numpy.ndarray): Point cloud data. Each row
                represents a single point.
            weight (bool): If False, the pointcloud has no weight. If True,
                the last column of the pointcloud ndarray is regarded as
                weights. Please note that the weight paramters of points
                should be the square of their own radii.
            no_squared (bool): By default, all birth/death times are squared.
                If no_squared is True, all computed birth/death times are
                not squared.
            subsets (list[int] or bool or None) :
                This parameter is used to compute relative homology.
                This parameter allows you to analyze the interspace structures
                between two or more objects in your pointcloud.

                If `subsets` is None, normal persistent homology is computed.

                If `subsets` is a list of integers whose length is the same
                as the number of points, the points are grouped
                by the integers and the gaps in the points in the same
                group is filled. The integer -1 in this list means
                that the point does not belong to any group.

                If subsets is True, the last column of `pointcloud` is regarded
                as the list of group id.
            check_acyclicity (bool):
                Checks the acyclicity of each grouped points in subsets
                if True. This parameter is used only if `subsets` parameter
                is used.
            algorithm (string or None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            vertex_symbols (list[string] or None): The names of vertices.
                The names are used to represent some simplices, such as
                birth/death simplices or optimal volumes.

                If None is given, vertices are automatically named by
                "0", "1", "2", ...
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles.
            periodicity (tuple[tuple[float, float], tuple[float, float], tuple[float, float]] or None):
                Periodic boundary condition.

        Returns:
            The :class:`PDList` object computed from the pointcloud.

        Examples:
            >>> import homcloud.interface as hc
            >>> pointcloud = hc.example_data("tetrahedron")
            >>> hc.PDList.from_alpha_filtration(pointcloud)
            -> Returns a new PDList
        """
        input_data = pointcloud.astype(dtype=float)
        num_points, dim = pointcloud.shape
        if isinstance(weight, np.ndarray):
            input_data = np.hstack([input_data,
                                    weight.reshape(num_points, 1)])
            weight = True
        elif weight is True:
            dim -= 1

        if isinstance(subsets, np.ndarray):
            input_data = np.hstack([input_data,
                                    subsets.reshape(num_points, 1)])
            subsets = True
        elif subsets is True:
            dim -= 1

        if periodicity:
            period = alpha_filtration.PeriodicBoundaryCondition(
                *list(chain.from_iterable(periodicity))
            )
        else:
            period = None

        alpha_shape = alpha_filtration.create_alpha_shape(input_data, dim,
                                                          weight, subsets, period)
        if check_acyclicity:
            alpha_shape.check_subsets_acyclicity()
        if subsets:
            alpha_shape.become_partial_shape()

        filtration = alpha_shape.create_filtration(no_squared,
                                                   save_boundary_map)
        if indexed:
            filtration = filtration.indexize(vertex_symbols)

        if save_to is None:
            save_to = PDList.tempfile(indexed)
        filtration.compute_diagram_and_save(save_to, parallels, algorithm)
        return PDList(save_to, PDList.typestring(indexed))

    @staticmethod
    def from_bitmap_levelset(array, mode="sublevel", type="bitmap",
                             algorithm=None, parallels=1,
                             periodicity=None, save_to=None, indexed=True,
                             save_boundary_map=False):
        """
        Computes superlevel/sublevel PDList from an n-dimensional bitmap.

        Args:
            array (numpy.ndarray): An n-dimensional array.
            mode (string): The direction of the filtration.
               "superlevel" or "sublevel".
            type (string): An internal filtration type.
               "bitmap" or "cubical".
               You can change the internal file format by this parameter.
               The file size of "bitmap" format is much smaller than
               "cubical". However, if you want to use the following
               functionality, you must use "cubical" format.

               * Periodic bitmaps (cylinder, torus, etc.)
               * Volume optimal cycles
            algorithm (string, None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            periodicity (None, list of bool):
                The list of booleans to specify the periodicity.
                Any periodic structure is not used if None.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles.

        Returns:
            The :class:`PDList` object computed from the bitmap.

        Examples:
            >>> import numpy as np
            >>> import homcloud.interface as hc
            >>> bitmap = np.array([[1.5, 2.0, 0.5],
            >>>                    [0.8, 4.1, 0.9],
            >>>                    [1.3, 1.8, 1.3]])
            >>> hc.PDList.from_bitmap_levelset(bitmap, "sublevel")
            -> Returns PDList object for sublevel persistence diagrams
            >>> hc.PDList.from_bitmap_levelset(bitmap, "superlevel",
            >>>                             periodicity=[True, True])
            -> Returns PDList object for superlevel PDList on a 2-torus
        """
        array = array.astype(float, copy=False)
        if mode == "sublevel":
            flip_sign = False
        elif mode == "superlevel":
            array = -array
            flip_sign = True
        else:
            raise(ValueError("unknown mode: {}".format(mode)))

        bitmap = pict_utils.build_levelset_filtration(
            array, type == "cubical", periodicity, flip_sign, save_boundary_map
        )
        if indexed:
            bitmap = bitmap.indexize()
        if not save_to:
            save_to = PDList.tempfile(indexed)
        bitmap.compute_diagram_and_save(save_to, parallels, algorithm)
        return PDList(save_to, PDList.typestring(indexed),
                      negate=(flip_sign and (not indexed)))

    @staticmethod
    def from_bitmap_distance_function(binary_pict, signed=False,
                                      metric="manhattan", type="bitmap",
                                      mask=None, algorithm=None,
                                      parallels=1, save_to=None, indexed=True,
                                      save_boundary_map=False):
        """
        This method is obsolete. Please use the combination of
        :meth:`PDList.from_bitmap_levelset` and
        :meth:`distance_transform` instead.

        Computes erosion/dilation PDList from an n-dimensional bitmap.

        In other words, this method computes the sublevel filtration
        whose level function is the distance function.

        Args:
            binary_pict (numpy.ndarray): An n-dimensional boolean array.
            signed (bool): The signed distance function is used
               instead of the normal distance function if True.
            metric (string): The metric. One of the followings:

               * "manhattan"
               * "chebyshev"
               * "euclidean"

            type (string): An internal filtration type.
               "bitmap" or "cubical".
               You can change the internal file format by this parameter.
               The file size of "bitmap" format is much smaller than
               "cubical". However, if you want to use the following
               functionality, you must use "cubical" format.

            mask (numpy.ndarray or None): The mask bitmap.
            algorithm (string, None): The name of the algorithm.
                An appropriate algorithm is
                automatically selected if None is given.

                The following algorithms are available:

                * "phat-twist"
                * "phat-chunk-parallel"
                * "dipha"

                In many cases, the parameter should be `None`.
            parallels (int): The number of threads used for the computation.
                This parameter is used only if "dipha" algorithm is used.
            save_to (string): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
            save_boundary_map (bool):
                The boundary map constructed by the given pointcloud is saved
                if this parameter is True. The boundary map is used to
                compute volume optimal cycles.

        Returns:
            The :class:`PDList` object computed from the bitmap.

        """
        # warnings.warn(
        #     "interface.PDList.from_bitmap_distance_function is obsolete."
        #     "Please use interaface.distance_transform and BitmapPHTreesPair.",
        #     PendingDeprecationWarning
        # )

        distance_map = pict_distance_transform.distance_transform(
            binary_pict, metric, signed, mask
        )
        bitmap = pict_utils.build_levelset_filtration(
            distance_map, type == "cubical", None, False, save_boundary_map
        )
        if indexed:
            bitmap = bitmap.indexize()
        if not save_to:
            save_to = PDList.tempfile(indexed)
        bitmap.compute_diagram_and_save(save_to, parallels, algorithm)
        return PDList(save_to, PDList.typestring(indexed))

    @staticmethod
    def from_rips_filtration(distance_matrix, maxdim, maxvalue=np.inf,
                             indexed=False, vertex_symbols=None,
                             algorithm=None, parallels=1, save_to=None):
        """
        Compute a PDList from a distance matrix by using Vietoris-Rips
        filtrations.

        Args:
            distance_matrix (numpy.ndarary): KxK distance matrix.
            maxdim (int): Maximal homology degree computed.
            maxvalue (float): Maximal distance for constructing a filtration.
                All longer edges do not apper in the constructed filtration.
            indexed (bool): TODO
            vertex_symbols (list[string] or None): The names of vertices.
                The names are used to represent some simplices, such as
                birth/death simplices or optimal volumes.

                If None is given, vertices are automatically named by
                "0", "1", "2", ...
            algorithm: The name of the algorithm, "dipha" and "ripser" are available.
            paralles: The number of threads for computation. This value is
                used only if algorith is "dipha".
            save_to (string or None): The file path which the computation result is
                saved into. You can load the saved data by
                `homcloud.interface.PDList(FILE_PATH)`.
                Saving the result is recommended since the computation cost is
                often expensive.
        """
        import homcloud.rips as rips

        filtration = rips.RipsFiltration(distance_matrix, maxdim, maxvalue)
        if indexed:
            filtration = filtration.indexize(vertex_symbols)
        if not save_to:
            save_to = PDList.tempfile(indexed)
        filtration.compute_diagram_and_save(save_to, parallels, algorithm=algorithm)
        return PDList(save_to, PDList.typestring(indexed))

    @staticmethod
    def from_boundary_information(boundary, levels, indexed=True, symbols=None,
                                  algorithm=None, parallels=1, save_to=None,
                                  save_boundary_map=False):
        """
        Args:
            boundary (list of (int, list of int, list of int)):
                list of (dim of cell, list of indices of, list of coefs)
        """
        assert len(boundary) == len(levels)
        assert symbols is None or len(symbols) == len(boundary)
        for k in range(len(levels) - 1):
            assert levels[k] <= levels[k + 1]
        assert indexed

        maxdim = 0
        for column in boundary:
            maxdim = max(maxdim, column[0])
        if symbols is None:
            symbols = [str(n) for n in range(len(levels))]

        filtration = abstract_filtration.AbstractFiltrationWithIndex(
            boundary,
            index_map.IndexMapForAbstractFiltration(
                np.array(levels, dtype=float), maxdim, symbols
            ),
            save_boundary_map
        )
        if not save_to:
            save_to = PDList.tempfile(indexed)
        filtration.compute_diagram_and_save(save_to, parallels, algorithm=algorithm)
        return PDList(save_to, "idipha")

    @staticmethod
    def tempfile(indexed):
        if indexed:
            return tempfile(".idiagram")
        else:
            return tempfile(".diagram")

    @staticmethod
    def typestring(indexed):
        return "idipha" if indexed else "dipha"

    def save(self, dest):
        """Save the PDList into `dest`.

        Args:
            dest (string): The filepath which the diagram data is saved into.
        """
        shutil.copyfile(self.path, dest)

    def dth_diagram(self, d):
        """Return `d`-th persistence diagram from PDList.

        Args:
            d (int): the degree of the diagram

        Returns:
            The :class:`PD` object.

        """
        def load_diagram():
            return PD(self.path, homdiag.PD.load(self.type, self.path, d, self.negate))

        if self.diagrams is None:
            return load_diagram()

        if d not in self.diagrams:
            self.diagrams[d] = load_diagram()

        return self.diagrams[d]

    __getitem__ = dth_diagram

    def idiagram_to_diagram(self, save_to=None):
        if not save_to:
            save_to = PDList.tempfile(False)
        with open(self.path, "rb") as infile:
            with open(save_to, "wb") as outfile:
                idiagram2diagram.convert(infile, outfile)
        return PDList(save_to)

    def invoke_gui_plotter(self, d, x_range=None, xbins=None, y_range=None, ybins=None,
                           colorbar={"type": "linear"},
                           title=None, unit_name=None, aspect="equal",
                           optimal_volume=False,
                           optimal_volume_options=None):
        """Invoke the GUI plotter.

        Args:
            d (int): The degree of the PD.
        """
        def format_range(r):
            return "[{}:{}]".format(r[0], r[1])

        options = ["-d", str(d)]
        if x_range:
            options.extend(["-x", format_range(x_range)])
        if xbins:
            options.extend(["-X", str(xbins)])
        if y_range:
            options.extend(["-y", format_range(y_range)])
        if ybins:
            options.extend(["-Y", str(ybins)])
        if colorbar["type"] == "linear":
            pass
        elif colorbar["type"] == "log":
            options.append("-l")
        elif colorbar["type"] == "loglog":
            options.append("--loglog")
        if "max" in colorbar:
            options.extend(["--vmax", str(colorbar["max"])])
        if title is not None:
            options.extend(["--title", str(title)])
        if unit_name is not None:
            options.extend(["--unit-name", str(unit_name)])
        options.extend(["--aspect", aspect])
        if optimal_volume:
            options.extend(["--optimal-volume", "on"])
        subprocess.Popen([sys.executable, "-m", "homcloud.plot_PD_gui"] +
                         options + [self.path])

    def check_coefficent_problem(self):
        pd = self.dth_diagram(0)
        index_map = pd.pd.index_map
        pd.load_boundary_map()
        checker = int_reduction.build_checker(index_map.dimension,
                                              pd.pd.boundary_map_dict)
        coef, index = checker.check()
        if coef == 0:
            return True, (0, 0.0)
        else:
            return False, (coef, index_map.resolve_level(index))
        # pd.pd.boundary_map_dict = None


#: Obsolete, for backward compatibility
PDs = PDList


@forwardable()
class PD(object):
    """
    The class for a single persistence diagram.

    You can get the object of this class by :meth:`PDList.dth_diagram` or
    :meth:`PDList.__getitem__`.

    Attributes:
        path (str): File path
        degree (int): Degree of the PD
        births (numpy.ndarray[num_of_pairs]): Birth times
        deaths (numpy.ndarray[num_of_pairs]): Death times
        birth_positions: Birth positions for birth-death pairs
        death_positions: Death positions for birth-death pairs
        essential_births (numpy.ndarray[num_of_ess_pairs]):
            Birth times of essenatial birth-death pairs (birth-death pairs with
            infinite death time)
        essential_birth_positions:
            Birth positions for essenatial birth-death pairs
    """

    def __init__(self, path, pd):
        self.path = path
        self.pd = pd
        self.spatial_searcher = None
        self._pairs = None

    def __repr__(self):
        return "PD(path=%s, d=%d)" % (self.path, self.pd.degree)

    def birth_death_times(self):
        """
        Returns the  birth times and death times.

        Returns:
            tuple[numpy.ndarray, numpy.ndarray]:
                The pair of birth times and death times
        """
        return self.pd.births, self.pd.deaths

    def_delegators("pd", "degree,births,deaths,birth_positions,death_positions"
                   ",essential_births,essential_birth_positions,sign_flipped")

    def histogram(self, x_range=None, x_bins=128, y_range=None, y_bins=None,):
        """
        Returns the histogram of the PD.

        This is the shortcut method of :meth:`Mesh.pd_histogram`

        Args:
           x_range (tuple[float, float] or None): The lower and upper range
               of the bins on x-axis. If None is given, the range
               is determined from the minimum and maximum of
               the birth times and death times of all pairs.
           y_range (int): The number of bins on x-axis.
           y_range (tuple[float, float] or None): The lower and upper range
               of the bins on y-axis. Same as `x_range` if None is given.
           y_bins (int or None): The number of bins on y-axis.
               Same as `x_bins` if None is given.
        """
        return Mesh(x_range, x_bins, y_range, y_bins, self.pd).pd_histogram(self.pd)

    def phtrees(self, save_to=None):
        """
        Computes a PH trees from an alpha filtration.

        Args:
            save_to (string or None): The filepath of the file
               which the PH trees information is saved in.
               You can load the PHTrees information from the file by
               using the constructor of :class:`PHTrees`.
        Returns:
            :class:`PHTrees`: PHTrees object.
        """
        if save_to is None:
            save_to = tempfile(".pht")

        if self.pd.index_map.type() != index_map.MapType.alpha:
            raise(RuntimeError("PHTrees is computable only from an alpha filtration"))

        if self.pd.degree != self.pd.index_map.dimension - 1:
            raise(RuntimeError("degree should equal dimension - 1"))

        pht = full_ph_tree.PHTrees(self.pd, self.pd.degree)
        pht.construct_tree()
        with open(save_to, "wb") as f:
            full_ph_tree.write_phtree(f, pht, self.pd)

        return PHTrees(save_to)

    def pair(self, nth):
        """Returns `nth` birth-death pairs.

        Args:
            nth (int): Index of the pair.

        Returns:
            :class:`Pair`: The nth pair.
        """
        return Pair(
            self,
            self.pd.masked_birth_indices[nth],
            self.pd.masked_death_indices[nth],
            self.pd.birth_positions[nth] if self.pd.index_map else None,
            self.pd.death_positions[nth] if self.pd.index_map else None
        )

    def pairs(self):
        """Returns all pairs of the PD.

        Returns:
            list of :class:`Pair`: All birth-death pairs.
        """
        return [self.pair(n) for n in range(len(self.pd.births))]

    def nearest_pair_to(self, x, y):
        """Returns a pair closest to `(x, y)`.

        Args:
            x (float): X-coordinate.
            y (float): Y-coordinate.

        Returns:
            :class:`Pair`: The cleosest pair.
        """
        return self.get_spatial_searcher().nearest_pair(x, y)

    def get_spatial_searcher(self):
        if not self.spatial_searcher:
            self.spatial_searcher = SpatialSearcher(self.pairs(), self.births,
                                                    self.deaths)
        return self.spatial_searcher

    def pairs_in_rectangle(self, xmin, xmax, ymin, ymax):
        """Returns all pairs in the rectangle.

        Returns all birth-death pairs whose birth time is in
        the interval [xmin, xmax] and
        whose death time is in [ymin, ymax].

        Args:
           xmin (float): The lower range of birth time.
           xmax (float): The upper range of birth time.
           ymin (float): The lower range of death time.
           ymax (float): The upper range of death time.

        Returns:
           list of :class:`Pair`: All birth-death pairs in the rectangle.
        """
        return self.get_spatial_searcher().in_rectangle(xmin, xmax, ymin, ymax)

    @staticmethod
    def empty():
        """Returns a persistence diagram which has no birth-death pairs.

        Returns:
            PD: A PD object with no birth-death pair.
        """
        return PD("", homdiag.PD.empty_pd())

    def slice_histogram(self, x1, y1, x2, y2, width, bins=100):
        """Returns 1D histogram of birth-death pairs in a thin strip.

        This method computes a 1D hitogram of birth-death pairs
        in the thin strip whose center line is
        `(x1, y1) - (x2, y2)` and whose width is `width`.

        Args:
            x1 (float): The x(birth)-coordinate of the starting point.
            y1 (float): The y(death)-coordinate of the starting point.
            x2 (float): The x(birth)-coordinate of the ending point.
            y2 (float): The y(death)-coordinate of the ending point.
            width (float): Width of the strip.
            bins (int): The number of bins.

        Returns:
            :class:`SliceHistogram`: The histogram.
        """
        transl, mat = plot_PD_slice.transform_to_x_axis(
            np.array([x1, y1]), np.array([x2, y2])
        )
        xy = np.dot(mat, np.array([self.births, self.deaths]) - transl.reshape(2, 1))
        mask = (xy[0, :] >= 0) & (xy[0, :] <= 1) & (np.abs(xy[1, :]) < width / 2)
        values, edges = np.histogram(xy[0, mask], bins, (0, 1))
        return SliceHistogram(values, edges, x1, y1, x2, y2)

    def load_boundary_map(self):
        if self.pd.boundary_map_dict:
            return
        with open(self.path, "rb") as f:
            unpacker = msgpack.Unpacker(f, raw=False)
            unpacker.skip()
            self.pd.boundary_map_dict = next(unpacker)

    @utils.once_cache
    def optimal_1_cycle_finder(self):
        return pict_opt1cyc.Finder(self.pd)


class SliceHistogram(object):
    """
    This class represents a 1D histogram of birth-death pairs
    in the thin strip on a persistence diagram.

    You can create an instance by :meth:`PD.slice_histogram`.

    Attributes:
       values (numpy.ndarary): The histogram values.
       x1 (float): The x-coordinate of the one end of the strip.
       y1 (float): The y-coordinate of the one end of the strip.
       x2 (float): The x-coordinate of the another end of the strip.
       y2 (float): The y-coordinate of the another end of the strip.
    """

    def __init__(self, values, edges, x1, y1, x2, y2):
        self.values = values
        self.edges = edges
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def plot(self, left_label=None, right_label=None, logscale=False, ax=None):
        """
        Plots the historam.

        Args:
            left_label (string): The label text at (x1, y1)
            right_label (string): The label text at (x2, y2)
            logscale (bool): Linear scale is used if False, and
               Log scale is used if True.
            ax (matplotlib.axes.Axes or None):
                The axes to be plotted on. By default (if None),
                `matplotlib.pyplot.gca()` is used.
        """
        ax = ax or plt.gca()
        width = self.edges[1] - self.edges[0]
        ax.bar(self.edges[:-1], self.values, width=width, align="edge", log=logscale)
        ax.set_xlim(-width / 2, 1 + width / 2)
        ax.set_xticks([0, 1])
        ax.set_xticklabels([
            plot_PD_slice.construct_label(left_label, self.x1, self.y1),
            plot_PD_slice.construct_label(right_label, self.x2, self.y2),
        ])


class Pair(object):
    """
    A class representing a birth-death pair.

    Attributes:
        diagram (:class:`PD`): The diagram which the birth-death pair
            belongs to.

    """

    def __init__(self, diagram, birth_index, death_index,
                 birth_position, death_position):
        self.diagram = diagram
        self.index_map = self.diagram.pd.index_map
        self._geom_resolver = None
        self.birth_index = birth_index
        self.death_index = death_index
        self.birth_position = birth_position
        self.death_position = death_position

    @property
    def geom_resolver(self):
        if not self._geom_resolver:
            self._geom_resolver = self.index_map.geometry_resolver(self.diagram)
        return self._geom_resolver

    @property
    def birth_position_symbols(self):
        return self.geom_resolver.cell_symbols(self.birth_index)

    @property
    def death_position_symbols(self):
        return self.geom_resolver.cell_symbols(self.death_index)

    def __iter__(self):
        return (self.birth_time(), self.death_time()).__iter__()

    def birth_time(self):
        """Returns the birth time of the pair.

        Returns:
            float: The birth time
        """
        return self.index_map.levels[self.birth_index]

    def death_time(self):
        """Returns the death time of the pair.

        Returns:
            float: The death time
        """
        return self.index_map.levels[self.death_index]

    #: float: The birth time
    birth = property(birth_time)
    #: float: The death time
    death = property(death_time)

    @property
    def birth_pos(self):
        """The birth position
        """
        return self.birth_position

    @property
    def death_pos(self):
        """The death position
        """
        return self.death_position

    def optimal_volume(self, cutoff_radius=None, solver=None,
                       constrain_birth=False, num_retry=4,
                       integer_programming=False):
        """Return the optimal volume of the pair.

        Args:
            cutoff_radius (float or None):
                The cutoff radius. Simplices which are further from
                the center of birth and death simplices than
                `cutoff_radius` are ignored for the computation of
                an optimal volume. You can reduce the computation time
                if you set the `cutoff_radius` properly.
                Too small `cutoff_radius` causes the failure of the computation.
                If this argument is None, all simplices are not ignored.
            solver (string or None): The name of the LP solver.
                The default solver (coinor Clp) is selected if None is given.
            constrain_birth (bool): Now this value is not used.
            num_retry (int): The number of retry.
                The cutoff_radius is doubled at every retrial.
            integer_programming (bool): Integer constrains are used if True.
                Integer constrains make the computation slower, but
                possibly you get a better result.
        Returns:
            :class:`OptimalVolume`: The optimal volume.
        """
        self.diagram.load_boundary_map()
        vocfinder = VolumeOptimalCycleFinder(
            self.diagram.pd, self.diagram.pd.degree, cutoff_radius,
            solver, constrain_birth, num_retry, integer_programming
        )
        query = optvol.IndexQuery(
            self.birth_index, self.death_index, vocfinder, self.index_map
        )

        try:
            query.invoke()
        except optvol.OptimalVolumeError as err:
            raise VolumeNotFound(err.message, err.code)

        return OptimalVolume(self.diagram, query.results[0].optimal_volume, query)

    def tightened_volume(self, threshold, cutoff_radius=None, solver=None,
                         constrain_birth=False, num_retry=4,
                         integer_programming=False):
        """Returns the tightend volume of the pair.

        Args:
            threshold (float): Positive float for tightening.
            cutoff_radius (float or None):
                The cutoff radius. Simplices which are further from
                the center of birth and death simplices than
                `cutoff_radius` are ignored for the computation of
                an optimal volume. You can reduce the computation time
                if you set the `cutoff_radius` properly.
                Too small `cutoff_radius` causes the failure of the computation.
                If this argument is None, all simplices are not ignored.
            solver (string or None): The name of the LP solver.
                The default solver (coinor Clp) is selected if None is given.
            constrain_birth (bool): Now this value is not used.
            num_retry (int): The number of retry.
                The cutoff_radius is doubled at every retrial.
            integer_programming (bool): Integer constrains are used if True.
                Integer constrains make the computation slower, but
                possibly you get a better result.
        Returns:
            :class:`TightenedVolume`: The tightened volume.
        """
        self.diagram.load_boundary_map()
        vocfinder = VolumeOptimalCycleFinder(
            self.diagram.pd, self.diagram.pd.degree, cutoff_radius,
            solver, constrain_birth, num_retry, integer_programming
        )
        query = optvol.IndexQuery(
            self.birth_index, self.death_index, vocfinder, self.index_map,
            no_optimal_volume=True, tightened_volume=threshold
        )
        query.invoke()
        return TightenedVolume(self.diagram, query.results[0].tightened_volume)

    def optimal_1_cycle(self):
        """Returns the optimal (not volume-optimal) 1-cycle
        corresponding to the birth-death pair.

        This method is available only for a bitmap filtration.

        Returns:
            :class:`Optimal1CycleForBitmap`: The optimal 1-cycle.

        Raises:
            AssertionError: Raised if the filtration is not a bitmap filtration
                or the degree of the pair is not 1.
        """
        assert self.index_map.type() == index_map.MapType.bitmap
        assert self.degree == 1
        result = self.diagram.optimal_1_cycle_finder().query_pair(
            self.birth_index, self.death_index
        )
        return Optimal1CycleForBitmap(result)

    def __eq__(self, other):
        return (isinstance(other, Pair) and
                self.diagram == other.diagram and
                self.birth_index == other.birth_index and
                self.death_index == other.death_index)

    def __repr__(self):
        return "Pair({}, {})".format(self.birth_time(), self.death_time())

    def lifetime(self):
        """The lifetime of the pair.

        Returns:
            float: The lifetime (death - birth) of the pair.
        """
        return self.death_time() - self.birth_time()

    def __hash__(self):
        return(id(self.diagram) + (int(self.birth_index) << 20) +
               (int(self.death_index) << 28))

    @property
    def degree(self):
        """The degree of the pair.
        """
        return self.diagram.degree


@forwardable()
class Volume(object):
    """
    This class represents a volume.
    This is the superclass of OptimalVolume, TightendVolume,
    TightedSubvolume, and OwnedVolume.

    Notes:
        * point: list of float
        * cell: simplex or cube, simplex is used if the filtration is
          simplicial (alpha filtration) and cube is used if the filtration
          is cubical.
        * simplex: list of point
        * cube: tuple[point, list of bool],
        * ssimplex: list of string

    Methods:
        birth_time()
            Returns:
                float: The birth time.

        death_time()
            Returns:
                float: The death time.

        points()
            Returns:
                list of point: All vertices in the optimal volume.

        boundary_points()
            Returns:
                list of point: All vertices in the volume optimal cycle.

        boundary()
            Returns:
                list of cells: All cells in the volume optimal cycle.

        death_position()
            Returns:
                simplex: The death simplex.

        points_symbols()
            Returns:
                list of string: All vertices in the optimal volume
                in the form of the symbolic representation.

        volume_simplices_symbols()
            Returns:
                list of ssimplex: All simplices in volume optimal cycles
                in the form of the symbolic representation.

        boundary_points_symbols()
            Returns:
                list of string: All vertices in the volume optimal cycle
                in the form of the symbolic representation.

        boundary_symbols()
            Returns:
                list of ssimplex: All simplices in the volume optimal cycle
                in the form of the symbolic representation.
    """

    def __init__(self, diagram, optimal_volume):
        self.diagram = diagram
        self.optimal_volume = optimal_volume
        self.geometry_resolver = diagram.pd.geometry_resolver()

    def_delegators("optimal_volume", "points,boundary_points,boundary,"
                   "birth_time,death_time,death_position,"
                   "points_symbols,volume_simplices_symbols,boundary_symbols,"
                   "boundary_points_symbols")

    def birth_time(self):
        """Returns the birth time.
        """
        return self.optimal_volume.birth_time()

    def death_time(self):
        """Returns the death time.
        """
        return self.optimal_volume.death_time()

    def simplices(self):
        """
        Returns:
            list of simplex: All simplices in volume optimal cycles.
        """
        return self.optimal_volume.volume_simplices()

    def cubes(self):
        """
        Returns:
            list of cube: All cubes in volume optimal cycles.
        """
        return self.optimal_volume.volume_cubes()

    def lifetime(self):
        """
        Returns:
            float: The lifetime of the pair.
        """
        return self.death_time() - self.birth_time()

    def children(self):
        """
        Returns:
           list of :class:`Pair`: All children pairs.
        """
        return [
            Pair(self.diagram, birth, death,
                 self.geometry_resolver.cell_coords(birth),
                 self.geometry_resolver.cell_coords(death))
            for (birth, death) in self.optimal_volume.children_pairs
        ]

    def to_dict(self):
        """
        Returns:
            dict: The information about the optimal volume.
        """
        return self.optimal_volume.to_jsondict()

    #: The alias of :meth:`death_position`.
    death_pos = death_position

    def pair(self):
        """
        Returns the corresponding birth-death pair by :class:`Pair`.
        """
        return Pair(self.diagram,
                    self.optimal_volume.birth,
                    self.optimal_volume.death,
                    self.optimal_volume.birth_position(),
                    self.optimal_volume.death_position())

    def to_paraview_node(self, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize an optimal volume.

        You can show the optimal volume by
        :meth:`homcloud.paraview_interface.show`. You can also
        adjust the visual by the methods of
        :class:`homcloud.paraview_interface.PipelineNode`.

        Args:
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """
        return OptimalVolume.to_paraview_node_for_volumes([self], gui_name)

    to_pvnode = to_paraview_node

    @staticmethod
    def to_paraview_node_for_volumes(volumes, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize multiple optimal volumes.

        All optimal volumes should come from the same :class:`PD` object.

        Args:
            volumes (list of :class:`OptimalVolume`): The optimal volumes to be
                visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """
        drawer = optvol.prepare_drawer_for_paraview(volumes[0].diagram.pd)
        for i, volume in enumerate(volumes):
            volume.optimal_volume.draw(drawer, str(i))
        path = tempfile(".vtk")
        drawer.output(path)
        return pv_interface.VTK(path, gui_name).set_representation("Wireframe")


@forwardable()
class OptimalVolume(Volume):
    """
    This class represents an optimal volume.

    Methods:
        birth_position()
            Returns:
                simplex: The birth simplex.
    """

    def __init__(self, diagram, optimal_volume, query):
        super().__init__(diagram, optimal_volume)
        self.query = query

    def_delegators("optimal_volume", "birth_position")

    #: The alias of :meth:`birth_position`.
    birth_pos = birth_position

    def tightened_subvolume(self, threshold):
        """
        Returns the tightened subvolume of the optimal volume.

        Args:
            threshold (float): The threshold of the tightened subvolume.
        Returns:
            TightenedSubvolume: The tightened subvolume.
        """
        self.query.tightened_subvolume = threshold
        subvolume = self.query.query_tightened_subvolume(self.optimal_volume)
        return TightenedSubvolume(self.diagram, subvolume)

    def owned_volume(self, threshold, connected):
        """
        Returns the owned volume of the optimal volume.

        Args:
            threshold (float): The threshold of the owned volume.
        Returns:
            OwnedVolume: The owned volume.
        """
        self.query.owned_volume = threshold
        self.query.owned_volume_connected_component = connected
        owned_volume = self.query.query_owned_volume(self.optimal_volume, None)
        return OwnedVolume(self.diagram, owned_volume)


@forwardable()
class EigenVolume(Volume):
    """
    This class represents an "eigenvolume". It is the superclass of
    TightenedVolume, TightenedSubvolume and OnwedVolume.

    Attributes:
        threshold (float): The threshold used for the computation of the
            eigenvolume.
    """
    def_delegators("optimal_volume", "threshold")


class TightenedVolume(EigenVolume):
    """
    This class represents a tightened volume.

    The instance is given by :meth:`Pair.tightened_volume`.
    """
    pass


class TightenedSubvolume(EigenVolume):
    """
    This class represents a tightened subvolume.

    The instance is given by :meth:`OptimalVolume.tightened_subvolume`.
    """
    pass


class OwnedVolume(EigenVolume):
    """
    This class represents an onwned volume.

    The instance is given by :meth:`OptimalVolume.owned_volume`.
    """
    pass


class Optimal1CycleForBitmap(object):
    """The class represents an optimal (not volume-optimal) 1-cycle.

    Computing volume-optimal cycle is very expensive for 3-D and
    higher dimensional cubical filtration. To fight against such
    a huge filtration, :meth:`Pair.optimal_1_cycle` is available.
    This method returns an instance of this class.
    """

    def __init__(self, orig):
        self.orig = orig

    def birth_time(self):
        """
        Returns:
            float: The birth time.
        """
        return self.orig.birth_time

    def death_time(self):
        """
        Returns:
            float: The death time.
        """
        return self.orig.death_time

    def birth_position(self):
        """
        Returns:
            tuple of float*N: The coordinate of birth position. (N: dimension)
        """
        return self.orig.path[0]

    def path(self):
        """
        Returns the path (loop) of the optimal 1-cycle.

        The first item and the last item is the same as :meth:`birth_position`.

        Returns:
            list of coord: The list of vertices of the loop ordered by the path
        """
        return self.orig.path

    def boundary_points(self):
        """
        Returns:
            list of coord: The list of vertices in the loop. Any vertex
                in the list is unique.
        """
        return self.orig.boundary_points()

    def to_paraview_node(self, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize an optimal 1-cycle.

        You can show the optimal 1-cycle by
        :meth:`homcloud.paraview_interface.show`. You can also
        adjust the visual by the methods of
        :class:`homcloud.paraview_interface.PipelineNode`.

        Args:
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """
        return self.to_paraview_node_for_1cycles([self], gui_name)

    @staticmethod
    def to_paraview_node_for_1cycles(cycles, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode` object
        to visulize multiple optimal 1-cycles.

        Args:
            cycles (list of :class:`Optimal1CycleForBitmap`):
                The optimal 1-cycles to be visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.PipelineNode: A PipelineNode object.
        """

        drawer = pict_opt1cyc.prepare_drawer_for_paraview(len(cycles))
        for i, cycle in enumerate(cycles):
            cycle.orig.draw(drawer, i, str(i))
        path = tempfile(".vtk")
        drawer.output(path)
        return pv_interface.VTK(path, gui_name).set_representation("Wireframe")

    to_pvnode = to_paraview_node
    to_pvnode_for_1cycle = to_paraview_node_for_1cycles


@forwardable()
class Histogram(object):
    """The class represents a histogram on birth-death plane.

    Methods:
        x_range()
            Returns:
                (tuple[int, int]): The lower and upper range of x-axis.

        x_bins()
            Returns:
                (int): The number of bins on x-axis.

        y_range()
            Returns:
                (tuple[int, int]): The lower and upper range of y-axis.
        y_bins()
            Returns:
                (int): The number of bins on y-axis.

    Attributes:
        xedges (numpy.ndarray[x_bins + 1]): The edges of bins on x-axis
            in ascending order.
        yedges (numpy.ndarray[y_bins + 1]): The edges of bins on y-axis
            in ascending order.

    """

    def __init__(self, orig):
        self.orig = orig

    @property
    def values(self):
        """
        (numpy.ndarary, shape (x_bins, y_bins)): 2-dimensional array of values
        in the bins.
        """
        return self.orig.values

    @values.setter
    def values(self, values):
        self.orig.values = values

    def_delegators('orig', 'x_range,y_range,x_bins,y_bins,xedges,yedges')

    def plot(self, colorbar={}, style="colorhistogram", title="",
             unit_name=None, font_size=None, aspect="equal", ax=None,
             levels=None):
        """Plot a histogram by matplotlib.

        Args:
            colorbar (dict): The specification of the histogram colors and
                the colorbar.

                The following fields are available for this dictionary.

                * "type" - The name of colorbar type. One of the followings
                  is available. The default type is "linear".

                  * "linear" - linear scale
                  * "log" - log scale
                  * "loglog" - log(log(n+1)+1)
                  * "linear-midpoint" - linear scale with midpoint.
                    You should specify the value of midpoint
                    by the "midpoint" field.
                  * "power" - n^p. You should specify p by "p" field.
                * "min" - The minimum of the colorbar. If this value is not
                  specified, the value is determined by the minimum of
                  histogram values.
                * "max" - The maximum of the colorbar. If this value is not
                  specified, the value is determined by the maximum of
                  histogram values.

            style (string): The plotting style. "colorhistogram" or "contour"
                is available.
            title (string): The title of the output figure.
            unit_name (string or None): The unit name of the x-axis
                and y-axis.
            font_size (float or None): The font size.
                The font size is automatically determined if None is given.
            aspect (string): The X-Y aspect. "equal" or "auto" is available.
            ax (matplotlib.axes.Axes or None):
                The axes to be plotted on. By default (if None),
                `matplotlib.pyplot.subplot()` is used.
            levels (list of floats or None):
                The levels for coutour plotting. This argument is used
                only if `style` is "contour".

        Example:
            >>> import matplotlib.pyplot as plt
            >>>    :
            >>> histogram.plot(colorbar={"type": "log", "max": 100},
            >>>                title="Title string")
            >>> plt.show()  # To show the histogram on your display
            >>> plt.savefig("histogram.png")  # To save the histogram figure.
        """
        plotter = plot_PD.PDPlotter.find_plotter(style)(
            self.orig, self._zspec(colorbar), plot_PD.AuxPlotInfo(
                title, unit_name, font_size, aspect
            )
        )
        if levels is not None:
            plotter.levels = levels

        plotter.plot(*self._fig_ax(ax))

    @staticmethod
    def _zspec(colorbar):
        type = colorbar.get("type", "linear")
        vmax = colorbar.get("max")
        vmin = colorbar.get("min")
        if "colormap" in colorbar:
            colormap = plt.get_cmap(colorbar["colormap"])
        else:
            colormap = None
        if type == "linear":
            return plot_PD.ZSpec.Linear(vmax, vmin, colormap)
        elif type == "log":
            return plot_PD.ZSpec.Log(vmax, vmin, colormap)
        elif type == "loglog":
            return plot_PD.ZSpec.LogLog(vmax, vmin, colormap)
        elif type == "linear-midpoint":
            return plot_PD.ZSpec.LinearMidPoint(colorbar["midpoint"],
                                                vmax, vmin, colormap)
        elif type == "power":
            return plot_PD.ZSpec.Power(colorbar["p"], vmax, vmin, colormap)
        else:
            raise(RuntimeError("unknown colorbar type: {}").format(type))

    @staticmethod
    def _fig_ax(ax):
        if ax is None:
            return plt.subplots()
        else:
            return (ax.get_figure(), ax)


class PHTrees(object):
    """
    This class represents PH trees computed from an alpha filtration.

    Please see `<https://arxiv.org/abs/1712.05103>`_ if you want to know
    the details of optimal volumes and volume optimal cycles.

    You can compute the PH trees by :meth:`PD.phtrees`.

    Args:
        path (string): The filepath.

    Example:
        >>> import homcloud.interface as hc
        >>> pointcloud = hc.example_data("tetrahedron")
        >>> pdlist = hc.PDList.from_alpha_filtration(pointcloud)
        >>> # Computes PH trees and save them in "tetrahedron.pht"
        >>> pdlist.dth_diagram(2).phtrees(save_to="tetrahedron.pht")
        >>> # Load the file.
        >>> phtrees = hc.PHTrees("tetrahedron.pht")
        >>> # Query the node whose birth-death pair is nearest to (19, 21).
        >>> node = phtrees.node_nearest_to(19, 21)
        >>> # Show birth time and death time
        >>> node.birth_time()
        19.600000000000005
        >>> node.death_time()
        21.069444444444443
        >>> node.boundary_points()
        [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]]
        >>> node.boundary()
        [[[0.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]],
         [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [5.0, 6.0, 0.0]],
         [[8.0, 0.0, 0.0], [5.0, 6.0, 0.0], [4.0, 2.0, 6.0]],
         [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [4.0, 2.0, 6.0]]]

    """

    def __init__(self, path):
        self.path = path
        self.resolver = None

    def save(self, dest):
        """
        Saves the data file to `dest`.

        Args:
            dest (string): The filepath.
        """
        shutil.copyfile(self.path, dest)

    def _resolver(self):
        if self.resolver is None:
            with open(self.path, "rb") as f:
                self.resolver = full_ph_tree.TreeResolver.load(f, self.Node)
        return self.resolver

    def nodes_of(self, pairs):
        """
        Returns the nodes of trees corresponding to birth-death pairs
        in `pairs`.

        Args:
            pairs (list of Pair): The list of pairs.

        Returns:
            list of :class:`PHTrees.Node`: The nodes.
        """
        return [self._resolver().phtree.nodes[pair.death_index]
                for pair in pairs]

    def pair_node_nearest_to(self, x, y):
        """
        Return the node corresponding the pair which is nearest to
        (`x`, `y`).

        Args:
            x (float): The birth-axis coordinate.
            y (float): The death-axis coordinate.

        Returns:
            PHTrees.Node: The nearest node.

        """
        return self._resolver().query_node(x, y)

    def pair_nodes_in_rectangle(self, xmin, xmax, ymin, ymax):
        """
        Returns the list of nodes corresponding to the birth-death
        pairs in the given rectangle.

        Args:
           xmin (float): The minimum of the birth-axis of the rectangle.
           xmax (float): The maximum of the birth-axis of the rectangle.
           ymin (float): The minimum of the death-axis of the rectangle.
           ymax (float): The maximum of the death-axis of the rectangle.

        Returns:
           list of :class:`PHTrees.Node`: The nodes in the rectangle.

        """
        return self._resolver().query_nodes_in_rectangle(xmin, xmax,
                                                         ymin, ymax)

    def to_paraview_node_from_nodes(self, nodes, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode`
        object to visulize optimal volumes of the nodes.

        Args:
            nodes (list of :class:`PHTrees.Node`): The list of nodes to be visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.VTK: Paraview Pipeline node object.

        Notes:
            All nodes should be nodes of `self` PHTrees.
        """
        path = tempfile(".vtk")
        self._resolver().draw_volumes_of_nodes(nodes, path, True, True)
        return pv_interface.VTK(path, gui_name).set_representation("Wireframe")

    to_pvnode_from_nodes = to_paraview_node_from_nodes

    class Node(full_ph_tree.PHTreesForQuery.Node):
        """
        The class represents a tree node of :class:`PHTrees`.

        Methods:
            birth_time()
                Returns:
                    float: The birth time of the corresponding birth-death pair.

            death_time()
                Returns:
                    float: The death time of the corresponding birth-death pair.

            lifetime()
                Returns:
                    float: The lifetime of the corresponding birth-death pair.

            points()
                Returns:
                    list of list of float, a.k.a list of points:
                        Points in the optimal volume.

            simplices()
                Returns:
                    list of list of list of float, a.k.a list of simplex:
                        The simplices in the optimal volume.

            boundary()
                Returns:
                    list of list of float, a.k.a. list of points:
                        Points in the volume optimal cycle.

            boundary_points()
                Returns:
                    list of list of float, a.k.a list of points:
                        Points in the volume optimal cycle.

            points_symbols()
                Returns:
                    list of string: All vertices in the optimal volume
                    in the form of the symbolic representation.

            volume_simplices_symbols()
                Returns:
                    list of list of string: All simplices in volume optimal cycles
                    in the form of the symbolic representation.

            boundary_points_symbols()
                Returns:
                    list of string: All vertices in the volume optimal cycle
                    in the form of the symbolic representation.

            boundary_symbols()
                Returns:
                    list of list of string: All simplices in the volume optimal cycle
                    in the form of the symbolic representation.

            birth_position()
                Returns the birth simplex.

            death_position()
                Returns the death simplex.

            ancestors()
                Returns:
                    list of :class:`PHTrees.Node`:
                        The ancestors of the tree node include itself.
        """

        def stable_volume(self, epsilon):
            """
            Args:
                epsilon (float): Duration noise strength

            Returns:
                PHTrees.StableVolume: The stable volume

            """
            return super().stable_volume(epsilon, PHTrees.StableVolume)

        def to_paraview_node(self, gui_name=None):
            """
            Construct a :class:`homcloud.paraview_interface.PipelineNode`
            object to visulize an optimal volume of the node.

            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

            Returns:
                homcloud.paraview_interface.VTK: Paraview Pipeline node object.
            """
            path = tempfile(".vtk")
            self.draw_descendants_volumes(self.index_map.points,
                                          path, False, False)
            return pv_interface.VTK(path, gui_name) \
                               .set_representation("Wireframe")

        to_pvnode = to_paraview_node

    class StableVolume(full_ph_tree.PHTreesForQuery.StableVolume):
        """
        The class represents a tree node of :class:`PHTrees`.

        Methods:
            birth_time()
                Returns:
                    float: The birth time of the corresponding birth-death pair.

            death_time()
                Returns:
                    float: The death time of the corresponding birth-death pair.

            lifetime()
                Returns:
                    float: The lifetime of the corresponding birth-death pair.

            points()
                Returns:
                    list of list of float, a.k.a list of points:
                        Points in the optimal volume.

            simplices()
                Returns:
                    list of list of list of float, a.k.a list of simplex:
                        The simplices in the optimal volume.

            boundary()
                Returns:
                    list of list of float, a.k.a. list of points:
                        Points in the volume optimal cycle.

            boundary_points()
                Returns:
                    list of list of float, a.k.a list of points:
                        Points in the volume optimal cycle.

            points_symbols()
                Returns:
                    list of string: All vertices in the optimal volume
                    in the form of the symbolic representation.

            volume_simplices_symbols()
                Returns:
                    list of list of string: All simplices in volume optimal cycles
                    in the form of the symbolic representation.

            boundary_points_symbols()
                Returns:
                    list of string: All vertices in the volume optimal cycle
                    in the form of the symbolic representation.

            boundary_symbols()
                Returns:
                    list of list of string: All simplices in the volume optimal cycle
                    in the form of the symbolic representation.

        """

        def to_paraview_node(self, gui_name=None):
            """
            Construct a :class:`homcloud.paraview_interface.PipelineNode` object
            to visulize.

            You can show the volume by
            :meth:`homcloud.paraview_interface.show`. You can also
            adjust the visual by the methods of
            :class:`homcloud.paraview_interface.PipelineNode`.

            Args:
                gui_name (string or None): The name shown in Pipeline Browser
                    in paraview's GUI.

            Returns:
                homcloud.paraview_interface.PipelineNode: A PipelineNode object.

            """
            path = tempfile(".vtk")
            drawer = ParaViewSimplexDrawer(1, self.index_map.points, {})
            self.draw_volume(drawer, 1, dict(), False, False)
            drawer.output(path)
            return pv_interface.VTK(path, gui_name).set_representation("Wireframe")

        to_pvnode = to_paraview_node


class MaskHistogram(Histogram):
    """
    The class represents a histogram on birth-death plane whose values
    are booleans.

    This class is helpful to pick up all birth-death pairs in an area.
    meth:`Mesh.mask_from_vector` and meth:`Mesh.mask_from_2darray` is
    available for this purpose.
    """

    def filter_pairs(self, pairs):
        """
        Returns all pairs in the area of bins whose values are True.

        Args:
            pairs (sequence of :class:`Pair`): Pairs to be filtered.

        Returns:
            list of :class:`Pair`: The filtered pairs.

        Notes:
            In fact, this method can filter the list of :class:`OptimalVolume`
            by their birth and death times.
        """
        return [pair for pair in pairs
                if self.orig.value_at(pair.birth_time(), pair.death_time())]

    def filter_pd(self, pd):
        """
        Returns all pairs of the persistence diagram
        in the area of bins whose values are True.

        Args:
            pd (:class:`PD`): A persistence diagram which has
               pairs to be filtered.

        Returns:
            list of :class:`Pair`: The filtered pairs.
        """

        return self.filter_pairs(pd.pairs())


class Mesh(object):
    """
    This class represents a 2D mesh on the plane of birth-death pairs.

    This class is useful to compute histograms from many diagrams
    with the same setting.

    Args:
        x_range (tuple(float, float) or None): The lower and upper range
            of the bins on x-axis.
        y_range (int): The number of bins on x-axis.
        y_range (tuple(float, float) or None): The lower and upper range
            of the bins on y-axis. Same as `x_range` if None is given.
        y_bins (int or None): The number of bins on y-axis.
            Same as `x_bins` if None is given.
        superlevel (bool): This should be True if your PDs come
            from superlevel filtrations, otherwise this should be False.

    Examples:
        >>> import homcloud.interface as hc
        >>> import matplotlib.pyplot as plt
        >>> pc = np.array([[0, 0, 0], [8, 0, 0], [5, 6, 0], [4, 2, 6],])
        >>> pd = hc.PDList.from_alpha_filtration(pc).dth_diagram(1)
        >>> mesh = hc.Mesh((0, 20), 128)
        >>> histogram = mesh.pd_histogram(pd)
        >>> histogram.plot(colorbar={"type": "log"}, title="1st PD")
        >>> plt.show()
        -> The histogram is displayed.

    """

    def __init__(self, x_range, xbins, y_range=None, ybins=None, pd=None,
                 superlevel=False):
        self.rulers = homdiag.Ruler.create_xy_rulers(x_range, xbins,
                                                     y_range, ybins, pd)
        self.sign_flipped = superlevel
        self._histoinfo = None

    @classmethod
    def from_histoinfo(cls, histoinfo):
        new_mesh = cls((histoinfo["x-edges"][0], histoinfo["x-edges"][-1]),
                       len(histoinfo["x-edges"]) - 1,
                       (histoinfo["y-edges"][0], histoinfo["y-edges"][-1]),
                       len(histoinfo["y-edges"]) - 1,)
        new_mesh._histoinfo = histoinfo
        return new_mesh

    def pd_histogram(self, pd):
        """Constructs a 2D histogram of `pd`.

        Args:
            pd (:class:`PD`): The diagram.

        Returns:
            :class:`Histogram`: The histogram.
        """
        return Histogram(homdiag.PDHistogram(pd, *self.rulers))

    def histogram_from_vector(self, vector):
        """
        Construct a histogram from a vector.

        The histogram is constructed by the rule of persistence image method.

        Args:
            vector (numpy.ndarray): A vector.

        Returns:
            :class:`Histogram`: The histogram.
        """
        return Histogram(homdiag.Histogram.reconstruct_from_vector(
            vector, self.histoinfo()
        ))

    def mask_from_vector(self, vector):
        """
        Construct a mask histogram from a boolean vector.

        The histogram is constructed by the rule of persistence image method.

        Args:
            vector (numpy.ndarray): A boolean vector.

        Returns:
            :class:`MaskHistogram`: The "histogram" whose values in bins are
                True or False.
        """
        return MaskHistogram(homdiag.BinaryHistogram.reconstruct_from_vector(
            vector, self.histoinfo()
        ))

    def mask_from_2darray(self, array):
        return MaskHistogram(homdiag.BinaryHistogram(
            array, self.rulers[0].edges(), self.rulers[1].edges()
        ))

    def vector_size(self):
        """
        Return the size of the vector generated by self.

        Returns:
            int: The size of the vector
        """
        return len(self.histoinfo()["x-indices"])

    def histoinfo(self):
        if not self._histoinfo:
            self._histoinfo = vectorize_PD.histogram_info_dict(
                homdiag.PDHistogram(homdiag.PD.empty_pd(self.sign_flipped), *self.rulers)
            )
        return self._histoinfo


class PIVectorizerMesh(Mesh):
    """
    This class represents a 2D mesh on the plane of birth-death pairs
    with information about vectorization by persistence image (PI) method.

    You can construct PI vectors from diagrams.

    Args:
        x_range (tuple[float, float] or None): The lower and upper range
            of the bins on x-axis.
        xbins (int): The number of bins on x-axis.
        y_range (tuple[float, float] or None): The lower and upper range
            of the bins on y-axis. Same as `x_range` if None is given.
        ybins (int or None): The number of bins on y-axis.
            Same as `x_bins` if None is given.
        weight (tuple or string): The information of the weight function.
            You can use one of the followings:

            * "none": A constant weight function
            * ("atan", `c`, `p`): An arctangent weight function,
              `c` and `p` should be floats. The weight function
              is c*atan((death - birth)**p) .
            * ("linear", `a`): A linear weight function. `a` should be
              a float. The weight function is a*(death - birth) .
        sigma (float): The standard deviation for the Gaussian distribution
            used by PI.
        superlevel (bool): This should be True if your PDs come
            from superlevel filtrations, otherwise this should be False.
            Internally, This parameter should be True if the PD has
            birth-death pairs with birth > death, and otherwise
            the parameter should be False.
    """

    def __init__(self, x_range, xbins, y_range=None, ybins=None,
                 weight=None, sigma=None, superlevel=False):
        super(PIVectorizerMesh, self).__init__(x_range, xbins,
                                               y_range, ybins, None, superlevel)
        self.weight = self.weight_function(weight)
        self.sigma = sigma

    @staticmethod
    def weight_function(params):
        if params == "none":
            return lambda b, d: 1.0
        if isinstance(params, tuple):
            if params[0] == "atan":
                return vectorize_PD.atan_weight_function(params[1], params[2])
            if params[0] == "linear":
                return vectorize_PD.linear_weight_function(1.0 / params[1])
            raise(ValueError("Unknown weight type: {}".format(params[0])))
        return params

    def vectorize(self, pd):
        """Vectroize `pd`.

        Args:
            pd (:class:`PD`): A persistence diagram.

        Returns:
            numpy.ndarray: The vectorized diagram.
        """
        histo = homdiag.PDHistogram(pd, *self.rulers)
        histo.apply_weight(self.weight)
        histo.apply_gaussian_filter(self.sigma)
        assert histo.sign_flipped == self.sign_flipped
        return histo.vectorize()

    def vectorize_pair(self, pair):
        """Vectorize a PD with a signle pair.

        Args:
            pd (:class:`PD` or tuple[double, double]): A birth-death pair

        Returns:
            numpy.ndarray: The vectorized diagram.
        """
        birth_time, death_time = tuple(pair)
        return self.vectorize(homdiag.PD([birth_time], [death_time]))


class BitmapPHTreesPair(object):
    """
    This class represents PH trees (or a merge trees) computed from
    a bitmap data.

    You can compute the PH trees for 0-th and (n-1)-st persistence homology
    from n-dimensional bitmap data.

    This class is named "Pair" because the instance stores
    PH trees for both 0-th and (n-1)-st persistent homology.

    You can compute PH trees by :meth:`from_bitmap_levelset` and
    :meth:`from_bitmap_distance_function`. The computed data can be loaded
    from a file by the constructor

    Args:
        path (string): The filepath of the data file which
            PH trees are stored in.
    """

    def __init__(self, path):
        self._dic = None
        self.path = path

    def sign(self):
        """
        Returns -1 if superlevel filtration. Otherwise returns 1.
        """
        return -1 if self.dic["sign-flipped"] else 1

    def PDList(self):
        """
        Returns:
           class:`PDList`: The persistence diagrams corresponding to
           the PH trees.
        """
        if os.path.splitext(self.path)[1] == "json":
            raise RuntimeError("PDList cannot be created from a json file")
        return PDList(self.path)

    def dim_0_trees(self):
        """
        Returns:
            class:`BitmapPHTrees`: The PH tress for 0-th persistent homology.
        """
        return BitmapPHTrees(self, self.dic["lower"])

    def codim_1_trees(self):
        """
        Returns:
            class:`BitmapPHTrees`: The PH tress for (n-1)-st
            persistent homology.
        """
        return BitmapPHTrees(self, self.dic["upper"])

    @property
    def dic(self):
        if self._dic is not None:
            return self._dic

        _, ext = os.path.splitext(self.path)
        if ext == ".json":
            with open(self.path) as f:
                self._dic = json.load(f)
        else:
            with open(self.path, "rb") as f:
                self._dic = msgpack.load(f, raw=False)

        return self._dic

    @staticmethod
    def from_bitmap_levelset(array, mode="sublevel", save_to=None):
        """Computes a PH trees from 0-th and (n-1)-st persistent homology
        from levelset filtration of the bitmap.

        Args:
            array (numpy.ndarray): The bitmap data.
            mode (string): "superlevel" or "sublevel".
            save_to (string or None): The filepath which the
                PH trees is stored in.

        Returns:
            :class:`BitmapPHTreesPair`: The PH trees pair of 0-th and (n-1)-st
               persistent homology.
        """
        is_superlevel = mode == "superlevel"
        lower, upper = pict_tree.construct_mergetrees(array, is_superlevel)
        dic = pict_tree.construct_dict(array.ndim, is_superlevel, lower, upper)
        save_to = BitmapPHTreesPair._save(dic, save_to)
        return BitmapPHTreesPair(save_to)

    @staticmethod
    def from_bitmap_distance_function(array, signed=False, metric="manhattan",
                                      mask=None, save_to=None):
        """Computes a PH trees fro 0-th and (n-1)-st persistent homology
        from the erosion-dilation filtration (the filtration by (signed)
        distance function) of the bitmap.

        This method is obsolete. Please use the combination of
        :meth:`BitmapPHTreesPair.from_bitmap_levelset` and
        :meth:`distance_transform` instead.

        Args:
            array (numpy.ndarray): The binary bitmap data. The `dtype`
                should be bool.
            signed (bool): The signed distance function is used if True.
                The normal distance function is used if False.
            metric (string): The metric used to compute a filtration.
                You can choose one of the followings:

                * "manhattan"
                * "chebyshev"
                * "euclidean"

            mask (numpy.ndarray or None): The mask bitmap.
            save_to (string or None): The filepath which the
                PH trees is stored in.

        Returns:
            :class:`BitmapPHTreesPair`: The PH trees pair of 0-th and (n-1)-st
                 persistent homology.
        """
        # warnings.warn(
        #     "interface.BitmapPHTreesPair.from_bitmap_distance_function is obsolete."
        #     "Please use interaface.distance_transform and BitmapPHTreesPair.",
        #     PendingDeprecationWarning
        # )
        array = binarize.distance_transform(array, metric, signed, mask)
        lower, upper = pict_tree.construct_mergetrees(array, False)
        dic = pict_tree.construct_dict(array.ndim, False, lower, upper)
        save_to = BitmapPHTreesPair._save(dic, save_to)
        return BitmapPHTreesPair(save_to)

    @staticmethod
    def _save(dic, save_to):
        if save_to is None:
            save_to = tempfile(".p2mt")
        _, ext = os.path.splitext(save_to)
        if ext == ".json":
            with open(save_to, "w") as f:
                json.dump(dic, f)
        else:
            with open(save_to, "wb") as f:
                msgpack.dump(dic, f)
        return save_to


class BitmapPHTrees(object):
    """
    This class represents PH trees computed from a bitmap filtration.

    You can create an instance of this class
    by :meth:`BitmapPHTreesPair.dim_0_trees` or
    :meth:`BitmapPHTreesPair.codim_1_trees`.

    Attributes:
        nodes (list of :class:`BitmapPHTrees.Node`): All nodes
        essential_nodes (list of :class:`BitmapPHTrees.Node`): All essential nodes
        nonessential_nodes (list of :class:`BitmapPHTrees.Node`): All nonessential nodes
    """

    def __init__(self, treespair, dic):
        self.treespair = treespair
        self.dic = dic
        self.nodes = [
            self.Node(self, d) for d in self.dic["nodes"].values()
            if d["birth-time"] != d["death-time"]
        ]
        self.essential_nodes = [node for node in self.nodes if node.essential()]
        self.nonessential_nodes = [node for node in self.nodes if not node.essential()]
        self.spatial_searcher = self.build_spatial_searcher()

    def build_spatial_searcher(self):
        noness_nodes = [node for node in self.nodes if not node.essential()]
        births = np.array([node.birth_time() for node in noness_nodes])
        deaths = np.array([node.death_time() for node in noness_nodes])
        return SpatialSearcher(noness_nodes, births, deaths)

    def degree(self):
        """
        Returns:
            int: The degree of the persistent homology.
        """
        return self.dic["degree"]

    def nearest_pair_node(self, x, y):
        """
        Searches a tree node corresponding the birth-death pair
        nearest to (x, y).

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
        Returns:
            :class:`BitmapPHTrees.Node`: The node.
        """
        return self.spatial_searcher.nearest_pair(x, y)

    def pair_nodes_in_rectangle(self, xmin, xmax, ymin, ymax):
        """
        Searches tree nodes corresponding the birth-death pairs
        which the given rectangle contains.

        Args:
            xmin (float): The left side of the rectangle.
            xmax (float): The right side of the rectangle.
            ymin (float): The bottom side of the rectangle.
            ymax (float): The top side of the rectangle.

        Returns:
            list of :class:`BitmapPHTrees.Node`: The nodes.
        """

        return self.spatial_searcher.in_rectangle(xmin, xmax, ymin, ymax)

    class Node(object):
        """
        This class represents a tree node of PH trees for a bitmap filtration.

        You can draw the optimal volume corresponding to the node
        on an image by :meth:`draw_volumes_on_2d_image`.
        """

        def __init__(self, mt, dic):
            self.mt = mt
            self.dic = dic

        def birth_time(self):
            """
            Returns:
                float: The birth time.
            """
            return self.dic["birth-time"]

        def death_time(self):
            """
            Returns:
                float: The death time. May be infinity.
            """
            if not self.essential():
                return self.dic["death-time"]
            return self.mt.treespair.sign() * np.inf

        def lifetime(self):
            """
            Returns:
                float: The lifetime of the pair.
            """
            return self.death_time() - self.birth_time()

        def birth_position(self):
            """Returns the birth pixel.

            Returns:
               list of int: The coordinate of the birth pixel.
            """
            return self.dic["birth-pixel"]

        def death_position(self):
            """Returns the death pixel.

            Returns:
               list of int: The coordinate of the death pixel.
            """
            return self.dic["death-pixel"]

        def volume(self):
            """
            Returns the optimal volume.

            In fact, for degree 0 node, this method returns
            optimal 0-cohomological volume (this means
            maximal connected conponents in the filtration)
            and for degree (n-1),
            this method returns optimal (n-1)-homological volume.
            This fact is quite mathematical problem, so if you feel that
            it is too difficult to understand, you can ignore the fact.
            You can understand the volume information without the understanding
            of such mathematical background.

            Returns:
                list of list of int: The coordinates of all pixels
                in the optimal volume.
            """
            return self.dic["volume"]

        def stable_volume(self, epsilon):
            """
            Args:
                epsilon (float): Duration noise strength

            Returns:
                BitmapPHTrees.StableVolume: The stable volume

            """
            return BitmapPHTrees.StableVolume(self, epsilon)

        def essential(self):
            """
            Returns:
                bool: True if the death time is infinity.
            """
            return self.dic["death-time"] is None

        def parent(self):
            """
            Returns:
                BitmapPHTrees.Node: The parent node of the node in the PH tree.
            """
            parent_id = self.dic["parent"]
            return BitmapPHTrees.Node(self.mt,
                                      self.mt.dic["nodes"][parent_id])

        def is_trivial(self, id):
            dic = self.mt.dic["nodes"][id]
            return dic["birth-time"] == dic["death-time"]

        def children(self):
            """
            Returns:
                list of :class:`BitmapPHTrees.Node`: All children nodes.
            """
            return [
                BitmapPHTrees.Node(self.mt, self.mt.dic["nodes"][child_id])
                for child_id in self.dic["children"] if not self.is_trivial(child_id)
            ]

        def __eq__(self, other):
            return ((self.mt == other.mt) and
                    (self.dic["id"] == other.dic["id"]))

        def __repr__(self):
            return "BitmapPHTrees.Node({}, {})".format(self.birth_time(), self.death_time())

        def to_paraview_node(self, gui_name=None):
            """
            Construct a :class:`homcloud.paraview_interface.PipelineNode` object
            to visulize :meth:`volume`.

            You can show the volume by
            :meth:`homcloud.paraview_interface.show`. You can also
            adjust the visual by the methods of
            :class:`homcloud.paraview_interface.PipelineNode`.

            Args:
                gui_name (string or None): The name shown in Pipeline Browser
                    in paraview's GUI.

            Returns:
                homcloud.paraview_interface.PipelineNode: A PipelineNode object.
            """
            return BitmapPHTrees.to_paraview_node_from_nodes([self], gui_name)

        to_pvnode = to_paraview_node

    class StableVolume(object):
        def __init__(self, node, epsilon):
            self.node = node
            self._volume = set(tuple(p) for p in node.dic["volume"])
            for child_id in node.dic["children"]:
                child_dic = node.mt.dic["nodes"][child_id]
                if self.is_unstable_child(child_dic, epsilon):
                    self._volume.difference_update(tuple(p) for p in child_dic["volume"])

        def is_unstable_child(self, child_dic, epsilon):
            is_sublevel = self.node.mt.treespair.sign() == 1
            is_lower = self.node.mt.degree() == 0
            if is_lower and is_sublevel:
                return child_dic["death-time"] > self.node.death_time() - epsilon
            elif is_lower and not is_sublevel:
                return child_dic["death-time"] < self.node.death_time() + epsilon
            elif not is_lower and is_sublevel:
                return child_dic["birth-time"] < self.node.birth_time() + epsilon
            elif not is_lower and not is_sublevel:
                return child_dic["birth-time"] > self.node.birth_time() - epsilon

        def volume(self):
            """
            Returns the pixels of the stable volume.

            Returns:
                set of tuple(int,...): The coordinates of all pixels.
            """
            return self._volume

        def to_paraview_node(self, gui_name=None):
            """
            Construct a :class:`homcloud.paraview_interface.PipelineNode` object
            to visulize :meth:`volume`.

            You can show the volume by
            :meth:`homcloud.paraview_interface.show`. You can also
            adjust the visual by the methods of
            :class:`homcloud.paraview_interface.PipelineNode`.

            Args:
                gui_name (string or None): The name shown in Pipeline Browser
                    in paraview's GUI.

            Returns:
                homcloud.paraview_interface.PipelineNode: A PipelineNode object.
            """
            return BitmapPHTrees.to_paraview_node_from_nodes([self], gui_name)

        to_pvnode = to_paraview_node

    @staticmethod
    def to_paraview_node_from_nodes(nodes, gui_name=None):
        """
        Construct a :class:`homcloud.paraview_interface.PipelineNode`
        object to visulize node volumes of the nodes.

        Args:
            nodes (list of :class:`BitmapPHTrees.Node`): The list of nodes to be visualized.
            gui_name (string or None): The name shown in Pipeline Browser
                in paraview's GUI.

        Returns:
            homcloud.paraview_interface.VTK: Paraview Pipeline node object.
        """

        drawer = pict_tree.prepare_drawer_for_paraview(len(nodes))
        for (index, node) in enumerate(nodes):
            pict_tree.draw_volume(drawer, node.volume(), index, str(index))
        path = tempfile(".vtk")
        drawer.output(path)
        return pv_interface.VTK(path, gui_name).set_representation("Wireframe")

    to_pvnode_from_nodes = to_paraview_node_from_nodes


def draw_pixels_on_2d_image(image, pixels, color, alpha=1.0):
    for (y, x) in pixels:
        if x < 0 or y < 0 or x >= image.size[0] or y >= image.size[1]:
            continue
        blended_color = tuple((np.array(image.getpixel((x, y))) * (1 - alpha) +
                               np.array(color) * alpha).astype(int))
        image.putpixel((x, y), blended_color)
    return image


def draw_volumes_on_2d_image(nodes, image, color, alpha=1.0,
                             birth_position=None, death_position=None, marker_size=1):
    """
    Draws optimal volumes for bitmap filtration on an image.

    Args:
        nodes (list of :class:`BitmapPHTrees.Node`):
            The tree nodes to be drawn.
        image (string or numpy.ndarray or PIL.Image.Image):
            The base image data.

            * string: The image file whose name is `image` is used.
            * numpy.ndarray: 2D array is treated as grayscale image.
            * PIL.Image.Image: The image data

            If PIL.Image.Image object is given, the object is overwrited.
        color (tuple[int, int, int]): The color (RGB) of the volumes.
        alpha (float): The alpha value.
           The volume is drawn by using alpha blending.
        birth_position (tuple[int, int, int] or None): If not None,
           birth positions are drawn by the given color
        death_position (tuple[int, int, int] or None): If not None,
           death positions are drawn by the given color
        marker_size (int): The marker size of birth positions and death positions.
           1, 3, 5, ... are available.
    Returns:
        PIL.Image.Image: The image data which optimal volumes are drawn.
    """
    image = to_pil_image(image)

    def draw_marker(position, color):
        d = marker_size // 2
        pixels = [(position[0] + dy, position[1] + dx)
                  for dx in range(-d, d + 1) for dy in range(-d, d + 1)]
        draw_pixels_on_2d_image(image, pixels, color)

    pixels = set(chain.from_iterable([map(tuple, node.volume()) for node in nodes]))
    draw_pixels_on_2d_image(image, pixels, color, alpha)

    if birth_position:
        for node in nodes:
            draw_marker(node.birth_position(), birth_position)
    if death_position:
        for node in nodes:
            draw_marker(node.death_position(), death_position)

    return image


def draw_birthdeath_pixels_2d(
        pairs, image, draw_birth=False, draw_death=False, draw_line=False,
        scale=1, marker_type="filled-diamond", marker_size=1,
        with_label=False, birth_color=(255, 0, 0), death_color=(0, 0, 255),
        line_color=(0, 255, 0),
):
    """
    Draw birth/death pixels on the given image.

    This function returns PIL.Image.Image object.
    Please see the `document of pillow
    <https://pillow.readthedocs.io/en/latest/reference/Image.html>`_
    to know how to treat this object.

    Args:
        pairs (list of :class:`Pair`): The birth-death pairs.
        image (string or numpy.ndarray or PIL.Image.Image):
            The image data.

            * string: The image file whose name is `image` is used.
            * numpy.ndarray: 2D array is treated as grayscale image.
            * PIL.Image.Image: The image data
        draw_birth (bool): Birth pixels are drawn if True.
        draw_death (bool): Death pixels are drawn if True.
        draw_line (bool): The lines connecting each birth pixels and
            death pixels are drawn.
        scale (int): Image scaling factor.
        marker_type (string): The type of the markers. You can choose
            one of the followings:

            * "filled-diamond"
            * "point"
            * "square"
            * "filled-square"
            * "circle"
            * "filled-circle"
        marker_size (int): The size of the marker.
        with_label (bool): Show birth and death times beside
            each birth/death pixel marker.
        birth_color (tuple[int, int, int]): The color of birth pixel markers.
        death_color (tuple[int, int, int]): The color of death pixel markers.
        line_color (tuple[int, int, int]): The color of lines.

    Returns:
        PIL.Image.Image: The image data which birth/death pixels are drawn.
    """
    image = to_pil_image(image)

    output_image, marker_drawer = view_index_pict.setup_images(
        image, scale, not with_label
    )
    marker_drawer.scale = scale
    marker_drawer.marker_size = marker_size
    marker_drawer.should_draw_birth_pixel = draw_birth
    marker_drawer.should_draw_death_pixel = draw_death
    marker_drawer.should_draw_line = draw_line
    marker_drawer.no_label = not with_label
    marker_drawer.birth_color = birth_color
    marker_drawer.death_color = death_color
    marker_drawer.line_color = line_color

    for pair in pairs:
        marker_drawer.draw_pair(pair)

    return output_image


def to_pil_image(image):
    if isinstance(image, str):
        return view_index_pict.open_image(image).convert("RGB")
    elif isinstance(image, np.ndarray):
        upper = np.max(image)
        lower = np.min(image)
        return Image.fromarray(((image - lower) / (upper - lower) * 250).astype(np.uint8)).convert("RGB")
    elif isinstance(image, Image.Image):
        return image
    else:
        raise(RuntimeError("{} cannot be converted to PIL.Image".format(repr(image))))


def loadtxt_nd(path):
    """
    Load a n-dimensional data from text.

    The format of the text file is as follows.

    * First line represents the shape of data. For example, if the shape of your d
      ata is 200x230x250, first line should be `200 230 250`.
    * The following lines are floating point number values in x-fastest direction
    * A line starting with `#` is skipped as a comment
    * An empty line is also skipped.

    The following is an example::

        # 4x3x2 3D voxel data
        4 3 2

        1 2 3 4
        5 6 7 8
        9 10 11 12

        13 14 15 16
        17 18 19 20
        21 22 23 24

    Args:
        path (string): The path of the text file.
    """
    return pict_utils.load_nd_picture_from_text(path)


def show_slice3d(volumes, slice=0, spacer=0, range=None, image_viewer="eog -n"):
    """
    Display slices of 3D bitmap data.

    Args:
        volumes (list of numpy.ndarray): multiple 3D bitmap data. These data are
            aligned horizontally.
        slice (int): The direction of slicing: 0, 1, or 2 for z, y, x direction.
        spacer (int): The number of pixels between horizontally aligned slices.
        range (None or tuple[int, int]): The range of the slices.
        image_viewer (str): Command line of the image viewer to see slices.
    """
    with TemporaryDirectory() as tmpdir:
        pict_slice3d.write_volume_slices(volumes, slice, spacer, range, tmpdir)
        subprocess.call("{} {}".format(image_viewer, tmpdir), shell=True)


class HomCloudError(Exception):
    """
    Base exception class of all exceptions in homcloud.interface
    and homcloud.paraview_interface module.
    """

    def __init__(self, message, code):
        self.message = message
        self.code = code


class VolumeNotFound(HomCloudError):
    """
    Exception class for :meth:`Pair.optimal_volume` and
    :meth:`Pair.tightened_volume`.
    """

    def __init__(self, message, code):
        super().__init__(message, code)
