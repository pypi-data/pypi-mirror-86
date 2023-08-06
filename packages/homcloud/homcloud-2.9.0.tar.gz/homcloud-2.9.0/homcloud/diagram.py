
import sys
import struct
import io
import os
import itertools
from operator import attrgetter
import warnings
import enum

import numpy as np
from scipy.ndimage.filters import gaussian_filter
import msgpack

from homcloud.index_map import IndexMap, MapType


MINUS_INF = -sys.float_info.max


class PD(object):
    """Persistence diagram class

    Note that birth_indices, death_indices, birth_positions, death_positions,
    filtration_type, and index_map are available if and only if
    an index map information is given.

    Instance variables:
    births -- birth times, 1D ndarray of floats
    deaths -- death times, 1D ndarray of floats
    birth_indices -- index birth times, 1D ndarray of int
    death_indices -- index death times, 1D ndarray of int
    birth_positions -- list of birth pixels or birth simplices
    death_positions -- list of death pixels or death simplices
    filtration_type -- index_map.MayType enum
    index_map -- index map defined in index_map module
    sign_flipped -- True if superlevel filtration, otherwise False
    """
    def __init__(self, births, deaths, degree=None, essential_births=np.empty((0,)),
                 boundary_map_dict=None, sign_flipped=False):
        self.births = births
        self.deaths = deaths
        self.essential_births = essential_births
        self.birth_indices = self.death_indices = None
        self.birth_positions = None
        self.death_positions = None
        self.filtration_type = None
        self.index_map = None
        self.path = None
        self.degree = degree
        self.sign_flipped = sign_flipped
        self.boundary_map_dict = boundary_map_dict

    MAGIC_DIPHA = 8067171840
    DIPHA_DIAGRAM_TYPE = 2

    @staticmethod
    def is_valid_header(magic, filetype):
        return magic == PD.MAGIC_DIPHA and filetype == PD.DIPHA_DIAGRAM_TYPE

    @staticmethod
    def write_dipha_diagram_header(f):
        f.write(struct.pack("qq", PD.MAGIC_DIPHA, PD.DIPHA_DIAGRAM_TYPE))

    @staticmethod
    def load_from_dipha(infile, d):
        """Create a PD object from dipha

        Args:
        infile -- io-like object
        d -- degree of persistent homology
        """
        if not PD.is_valid_header(*struct.unpack("qq", infile.read(16))):
            raise RuntimeError("This file is not a dipha PD file")
        num_pairs, = struct.unpack("q", infile.read(8))
        births = []
        deaths = []
        ess_births = []

        for _ in range(0, num_pairs):
            pair_d, birth, death = struct.unpack("qdd", infile.read(24))
            if (-pair_d - 1 == d) or (pair_d == d and death == np.inf):
                ess_births.append(birth)
            elif pair_d == d and birth == MINUS_INF:
                pass
            elif pair_d == d:
                births.append(birth)
                deaths.append(death)

        return PD(np.array(births), np.array(deaths), d, np.array(ess_births))

    @staticmethod
    def load_from_diphafile(inpath, d):
        """Creat a PD object from dipha file.

        Args:
        inpath -- dipha diagram file path
        d -- degree of persistence homology
        """
        with open(inpath, "rb") as f:
            return PD.load_from_dipha(f, d).set_path(inpath)

    @staticmethod
    def load_from_text(infile):
        """Create a PD object from text file

        Args:
        infile -- io-like object
        """
        births = []
        deaths = []
        for line in infile:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            birth, death = line.split()
            if death == "Inf":
                continue
            births.append(float(birth))
            deaths.append(float(death))

        return PD(np.array(births), np.array(deaths))

    @staticmethod
    def merge(pds):
        """Merge multiple PDs in on pd object.

        Args:
        pds: list of PD objects
        """
        if not pds:
            return PD.empty_pd()
        births = np.concatenate([pd.births for pd in pds])
        deaths = np.concatenate([pd.deaths for pd in pds])
        new_pd = PD(births, deaths)
        new_pd.filtration_type = pds[0].filtration_type
        if new_pd.filtration_type:
            new_pd.birth_positions = list(itertools.chain.from_iterable([
                pd.birth_positions for pd in pds
            ]))
            new_pd.death_positions = list(itertools.chain.from_iterable([
                pd.death_positions for pd in pds
            ]))

        return new_pd

    @staticmethod
    def empty_pd(sign_flipped=False):
        """Return a PD without any birth-death pair
        """
        return PD(np.zeros((0,)), np.zeros((0,)), sign_flipped=sign_flipped)

    @staticmethod
    def load_from_textfile(path):
        """Create a PD object from text file whose name is path

        Args:
        path -- input file path
        """
        with open(path) as f:
            return PD.load_from_text(f).set_path(path)

    @staticmethod
    def load_from_indexed_diphafile(inpath, d, load_bmap=False):
        """Create a PD object from idiagram file

        Args:
        inpath -- the path of input file
        d -- degree
        """
        with open(inpath, "rb") as f:
            return PD.load_from_indexed_dipha(f, d, load_bmap).set_path(inpath)

    @staticmethod
    def load_from_indexed_dipha(f, d, load_bmap=False):
        """Create a PD object from idiagram io-like object

        Args:
        f -- an io-like object, read data from this object
        d -- degree
        """
        unpacker = msgpack.Unpacker(f, raw=False)
        data = next(unpacker)
        pd = PD.load_from_dipha(io.BytesIO(data["diagram"]), d)
        pd.boundary_map_dict = PD.load_boundary_map(load_bmap, unpacker)
        pd.index_map = IndexMap.load_from_dict(data["index-map"])
        pd.restore_levels(pd.index_map)
        return pd

    @staticmethod
    def load_boundary_map(load_bmap, unpacker):
        if not load_bmap:
            return None

        try:
            return next(unpacker)
        except StopIteration:
            raise(RuntimeError("No boundary map information"))

    @staticmethod
    def load_from_pmtfile(path, d):
        with open(path, "rb") as f:
            return PD.load_from_pmt(f, d).set_path(path)

    @staticmethod
    def load_from_pmt(f, d):
        if d != 0:
            raise ValueError("degree for pmt file must be 0")
        dic = msgpack.unpack(f, raw=False)
        births = []
        deaths = []
        birth_poss = []
        death_poss = []
        for node in dic["nodes"]:
            if node["level"] != node["death_time"] and node["death_time"] is not None:
                births.append(node["level"])
                deaths.append(node["death_time"])
                birth_poss.append(node["pos"])
                death_poss.append(node["death_pos"])
        pd = PD(np.array(births), np.array(deaths), 0)
        pd.birth_positions = birth_poss
        pd.death_positions = death_poss
        pd.filtration_type = MapType.bitmap
        return pd

    @staticmethod
    def load_from_p2mtfile(path, d):
        with open(path, "rb") as f:
            return PD.load_from_p2mt(f, d).set_path(path)

    @staticmethod
    def load_from_p2mt(f, d):
        dic = msgpack.unpack(f, raw=False)
        if d == 0:
            nodes = dic["lower"]["nodes"]
        elif d == dic["dim"] - 1:
            nodes = dic["upper"]["nodes"]
        else:
            raise(RuntimeError("degree for p2mt file must be 0 or n-1"))
        births = list()
        deaths = list()
        birth_poss = list()
        death_poss = list()
        ess_births = list()
        ess_birth_poss = list()
        for node in nodes.values():
            if node["birth-time"] == node["death-time"]:
                continue
            if node["death-time"] is None:
                ess_births.append(node["birth-time"])
                ess_birth_poss.append(node["birth-pixel"])
            else:
                births.append(node["birth-time"])
                deaths.append(node["death-time"])
                birth_poss.append(node["birth-pixel"])
                death_poss.append(node["death-pixel"])
        pd = PD(np.array(births, dtype=float), np.array(deaths, dtype=float), d,
                np.array(ess_births, dtype=float))
        pd.birth_positions = birth_poss
        pd.death_positions = death_poss
        pd.essential_birth_positions = ess_birth_poss
        pd.filtration_type = MapType.bitmap
        pd.sign_flipped = dic["sign-flipped"]
        return pd

    @staticmethod
    def load(typestr, path, degree, negate=False):
        filetype = PD.estimate_filetype(typestr, path)
        if filetype == PD.FileType.dipha_diagram:
            pd = PD.load_from_diphafile(path, degree)
        elif filetype == PD.FileType.idipha_diagram:
            pd = PD.load_from_indexed_diphafile(path, degree)
        elif filetype == PD.FileType.text:
            pd = PD.load_from_textfile(path)
        elif filetype == PD.FileType.persistence_merge_tree:
            pd = PD.load_from_pmtfile(path, degree)
        elif filetype == PD.FileType.p2mt:
            pd = PD.load_from_p2mtfile(path, degree)
        else:
            raise ValueError("Unkown file format: {}".format(path))
        if negate:
            pd.negate_birth_death_time()
        return pd

    @staticmethod
    def load_diagrams(typestr, paths, degree, negate):
        """Load diagrams from paths, merge them, and return merged diagram

        Args:
        typestr -- the type of input file, "dipha", "text", "idipha",
                   or None(autodetect)
        paths -- the list of input files
        degree -- degree of persistence homology
                  (not requred for "text" format)
        negate -- flip sign of birth/death times if True
        """
        diagrams = [PD.load(typestr, path, degree) for path in paths]
        if len(diagrams) != 1:
            diagram = PD.merge(diagrams)
        else:
            diagram = diagrams[0]

        if negate:
            diagram.negate_birth_death_time()

        return diagram

    @staticmethod
    def estimate_filetype(typestr, path):
        """Estimate file type from typestr and path and return
        an element of PD.FileType

        if the file type cannot be determined, returns PD.FileType.unknown
        args:
        typestr -- a string representing filetype, one of: None, "idipha",
                   "dipha", "text"
        path -- a filepath string
        """
        TABLE_TYPENAME = {
            "idipha": PD.FileType.idipha_diagram,
            "dipha": PD.FileType.dipha_diagram,
            "text": PD.FileType.text,
            "pmt": PD.FileType.persistence_merge_tree,
            "p2mt": PD.FileType.p2mt,
        }
        TABLE_EXTENSION = {
            ".idiagram": PD.FileType.idipha_diagram,
            ".diagram": PD.FileType.dipha_diagram,
            ".pmt": PD.FileType.persistence_merge_tree,
            ".p2mt": PD.FileType.p2mt,
            ".txt": PD.FileType.text,
        }

        _, ext = os.path.splitext(path)
        return(TABLE_TYPENAME.get(typestr) or
               TABLE_EXTENSION.get(ext) or
               PD.FileType.unknown)

    def set_path(self, path):
        self.path = path
        return self

    def pairs(self):
        """Return birth-death pairs as a list of (2,)-ndarray
        """
        return np.array([self.births, self.deaths]).transpose()

    def pairs_positions(self):
        """Return birth-death pairs as a list of Pair objects.

        Pair object has additional information of birth/death simplices/pixels.
        The returned list is sorted by pairs' lifetime.
        """
        return sorted([
            Pair(birthtime, deathtime, birth_pos, death_pos)
            for (birthtime, deathtime, birth_pos, death_pos)
            in zip(self.births, self.deaths, self.birth_positions, self.death_positions)
        ], key=attrgetter("lifetime"), reverse=True)

    def lifetimes(self):
        """Return birth times of pairs as a 1D ndarray of floats
        """
        return self.deaths - self.births

    def restore_levels(self, index_map):
        """Restore real birth and death times from index map

        This method is used internally.
        """
        self.birth_indices = self.births.astype(int)
        self.death_indices = self.deaths.astype(int)
        self.essential_birth_indices = self.essential_births.astype(int)
        births, birth_poss = index_map.resolve(self.birth_indices)
        deaths, death_poss = index_map.resolve(self.death_indices)
        mask = (births != deaths) & (births != MINUS_INF)
        self.births = births[mask]
        self.deaths = deaths[mask]
        self.birth_positions = [birth_poss[i] for (i, b) in enumerate(mask) if b]
        self.death_positions = [death_poss[i] for (i, b) in enumerate(mask) if b]
        self.masked_birth_indices = self.birth_indices[mask]
        self.masked_death_indices = self.death_indices[mask]
        self.essential_births, self.essential_birth_positions = index_map.resolve(
            self.essential_birth_indices
        )
        self.filtration_type = index_map.type()
        self.sign_flipped = index_map.levels_sign_flipped

    def negate_birth_death_time(self):
        """Flip the sign of birth times and death times.

        If index_map says that the sign of levels in the index_map is already flipped,
        this method call do nothing.
        """
        if self.sign_flipped:
            return
        if self.index_map and not self.sign_flipped:
            warnings.warn("Flip sign unless your filtration is not superlevel")
        self.births *= -1
        self.deaths *= -1
        self.essential_births *= -1

    def minmax_of_birthdeath_time(self):
        """Return a pair of (min, max) of birth time and death time

        The return value will be used to determine the range of plotting.
        """
        return (min(self.births.min(), self.deaths.min()),
                max(self.births.max(), self.deaths.max()))

    def count_pairs_in_rectangle(self, birth1, birth2, death1, death2):
        birth_min = min([birth1, birth2])
        birth_max = max([birth1, birth2])
        death_min = min([death1, death2])
        death_max = max([death1, death2])

        return np.sum((self.births >= birth_min) & (self.births <= birth_max) &
                      (self.deaths >= death_min) & (self.deaths <= death_max))

    def cell_dim(self, idx):
        return self.boundary_map_dict["map"][idx][0]

    def cell_boundary(self, idx):
        return self.boundary_map_dict["map"][idx][1]

    def geometry_resolver(self):
        return self.index_map.geometry_resolver(self)

    class FileType(enum.Enum):
        text = 0
        dipha_diagram = 1
        idipha_diagram = 2
        persistence_merge_tree = 3
        p2mt = 4
        unknown = -1


