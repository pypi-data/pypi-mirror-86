import subprocess
import sys
from tempfile import TemporaryDirectory
import os
import argparse
import io
import math

import msgpack

import homcloud.utils as utils
from homcloud.version import __version__
import homcloud.dipha_alt as dipha_alt
from homcloud.license import add_argument_for_license


class DiphaInputFromComplexFile:
    def __init__(self, inpath):
        self.inpath = inpath

    def save_to_file(self):
        """Return inpath.

        Normally, save a dipha complex file to temporary file and return
        the path of the temporary file. But in this class such a file
        already exists and simply return the path.
        """
        return self.inpath

    def get_binary(self):
        with open(self.inpath, "rb") as f:
            return f.read()

    def cubical_dim(self):
        return None


class DiphaInputFromIComplexFile:
    def __init__(self, inpath, tmpdir):
        self.inpath = inpath
        self.tmpdir = tmpdir
        self.index_map = None

    def save_to_file(self):
        input_data = self.read_icomplex_file()
        complex_path = os.path.join(self.tmpdir, "tmp.complex")
        with open(complex_path, "wb") as f:
            f.write(input_data["dipha-data"])
        self.index_map = input_data["index-map"]
        return complex_path

    def get_binary(self):
        input_data = self.read_icomplex_file()
        self.index_map = input_data["index-map"]
        return input_data["dipha-data"]

    def read_icomplex_file(self):
        with open(self.inpath, "rb") as f:
            return msgpack.unpackb(f.read(), raw=False)

    def cubical_dim(self):
        return cubical_dim_from_index_map(self.index_map)


class DiphaInputFromFiltrationObject:
    def __init__(self, filtration, tmpdir):
        self.filtration = filtration
        self.tmpdir = tmpdir
        self.index_map = filtration.index_map.to_dict() if filtration.is_indexized() else None

    def save_to_file(self):
        complex_path = os.path.join(self.tmpdir, "tmp.complex")
        with open(complex_path, "wb") as f:
            self.filtration.write_dipha_complex(f)
        return complex_path

    def get_binary(self):
        buf = io.BytesIO()
        self.filtration.write_dipha_complex(buf)
        return buf.getvalue()

    def cubical_dim(self):
        return cubical_dim_from_index_map(self.index_map)


def cubical_dim_from_index_map(index_map):
    if index_map is None:
        return None
    if index_map["type"] != "bitmap":
        return None
    if "dimension" not in index_map:  # for older index-map format
        return None
    return index_map["dimension"]


class DiphaOutputToDiagramFile:
    def __init__(self, outpath):
        self.outpath = outpath
        self.binary = None

    def dipha_diagram_path(self):
        return self.outpath

    def output(self):
        if self.binary:
            with open(self.outpath, "wb") as f:
                f.write(self.binary)


class DiphaOutputToIDiagramFile:
    def __init__(self, outpath, dipha_input, tmpdir):
        self.outpath = outpath
        self.dipha_input = dipha_input
        self.tmpdir = tmpdir
        self.binary = None

    def dipha_diagram_path(self):
        return os.path.join(self.tmpdir, "tmp.diagram")

    def output(self):
        self.write_indexed_diagram(self.get_binary())

    def get_binary(self):
        if self.binary:
            return self.binary
        with open(self.dipha_diagram_path(), "rb") as f:
            return f.read()

    def write_indexed_diagram(self, binary):
        with open(self.outpath, "wb") as f:
            f.write(msgpack.packb({
                "diagram": binary,
                "index-map": self.dipha_input.index_map,
            }, use_bin_type=True))


class DiphaOutputToPDObject:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
        self.binary = None

    def dipha_diagram_path(self):
        return os.path.join(self.tmpdir, "tmp.diagram")

    def get_diagram_input(self):
        if self.binary:
            return io.BytesIO(self.binary)
        else:
            return open(self.dipha_diagram_path(), "rb")


def execute_dipha(dipha_input, dipha_output, parallels=1, dual=False,
                  upper_dim=None, upper_value=None):
    if os.environ.get("HOMCLOUD_USE_DIPHA_ALT") == "1":
        dipha_alt.execute(dipha_input, dipha_output)
        return

    complex_path = dipha_input.save_to_file()
    diagram_path = dipha_output.dipha_diagram_path()
    options = []

    if os.environ.get("HOMCLOUD_SUPPRESS_MPI") == "1":
        mpi = []
    else:
        mpi = ["mpiexec", "-n", str(parallels)]
    if dual:
        options.append("--dual")
    if upper_dim is not None:
        options.extend(["--upper_dim", str(upper_dim + 1)])
    if upper_value is not None and upper_value != math.inf:
        options.extend(["--upper_value", str(upper_value)])

    if dipha_input.cubical_dim() in [2, 3, 4] and cubical_ripser_available():
        exec_cubicalripser(complex_path, diagram_path, dipha_input.cubical_dim())

    subprocess.check_call(mpi + ["dipha"] + options + [complex_path, diagram_path])


def cubical_ripser_available():
    return os.environ.get("HOMCLOUD_USE_CUBICALRIPSER") == "1"


def exec_cubicalripser(inpath, outpath, dim):
    exec_path = "CR{:1d}".format(dim)
    subprocess.check_call([exec_path, "--output", outpath, inpath])


def exec_dipha(inpath, outpath, parallels=1, dual=False):
    """Exec dipha.

    You need to put the dipha executable file on PATH.

    Args:
    input -- input file path
    output -- output file path
    parallels -- number of parallel computations
    dual -- use dual algorithm
    """
    dipha_input = DiphaInputFromComplexFile(inpath)
    dipha_output = DiphaOutputToDiagramFile(outpath)
    execute_dipha(dipha_input, dipha_output, parallels, dual)
    dipha_output.output()


def compute_indexed_complex(inpath, outpath, parallels=1, dual=False):
    """Exec dipha for indexed complex.

    Args:
    inpath -- input file path
    outpath -- output file path
    parallels -- number of parallel computation
    dual -- use dual algorithm
    """
    with TemporaryDirectory() as tmpdir1, TemporaryDirectory() as tmpdir2:
        dipha_input = DiphaInputFromIComplexFile(inpath, tmpdir1)
        dipha_output = DiphaOutputToIDiagramFile(outpath, dipha_input, tmpdir2)
        execute_dipha(dipha_input, dipha_output, parallels, dual)
        dipha_output.output()


def argument_parser():
    p = argparse.ArgumentParser(description="Call dipha")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-T", "--type", help="input type (dipha, idipha)")
    p.add_argument("-n", "--parallels", default=1, type=int,
                   help="number of parallel computation (default: 1)")
    p.add_argument("-d", "--dual", default=False, action="store_true",
                   help="use dual algorithm")
    p.add_argument("input", help="input file")
    p.add_argument("output", help="output file")
    add_argument_for_license(p)
    return p


def main(args=None):
    print("homcloud.dipha is obsolete, please use -D option", file=sys.stderr)
    args = args or argument_parser().parse_args()
    filetype = utils.estimate_complex_file_type(args.type, args.input)
    if filetype == utils.FileType.idipha_complex:
        compute_indexed_complex(args.input, args.output, args.parallels, args.dual)
    elif filetype == utils.FileType.dipha_complex:
        exec_dipha(args.input, args.output, args.parallels, args.dual)
    else:
        sys.stderr.write("Unknown input file type")
        exit(1)


if __name__ == "__main__":
    main()
