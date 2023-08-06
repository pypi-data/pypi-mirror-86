"""A module providing binarization and enlargement of pictures
"""
import argparse
import sys
import warnings

import numpy as np

import homcloud.pict.utils as utils
from homcloud.bitmap_filtration import BitmapFiltration
from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.pict.distance_transform import distance_transform


def main(args=None):
    warnings.warn("This program is obsolete. Please use homcloud.pict.binarize_nd instead")
    args = args or argument_parser().parse_args()
    pict = utils.load_picture(args.input, filetype=args.type)
    binary_pict = binarize_picture(pict, args.threshold, args.mode, (args.gt, args.lt))
    opts = {}
    if args.metric == "mahalanobis":
        opts["VI"] = mahalanobis_vi(args.weight, args.angle)

    bitmap = BitmapFiltration(distance_transform(
        binary_pict, args.metric, args.ensmall, **opts
    ), False)

    if args.combine_index_map:
        bitmap = bitmap.indexize()

    if args.convert_to_diagram:
        bitmap.compute_diagram_and_save(args.output)
    else:
        bitmap.write_file(args.output)

    return 0


def argument_parser():
    p = argparse.ArgumentParser(description="Construct cubical filtrations from binarized digital pictures using a distance on the pictures")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_binarize_threshold(p)
    p.add_argument("-T", "--type", default="picture",
                   help="input file format (picture(default), text)")
    p.add_argument("--metric", default="manhattan",
                   help="metric used to enlarge binarized image"
                   + "(manhattan, euclidean, etc., default is manhattan) ")
    p.add_argument("-I", "--combine-index-map", default=False, action="store_true",
                   help="combine the index map with the output filtration")
    p.add_argument("-s", "--ensmall", action="store_true", default=False,
                   help="ensmall binarized picture")
    p.add_argument("-w", "--weight", type=float, default=1,
                   help="weight for mahalanobis metric")
    p.add_argument("-a", "--angle", type=float, default=0.0,
                   help="angle for mahalanobis metric")
    p.add_argument("-D", "--convert-to-diagram", default=False, action="store_true",
                   help="call dipha and directly convert to a diagram")
    add_argument_for_license(p)
    p.add_argument("input", help="input file name")
    p.add_argument("output", help="output file name")
    return p


def add_argument_for_binarize_threshold(p):
    p.add_argument("-m", "--mode", default="black-base",
                   help="the way to construct dipha complex (black-base|white-base, "
                   + "default is black-base)")
    p.add_argument("-t", "--threshold", type=float, default=128,
                   help="threshold for binarization (default: 128)")
    p.add_argument("--gt", type=float, default=None, help="lower threshold")
    p.add_argument("--lt", type=float, default=None, help="upper threshold")


def binarize_picture(pict, threshold, mode, bounds):
    """Binarize pict using threshold.

    Args:
    pict -- a gray-scale picture (ndarray)
    threshold -- threshold for binarization
    mode -- "black-base" or "white-base"
    bounds -- a pair of lower and upper bounds
        if both of them are None, the pair of threshold and mode is used
    """
    lower_bound, upper_bound = bounds

    if lower_bound is None and upper_bound is None:
        if mode == "black-base":
            upper_bound = threshold
        elif mode == "white-base":
            lower_bound = threshold
        else:
            raise RuntimeError("Unknown mode {0}".format(mode))

    lower_bound = -float("inf") if lower_bound is None else lower_bound
    upper_bound = float("inf") if upper_bound is None else upper_bound
    return (lower_bound <= pict) & (pict <= upper_bound)


def mahalanobis_vi(weight, angle):
    def rotation_matrix(t):
        from math import cos, sin
        return np.array([[cos(t), sin(t)], [-sin(t), cos(t)]])
    return rotation_matrix(angle) @ np.diag([weight, 1 / weight]) @ rotation_matrix(-angle)


if __name__ == "__main__":
    sys.exit(main())