class Pair(object):
    def __init__(self, birth, death, birth_pos, death_pos):
        self.birth = birth
        self.death = death
        self.birth_pos = birth_pos
        self.death_pos = death_pos

    @property
    def lifetime(self):
        return self.death - self.birth

    def display_str(self):
        return "({0}, {1}) - ({2}, {3}) ({4}, {5})".format(
            self.birth, self.death,
            self.birth_pos[0], self.birth_pos[1],
            self.death_pos[0], self.death_pos[1]
        )

    def __repr__(self):
        return "Pair({})".format(self.display_str())


class Histogram(object):
    """A histogram, normally used for representing persistence diagrams.
    The PDHistogram subclass is used for this purpose.

    This class is also used for representing vectorized histogram.
    """
    def __init__(self, values, xedges, yedges, sign_flipped=False):
        self.values = values
        self.xedges = xedges
        self.yedges = yedges
        self.values_as_float = values.astype(float)
        self.sign_flipped = sign_flipped

    def xy_extent(self):
        """Return [xmin, xmax, ymin, ymax].
        """
        return [self.xedges[0], self.xedges[-1], self.yedges[0], self.yedges[-1]]

    def x_range(self):
        """Return the range of the histogram along with x-axis as a pair of (min, max).
        """
        return (self.xedges[0], self.xedges[-1])

    def y_range(self):
        """Return the range of the histogram along with y-axis as a pair of (min, max).
        """
        return (self.yedges[0], self.yedges[-1])

    def x_bins(self):
        """Return the number of bins of x-axis.
        """
        return self.xedges.size - 1

    def y_bins(self):
        """Return the number of bins of y-axis.
        """
        return self.yedges.size - 1

    def vectorize(self):
        """Return vectorized histogram as a 1D ndarray of floats.
        """
        return self.values[self.vectorize_mask()]

    def vectorize_mask(self):
        """Internally used by vectorize().
        """
        if self.sign_flipped:
            return self.xedges_of_bins() > self.yedges_of_bins()
        else:
            return self.xedges_of_bins() < self.yedges_of_bins()

    def xedges_of_bins(self):
        """Internally used by vectorize().
        """
        xedges = self.xedges[1:] if self.sign_flipped else self.xedges[:-1]
        return np.repeat(xedges.reshape((1, self.x_bins())), self.y_bins(), axis=0)

    def yedges_of_bins(self):
        """Internally used by vectorize().
        """
        yedges = self.yedges[:-1] if self.sign_flipped else self.yedges[1:]
        return np.repeat(yedges.reshape((self.y_bins(), 1)), self.x_bins(), axis=1)

    def coordinates_of_center_of_bins(self):
        """Internally used by vectorize().
        """
        x_centers = (self.xedges[:-1] + self.xedges[1:]) / 2
        y_centers = (self.yedges[:-1] + self.yedges[1:]) / 2
        xs = np.repeat(x_centers.reshape((1, self.x_bins())), self.y_bins(), axis=0)
        ys = np.repeat(y_centers.reshape((self.y_bins(), 1)), self.x_bins(), axis=1)
        return (xs, ys)

    def centers_of_vectorize_bins(self):
        xs, ys = self.coordinates_of_center_of_bins()
        mask = self.vectorize_mask()
        return np.vstack((xs[mask], ys[mask])).transpose()

    def indices_for_vectorization(self):
        """Internally used by vectorize().
        """
        yindices, xindices = np.indices((self.y_bins(), self.x_bins()))
        mask = self.vectorize_mask()
        return (yindices[mask], xindices[mask])

    def value_at(self, birth, death):
        """Internally used by vectorize().
        """
        y_index = np.searchsorted(self.yedges, death)
        x_index = np.searchsorted(self.xedges, birth)
        if not ((0 < y_index < self.yedges.size) and (0 < x_index < self.xedges.size)):
            return None
        return self.values[y_index-1, x_index-1]

    @classmethod
    def reconstruct_from_vector(cls, vector, histinfo):
        """Construct a Histogram object from vector and histinfo

        Args:
        vector -- 1D ndarray of floats, this vector is translated into a histogram.
        histinfo -- a dict that has histogram information.
          The information is generated in vectorize_PD.save_histogram_information().
        """
        x_edges = np.array(histinfo["x-edges"], dtype=float)
        y_edges = np.array(histinfo["y-edges"], dtype=float)
        y_indices = histinfo["y-indices"]
        x_indices = histinfo["x-indices"]
        values = np.zeros((len(y_edges) - 1, len(x_edges) - 1), dtype=vector.dtype)
        for (y, x, val) in zip(y_indices, x_indices, vector):
            values[y, x] = val

        return cls(values, x_edges, y_edges)

    def binary_histogram_by_ranking(self, rank_range, sign=None, use_abs=True):
        """Create a binary (bool) histogram by ranking of histogram bin values.

        Args:
        rank_range: a pair of (minimum rank, maximum rank)
        sign: if this value is not None, only bins with positive(sign=+1) or
              negative(sign=-1) value is selected
        use_abs: if true, to compute a ranking, absolute value of each bin is used
        """
        if use_abs:
            values = np.abs(self.values).flatten()
        else:
            values = self.values.flatten()

        min_rank, max_rank = rank_range
        ranks = np.argsort(values.flatten())[::-1][min_rank:max_rank - min_rank + 1]
        mask = np.full_like(values, False, dtype=bool)
        mask[ranks] = True

        mask = mask.reshape(self.values.shape)
        if sign is not None:
            mask &= sign * self.values > 0
        return BinaryHistogram(mask, self.xedges, self.yedges)


