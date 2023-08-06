import argparse
import warnings

from homcloud.pict import utils
from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.utils import parse_cubical_periodic_flags, parse_bool


def main(args=None):
    args = args or argument_parser().parse_args()
    pict = utils.load_nd_picture(args.input, args.type)
    if args.mode == "superlevel":
        pict = -pict.astype(float)
        flip_sign = True
    elif args.mode == "sublevel":
        flip_sign = False
    else:
        raise RuntimeError("mode must be superlevel or subelvel")

    bitmap = utils.build_levelset_filtration(pict, args.cubical, args.periodic,
                                             flip_sign, args.save_boundary_map)

    if args.combine_index_map:
        bitmap = bitmap.indexize()

    if args.convert_to_diagram:
        bitmap.compute_diagram_and_save(args.output, algorithm=args.algorithm)
    else:
        warnings.warn("-D option should be used.")
        bitmap.write_file(args.output)


def argument_parser():
    p = argparse.ArgumentParser()
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-m", "--mode", default="sublevel",
                   help="the way to construct dipha complex (sublevel(default),superlevel)")
    p.add_argument("-I", "--combine-index-map", default=False, action="store_true",
                   help="combine the index map with the output filtration")
    p.add_argument("-T", "--type", default="text_nd",
                   help="input data format (text2d,text_nd(default),picture2d,pictures3d,npy)")
    p.add_argument("-D", "--convert-to-diagram", default=False, action="store_true",
                   help="call dipha and directly convert to a diagram")
    p.add_argument("-C", "--cubical", default=False, action="store_true",
                   help="Use explicit cubical filtration (slow)")
    p.add_argument("-o", "--output", required=True,
                   help="output file")
    p.add_argument("-p", "--periodic", default=None,
                   type=parse_cubical_periodic_flags,
                   help="periodic (example: 0,1,1 for y and z are periodic)")
    p.add_argument("--algorithm", default=None,
                   help="algorithm (dipha, phat-twist, phat-chunk-parallel)")
    p.add_argument("-M", "--save-boundary-map",
                   default=False, type=parse_bool,
                   help="save boundary map into idiagram file"
                   "(only available with phat-* algorithms, on/*off*)")
    add_argument_for_license(p)
    p.add_argument("input", nargs="*", help="input files")
    return p


if __name__ == "__main__":
    main()
