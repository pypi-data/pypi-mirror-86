import re
from tempfile import TemporaryDirectory

import msgpack
from forwardable import forwardable

from homcloud.dipha import (
    DiphaInputFromFiltrationObject, DiphaOutputToIDiagramFile,
    DiphaOutputToDiagramFile, execute_dipha
)


class Filtration(object):
    """Super class of AlphaFiltration and BitmapFiltration

    This class has common methods of subclasses.
    """
    def write_file(self, path):
        with open(path, "wb") as f:
            self.write(f)

    def compute_diagram_and_save(self, outpath, parallels=1, algorithm=None):
        """Convert filtration into diagram, and save the diagram into out.
        """
        if not algorithm:
            algorithm = self.favorite_algorithm()

        if algorithm == "dipha":
            self.compute_diagram_by_dipha(outpath, parallels)
        elif algorithm.startswith("phat-"):
            self.compute_diagram_by_phat(outpath, algorithm)
        elif algorithm.startswith("homccube-"):
            self.compute_diagram_by_homccube(outpath, algorithm)
        else:
            raise(ValueError("unknown algorithm: {}".format(algorithm)))

    @staticmethod
    def compute_diagram_by_homccube(outpath, algorithm):
        raise(NotImplementedError("HomcCube is only available for indexed bitmaps"))


class FiltrationWithIndex(object):
    @staticmethod
    def is_indexized():
        return True

    def write(self, output):
        """Write indexed dipha complex to output."""
        self.write_indexed_complex(output)

    def compute_diagram_by_dipha(self, outpath, parallels=1,
                                 upper_dim=None, upper_value=None):
        with TemporaryDirectory() as tmpdir:
            dipha_input = DiphaInputFromFiltrationObject(self, tmpdir)
            dipha_output = DiphaOutputToIDiagramFile(outpath, dipha_input,
                                                     tmpdir)
            execute_dipha(dipha_input, dipha_output, parallels,
                          upper_dim=upper_dim, upper_value=upper_value)
            dipha_output.output()

    def compute_diagram_by_phat(self, outpath, algorithm):
        matrix = self.build_phat_matrix()
        invoke_phat(matrix, algorithm)
        with open(outpath, "wb") as f:
            write_idiagram(f, matrix.dipha_diagram_bytes(), self.index_map)
            write_boundary_map(f, self.boundary_map_byte_sequence(matrix))

    def boundary_map_byte_sequence(self, matrix):
        return matrix.boundary_map_byte_sequence()


class FiltrationWithoutIndex(object):
    @staticmethod
    def is_indexized():
        return False

    def write(self, output):
        """Write a dipha complex to output."""
        self.write_dipha_complex(output)

    def compute_diagram_by_dipha(self, outpath, parallels=1,
                                 upper_dim=None, upper_value=None):
        with TemporaryDirectory() as tmpdir:
            dipha_input = DiphaInputFromFiltrationObject(self, tmpdir)
            dipha_output = DiphaOutputToDiagramFile(outpath)
            execute_dipha(dipha_input, dipha_output, parallels,
                          upper_dim=upper_dim, upper_value=upper_value)
            dipha_output.output()

    def compute_diagram_by_phat(self, outpath, algorithm):
        filt = self.indexize()
        matrix = filt.build_phat_matrix()
        invoke_phat(matrix, algorithm)
        with open(outpath, "wb") as f:
            f.write(matrix.level_resolved_dipha_diagram_bytes(filt.index_map.levels))


def invoke_phat(matrix, algorithm):
    if algorithm == "phat-twist":
        matrix.reduce_twist()
    elif algorithm == "phat-chunk-parallel":
        matrix.reduce_chunk()
    else:
        raise(ValueError("unknown algorithm: {}".format(algorithm)))


def write_idiagram(f, diagram_bytes, index_map):
    msgpack.dump({
        "diagram": diagram_bytes,
        "index-map": index_map.to_dict(),
    }, f, use_bin_type=True)


def write_boundary_map(f, boundary_map_bytes):
    if boundary_map_bytes:
        f.write(boundary_map_bytes)
