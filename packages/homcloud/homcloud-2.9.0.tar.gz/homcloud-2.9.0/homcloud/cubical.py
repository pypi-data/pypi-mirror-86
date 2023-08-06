import msgpack

from homcloud.filtration import (
    Filtration, FiltrationWithIndex, FiltrationWithoutIndex
)
from homcloud.cubical_ext import CubicalFiltrationExt
from homcloud.index_map import IndexMapForCubical
from forwardable import forwardable


@forwardable()
class CubicalFiltrationBase(Filtration):
    def_delegators("cubefilt_ext", "array")
    def_delegators("cubefilt_ext", "value_at")
    def_delegators("cubefilt_ext", "encode_cube")
    def_delegators("cubefilt_ext", "decode_cube")
    def_delegators("cubefilt_ext", "all_cubes")

    def write_dipha_complex(self, output):
        output.write(self.cubefilt_ext.dipha_byte_sequence())


class CubicalFiltration(CubicalFiltrationBase, FiltrationWithoutIndex):
    def __init__(self, array, periodic, levels_sign_flipped=False,
                 save_boundary_map=False):
        self.cubefilt_ext = CubicalFiltrationExt(array.astype(float),
                                                 periodic, save_boundary_map)
        self.levels_sign_flipped = levels_sign_flipped

    def indexize(self):
        levels = self.cubefilt_ext.indexize_internal()
        index_map = IndexMapForCubical(
            self.sign() * levels, self.levels_sign_flipped,
            self.cubefilt_ext.array.shape, self.cubefilt_ext.sorted_cubes
        )
        return IndexedCubicalFiltration(index_map, self.cubefilt_ext)

    def sign(self):
        return -1 if self.levels_sign_flipped else 1

    @staticmethod
    def favorite_algorithm():
        return "dipha"


class IndexedCubicalFiltration(CubicalFiltrationBase, FiltrationWithIndex):
    def __init__(self, index_map, cubefilt_ext):
        self.index_map = index_map
        self.cubefilt_ext = cubefilt_ext

    def build_phat_matrix(self):
        return self.cubefilt_ext.build_phat_matrix()

    def write_indexed_complex(self, output):
        output.write(msgpack.packb({
            "dipha-data": self.cubefilt_ext.dipha_byte_sequence(),
            "index-map": self.index_map.to_dict(),
        }, use_bin_type=True))

    @staticmethod
    def favorite_algorithm():
        return "phat-twist"