class Ruler(object):
    """A pair of min-max (range) and # of bins.
    """
    def __init__(self, minmax, bins):
        self.minmax = minmax
        self.bins = bins

    def min(self):
        return self.minmax[0]

    def max(self):
        return self.minmax[1]

    def bin_width(self):
        return (self.max() - self.min()) / float(self.bins)

    def edges(self):
        return np.linspace(self.minmax[0], self.minmax[1], self.bins + 1)

    @staticmethod
    def create_xy_rulers(x_range, xbins, y_range, ybins, diagram):
        x_range = x_range or diagram.minmax_of_birthdeath_time()
        y_range = y_range or x_range
        ybins = ybins or xbins
        return (Ruler(x_range, xbins), Ruler(y_range, ybins))


class PDHistogram(Histogram):
    """Histogram of persistence diagram
    """
    def __init__(self, diagram, x_ruler, y_ruler):
        self.diagram = diagram
        self.x_ruler = x_ruler
        self.y_ruler = y_ruler
        values, yedges, xedges = np.histogram2d(
            diagram.deaths, diagram.births,
            bins=self.yx_bins(), range=self.yx_ranges()
        )
        super(PDHistogram, self).__init__(values, xedges, yedges, diagram.sign_flipped)

    def yx_bins(self):
        return (self.y_ruler.bins, self.x_ruler.bins)

    def yx_ranges(self):
        return (self.y_ruler.minmax, self.x_ruler.minmax)

    def apply_gaussian_filter(self, sigma):
        """Apply a Gaussian filter to the histogram.

        Note: This method works correctly only if the scale of x-axis and
        the scale of y-axis are the same. This should be fixed in the future.

        Args:
        sigma -- standard deviation of the gaussian distribution
        """
        self.values = gaussian_filter(self.values, self.normalized_standard_deviation(sigma))

    def normalized_standard_deviation(self, sigma):
        """Compute the standard deviation from x-scale and sigma.

        This method is internally used from apply_gaussian_filter.
        """
        return sigma / self.x_ruler.bin_width()

    def apply_weight(self, weight_func):
        """Apply (multiply) weights to all values in bins.

        The weight is computed by weight_func.
        Args:
        weight_func -- an applicable object with two parameters,
          x (birth time) and y (death time)
        """
        xs, ys = self.coordinates_of_center_of_bins()
        self.values *= np.vectorize(weight_func)(xs, ys)

    def multiply_histogram(self, val):
        """Apply (multiply) a uniform weight to all values in bins.

        Args:
        val -- weight
        """
        self.values *= val


class BinaryHistogram(Histogram):
    """A PD histogram whose values are bool.
    """
    def filter_pairs(self, pairs):
        return [pair for pair in pairs if self.value_at(pair.birth, pair.death)]
