import argparse

import matplotlib.pyplot as plt

from homcloud import utils
from homcloud import plot_PD
from homcloud.version import __version__
from homcloud.diagram import PD


def argument_parser():
    p = argparse.ArgumentParser(description="plot 1d projected histogram")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-T", "--type", default="dipha",
                   help="input file format (dipha(default), idipha, text)")
    p.add_argument("-t", "--title", metavar="Title",
                   default=None, help="title string")
    p.add_argument("-d", "--degree", metavar="D", type=int,
                   default=1, help="degree of homology (default: 1)")
    p.add_argument("-U", "--unit-name", default=None,
                   help="unit name of birth and death times")
    p.add_argument("-x", "--x-range", required=True, type=utils.parse_range,
                   help="birth range")
    p.add_argument("-X", "--xbins", required=True, type=int,
                   help="number of bins in birth-axis")
    p.add_argument("-i", "--indexed", metavar="JSONFILE", nargs="*",
                   help="index file")
    p.add_argument("input", nargs="+", help="input file path")
    p.add_argument("-D", "--direction", default="birth",
                   help="projection direction (birth or death (default: birth))")
    return p

def main(args=None):
    args = args or argument_parser().parse_args()
    pd = PD.load_diagrams(args.type, args.input, args.degree, False)
    if args.title is None:
        args.title = args.input[0]

    if args.direction == "birth":
        data = pd.births
        xlabel = plot_PD.label_text("Birth", args)
    else:
        data = pd.deaths
        xlabel = plot_PD.label_text("Death", args)

    plt.xlabel(xlabel)
    plt.ylabel("Frequency [-]")
    plt.hist(data, bins=args.xbins, range=args.x_range)
    plt.title(args.title)
    plt.show()


if __name__ == "__main__":
    main()
