# pylint: disable=R0204
import re
import enum
import os
import subprocess
import sys
import struct
from functools import wraps

import numpy as np


def standardize(pict):
    """Standardize pixel values of the picture

    Args:
    pict -- 2D ndarray
    """
    average = np.average(pict)
    sd = np.std(pict)
    return (pict - average) / sd


def add_arguments_for_load_diagrams(parser):
    parser.add_argument("-d", "--degree", type=int, required=True,
                        help="degree of PH")
    parser.add_argument("-T", "--type",
                        help="input file format (dipha, idipha, text) (default: autodetect)")
    parser.add_argument("-N", "--negate", default=False, action="store_true",
                        help="flip the sign of birth/death times for superlevel persistence (default: False)")


def add_arguments_for_histogram_rulers(parser):
    parser.add_argument("-x", "--x-range", type=parse_range,
                        help="birth range")
    parser.add_argument("-X", "--xbins", type=int, default=128,
                        help="number of bins in birth-axis")
    parser.add_argument("-y", "--y-range", type=parse_range, default=None,
                        help="death range")
    parser.add_argument("-Y", "--ybins", type=int, default=None,
                        help="number of bins in death-axis")


def add_arguments_for_gaussian_diffusion(parser):
    parser.add_argument("-D", "--gaussian-sd", type=float, required=True,
                        help="standard deviation of gaussian diffusion")


def add_arguments_for_kernel_weight(parser):
    parser.add_argument("-C", type=float, help="weight constant C")
    parser.add_argument("-p", type=float, default=1.0, help="weight constant p")


FLOAT_REGEXP = r"[+-]?\d+(\.\d+)?"
RANGE_REGEXPS = [
    re.compile(r"\A(?P<begin>{0}):(?P<end>{0})\Z".format(FLOAT_REGEXP)),
    re.compile(r"\A\[(?P<begin>{0}):(?P<end>{0})\]\Z".format(FLOAT_REGEXP)),
]


def parse_range(string):
    for regexp in RANGE_REGEXPS:
        m = regexp.match(string)
        if m:
            return (float(m.group("begin")), float(m.group("end")))
    raise ValueError("{} cannot be parsed as range".format(string))


def parse_bool(string):
    s = string.lower()
    if s == "true" or s == "yes" or s == "1" or s == "on":
        return True
    if s == "false" or s == "no" or s == "0" or s == "off":
        return False
    raise ValueError("{} cannot be parsed as boolean".format(string))


def parse_color(string):
    if re.match(r"#[0-9a-fA-F]{6}\Z", string):
        return tuple(int(string[i:i + 2], 16) for i in [1, 3, 5])
    raise ValueError("{} cannot be parsed as color".format(string))


def boundary_of_simplex(simplex):
    return [simplex.difference([el]) for el in simplex]


def paraview_programname():
    return os.environ.get("HOMCLOUD_PARAVIEW_PROGRAMNAME", "paraview")


def invoke_paraview(*args, wait=False):
    devnull = subprocess.DEVNULL
    redirect = {"stdin": devnull, "stdout": devnull, "stderr": devnull}
    program_name = paraview_programname()

    if sys.platform.startswith("darwin"):
        if wait:
            subprocess.check_call(
                ["open", "-a", program_name, "-W", "--args"] + list(args), **redirect
            )
        else:
            subprocess.check_call(["open", "-a", program_name, "--args"] + list(args),
                                  **redirect)
    elif sys.platform.startswith("win"):
        if wait:
            subprocess.check_call([program_name] + list(args), **redirect)
        else:
            subprocess.Popen([program_name] + list(args), **redirect)
    else:
        if wait:
            subprocess.check_call(["nohup", program_name] + list(args),
                                  **redirect)
        else:
            subprocess.Popen(["nohup", program_name] + list(args), **redirect)


def deep_tolist(lst):
    """Convert ndarray to python's list recursively.

    This function is useful to convert data into json/msgpack format.

    TODO: support dict.
    """
    if isinstance(lst, np.ndarray):
        return lst.tolist()
    if isinstance(lst, list):
        return [deep_tolist(l) for l in lst]
    return lst


@enum.unique
class FileType(enum.Enum):
    text = 0
    dipha_complex = 1
    dipha_diagram = 2
    idipha_complex = 3
    idipha_diagram = 4
    unknown = 5


def estimate_complex_file_type(typestr, path):
    TABLE_TYPENAME = {
        "idipha": FileType.idipha_complex,
        "dipha": FileType.dipha_complex
    }

    TABLE_EXTENSION = {
        ".icomplex": FileType.idipha_complex,
        ".complex": FileType.dipha_complex,
    }

    _, ext = os.path.splitext(path)
    return TABLE_TYPENAME.get(typestr) or TABLE_EXTENSION.get(ext) or FileType.dipha_complex


def read_diagram_header(f):
    magic, filetype = struct.unpack("qq", f.read(16))
    if magic != 8067171840 or filetype != 2:
        raise RuntimeError("This file is not a dipha diagram file")
    num_pairs, = struct.unpack("q", f.read(8))
    return num_pairs


def parse_cubical_periodic_flags(arg):
    return [bool(int(el)) for el in re.split(",", arg)]


def load_symbols(path):
    if path is None:
        return None

    symbols = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            symbols.append(line)
    return symbols


class Cache():
    def __init__(self, func, obj):
        self.func = func
        self.obj = obj
        self.cache = None
        self.cached = False

    def __call__(self):
        if not self.cached:
            self.cache = self.func(self.obj)
            self.cached = True

        return self.cache

    def purge_cache(self):
        self.cache = None
        self.cached = False

def once_cache(f):
    @wraps(f)
    def wrapped(obj):
        c = Cache(f, obj)
        setattr(obj, f.__name__, c)
        return c()

    return wrapped
