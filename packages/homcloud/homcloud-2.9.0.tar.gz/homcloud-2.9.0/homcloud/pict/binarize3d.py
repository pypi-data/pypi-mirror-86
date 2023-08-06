import argparse
import sys
import warnings

import homcloud.pict.binarize as binarize
import homcloud.pict.utils as utils
from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.bitmap_filtration import BitmapFiltration
from homcloud.pict.distance_transform import distance_transform


def argument_parser():
    """Return ArgumentParser object to parse pic2diphacomplex.pict3d's
    argument
    """
    p = argparse.ArgumentParser()
    p.description = "Stack multiple 2d images to create 3d dipha image complex"
    p.add_argument("-V", "--version", action="version", version=__version__)
    binarize.add_argument_for_binarize_threshold(p)
    p.add_argument("-o", "--output", required=True,
                   help="output complex file name")
    p.add_argument("-s", "--ensmall", action="store_true", default=False,
                   help="ensmall binarized picture")
    p.add_argument("-I", "--combine-index-map", default=False, action="store_true",
                   help="combine the index map with the output filtration")
    p.add_argument("--metric", default="manhattan",
                   help="metric used to enlarge binarized image (manhattan, euclidean, etc.)")
    p.add_argument("-D", "--convert-to-diagram", default=False, action="store_true",
                   help="call dipha and directly convert to a diagram")
    add_argument_for_license(p)
    p.add_argument("input", nargs="*",
                   help="Input image files ordered by stacking order")
    return p


def main(args=None):
    """Main program invoked from command line.
    """
    warnings.warn("This program is obsolete. Please use homcloud.pict.binarize_nd instead")
    args = args or argument_parser().parse_args()
    pict = utils.load_nd_picture(args.input, "pictures3d")
    binary_pict = binarize.binarize_picture(pict, args.threshold, args.mode,
                                            (args.gt, args.lt))
    bitmap = BitmapFiltration(
        distance_transform(binary_pict, args.metric, args.ensmall), False
    )

    if args.combine_index_map:
        bitmap = bitmap.indexize()

    if args.convert_to_diagram:
        bitmap.compute_diagram_and_save(args.output)
    else:
        bitmap.write_file(args.output)

    return 0

if __name__ == '__main__':
    sys.exit(main())
