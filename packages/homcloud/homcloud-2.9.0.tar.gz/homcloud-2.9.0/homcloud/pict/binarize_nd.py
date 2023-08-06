
import argparse
import sys
import warnings

import homcloud.pict.binarize as binarize
import homcloud.pict.utils as utils
from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.utils import parse_cubical_periodic_flags, parse_bool
from homcloud.pict.distance_transform import distance_transform

def argument_parser():
    """Return ArgumentParser object to parse command line arguments
    """
    p = argparse.ArgumentParser()
    p.description = "Create N-dimensional erosion-dilation filtration "
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-T", "--type", default="text_nd",
                   help="input data format (text2d,text_nd(default),picture2d,pictures3d,npy)")
    binarize.add_argument_for_binarize_threshold(p)
    p.add_argument("-o", "--output", required=True,
                   help="output complex file name")
    p.add_argument("-s", "--ensmall", action="store_true", default=False,
                   help="ensmall binarized picture")
    p.add_argument("-I", "--combine-index-map", default=False, action="store_true",
                   help="combine the index map with the output filtration")
    p.add_argument("--metric", default="manhattan",
                   help="metric used to enlarge binarized image "
                   "(manhattan(default), euclidean, etc.)")
    p.add_argument("-D", "--convert-to-diagram", default=False, action="store_true",
                   help="call dipha and directly convert to a diagram")
    p.add_argument("-C", "--cubical", default=False, action="store_true",
                   help="use explicit cubical filtration (slow)")
    p.add_argument("-p", "--periodic", default=None, type=parse_cubical_periodic_flags,
                   help="periodic (example: 0,1,1 for y and z are periodic)")
    p.add_argument("--mask", help="mask bitmap")
    p.add_argument("--algorithm", default=None,
                   help="algorithm (dipha, phat-twist, phat-chunk-parallel)")
    p.add_argument("-M", "--save-boundary-map",
                   default=False, type=parse_bool,
                   help="save boundary map into idiagram file"
                   "(only available with phat-* algorithms, on/*off*)")
    add_argument_for_license(p)
    p.add_argument("input", nargs="*", help="input files")
    return p


def main(args=None):
    args = args or argument_parser().parse_args()
    pict = utils.load_nd_picture(args.input, args.type)
    binary_pict = binarize.binarize_picture(pict, args.threshold, args.mode,
                                            (args.gt, args.lt))
    mask = load_mask(args.mask, args.type)
    distance_map = binarize.distance_transform(binary_pict, args.metric,
                                               args.ensmall, obstacle=mask)
    bitmap = utils.build_levelset_filtration(
        distance_map, args.cubical, args.periodic, False, args.save_boundary_map
    )

    if args.combine_index_map:
        bitmap = bitmap.indexize()

    if args.convert_to_diagram:
        bitmap.compute_diagram_and_save(args.output, algorithm=args.algorithm)
    else:
        warnings.warn("-D option should be used.")
        bitmap.write_file(args.output)

    return 0


def load_mask(path, type):
    if path:
        return utils.load_nd_picture([path], type) > 0
    else:
        return None


if __name__ == '__main__':
    sys.exit(main())
