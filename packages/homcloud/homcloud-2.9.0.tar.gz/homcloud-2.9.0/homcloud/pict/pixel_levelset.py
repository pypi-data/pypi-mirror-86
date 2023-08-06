"""A moudle providing levelset complex using pixel value
"""
import argparse
import warnings

import homcloud.pict.utils as utils
from homcloud.bitmap_filtration import BitmapFiltration
from homcloud.version import __version__
from homcloud.license import add_argument_for_license

def main(args=None):
    warnings.warn("This program is obsolete. Please use homcloud.pict.binarize_nd instead")
    args = args or argument_parser().parse_args()
    pict = utils.load_picture(args.input, args.type)
    if args.mode == "superlevel":
        pict = -pict.astype(float)
        upper_bound = -args.lower_bound
        lower_bound = -args.upper_bound
        flip_sign = True
    elif args.mode == "sublevel":
        upper_bound = args.upper_bound
        lower_bound = args.lower_bound
        flip_sign = False
    else:
        raise RuntimeError("mode must be superlevel or subelvel")

    pict[pict > upper_bound] = upper_bound
    pict[pict < lower_bound] = lower_bound

    bitmap = BitmapFiltration(pict, flip_sign)

    if args.combine_index_map:
        bitmap = bitmap.indexize()

    if args.convert_to_diagram:
        bitmap.compute_diagram_and_save(args.output)
    else:
        bitmap.write_file(args.output)

def argument_parser():
    p = argparse.ArgumentParser()
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-m", "--mode", default="sublevel",
                   help="the way to construct dipha complex (sublevel or superlevel, default is sublevel)")
    p.add_argument("-u", "--upper-bound", type=float, default=255,
                   help="upper bound of pixel value")
    p.add_argument("-l", "--lower-bound", type=float, default=0,
                   help="lower bound of pixel value")
    p.add_argument("-I", "--combine-index-map", default=False, action="store_true",
                   help="combine the index map with the output filtration")
    p.add_argument("-T", "--type", default="picture",
                   help="input file format (picture(default), text)")
    p.add_argument("-D", "--convert-to-diagram", default=False, action="store_true",
                   help="call dipha and directly convert to a diagram")
    add_argument_for_license(p)
    p.add_argument("input", help="input file name")
    p.add_argument("output", help="output file name")
    return p


if __name__ == "__main__":
    main()
