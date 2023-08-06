import struct
import re

import numpy as np
import msgpack

from homcloud.index_map import IndexMapForBitmap
from homcloud.pict.utils import nd_indices
from homcloud.filtration import (
    Filtration, FiltrationWithIndex, FiltrationWithoutIndex
)
import homcloud.homccube as homccube

class BitmapFiltraionBase(Filtration):
    """A class representing N-d bitmap complex
    """
    def __init__(self, array):
        self.array = array
        self.dim = array.ndim

    def write_dipha_complex(self, f):
        """Write a picture to f with the dipha format.
        """
        f.write(struct.pack("qq", 8067171840, 1))
        f.write(struct.pack("qq", self.array.size, self.array.ndim))
        for g in reversed(self.array.shape):
            f.write(struct.pack("q", g))

        for pixel in self.array.flatten():
            f.write(struct.pack("d", pixel))

    def dipha_complex_size(self):
        header_size = 8 * 4
        ndim_size = 8 * self.array.ndim
        data_size = 8 * self.array.size
        return header_size + ndim_size + data_size

    @staticmethod
    def favorite_algorithm():
        return "dipha"


class BitmapFiltration(BitmapFiltraionBase, FiltrationWithoutIndex):
    def __init__(self, array, flip_levels_sign=None):
        super().__init__(array)
        self.flip_levels_sign = flip_levels_sign

    def indexize(self):
        """Index-ize self.
        """
        indices = nd_indices(self.array.shape)
        keys = np.argsort(self.array, axis=None, kind="mergesort")
        levels = self.sign() * self.array.flatten()[keys]
        invert_keys = invert_permutation(keys)
        bitmap_index = invert_keys.reshape(self.array.shape)
        bitmap_index[self.array == np.inf] = np.inf
        index_map = IndexMapForBitmap(indices[keys, :], levels, self.array.ndim,
                                      self.flip_levels_sign, self.array.shape)
        return IndexedBitmapFiltration(index_map, bitmap_index)

    def sign(self):
        return -1 if self.flip_levels_sign else 1


class IndexedBitmapFiltration(BitmapFiltraionBase, FiltrationWithIndex):
    def __init__(self, index_map, array):
        self.index_map = index_map
        super().__init__(array)

    def write_indexed_complex(self, output):
        """Write a picture with index-map to output

        This method is available for "indexize"d bitmap.
        """
        packer = msgpack.Packer(use_bin_type=True)
        output.write(packer.pack_map_header(2))
        output.write(packer.pack("dipha-data"))
        output.write(struct.pack(">BL", 0xc6, self.dipha_complex_size()))
        self.write_dipha_complex(output)
        output.write(packer.pack("index-map"))
        output.write(packer.pack(self.index_map.to_dict()))

    @staticmethod
    def homccube_cache_strategy(algorithm):
        strategy = re.match(r'^homccube-(.+)\Z', algorithm).group(1)
        if strategy in ["nothing", "requested", "always"]:
            return strategy
        else:
            return None

    def compute_diagram_by_homccube(self, outpath, algorithm):
        dipha_binary = homccube.compute_pd(
            self.array.astype(np.int32), [False] * self.array.ndim,
            self.homccube_cache_strategy(algorithm), True
        )

        with open(outpath, "wb") as f:
            f.write(msgpack.packb({
                "diagram": dipha_binary,
                "index-map": self.index_map.to_dict(),
            }, use_bin_type=True))

    def favorite_algorithm(self):
        if self.array.ndim in [2, 3]:
            return "homccube-requested"
        else:
            return "dipha"


def invert_permutation(a):
    """Create the inverse of the permutation given by a.

    If a is not a permutation, the result is indefinite.
    """
    s = np.zeros(a.size, dtype=np.float64)
    i = np.arange(a.size, dtype=np.int32)
    np.put(s, a, i)
    return s
