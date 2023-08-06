import argparse
import re
import warnings

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
import matplotlib.cm as cm
import numpy as np

from .diagram_to_text import load_diagram
from .version import __version__
from .alpha_filtration import MINUS_INF
from homcloud.license import add_argument_for_license


def argument_parser():
    p = argparse.ArgumentParser(description="plot diagram")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-d", "--degree", type=int, required=True, help="degree")
    p.add_argument("-x", "--range", type=parse_range, help="plot range")
    p.add_argument("-X", "--bins", type=int, default=128, help="plot bins (default: 128)")
    p.add_argument("-l", "--log", action="store_true", default=False, help="log histogram")
    p.add_argument("-m", "--vmax", type=float, default=None, help="max of colorbar")
    p.add_argument("-N", "--negate", action="store_true", help="negate")
    p.add_argument("-o", "--output", help="output file")
    add_argument_for_license(p)
    p.add_argument("input", help="input file")
    return p

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

def main(args=None):
    warnings.warn("plot_diagram is obsolete. Please use homcloud.plot_PD")
    args = args or argument_parser().parse_args()
    births, deaths, _, index_map = load_diagram(args.input, args.degree)

    if index_map:
        births, deaths = resolve_index_map(births, deaths, index_map)

    births, deaths = remove_minus_inf(births, deaths)

    if args.negate:
        if index_map.levels_sign_flipped is True:
            pass
        elif index_map.levels_sign_flipped is False:
            warnings.warn("Try to flip sign unless your filtration is not superlevel")
            births = -births
            deaths = -deaths
        else:
            births = -births
            deaths = -deaths

    if args.range:
        min_time, max_time = args.range
    else:
        min_time = min([np.min(births), np.min(deaths)])
        max_time = max([np.max(births), np.max(deaths)])

    plot_range = ((min_time, max_time), (min_time, max_time))

    if args.log:
        norm = LogNorm(vmax=args.vmax)
    else:
        norm = Normalize(vmax=args.vmax)

    plt.plot([min_time, max_time], [min_time, max_time], c="black")
    plt.hist2d(births, deaths, bins=args.bins, range=plot_range, norm=norm, cmap=cm.rainbow)
    plt.colorbar()
    if args.output is None:
        plt.show()
    else:
        plt.savefig(args.output)

def resolve_index_map(births, deaths, index_map):
    births = index_map.resolve_levels(births)
    deaths = index_map.resolve_levels(deaths)
    mask = births != deaths
    return births[mask], deaths[mask]

def remove_minus_inf(births, deaths):
    mask = births != MINUS_INF
    return births[mask], deaths[mask]

if __name__ == "__main__":
    main()
