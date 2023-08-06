import argparse

import numpy as np
import scipy.misc

from homcloud.utils import load_picture

def argument_parser():
    p = argparse.ArgumentParser(description="Divide images into small pieces")
    p.add_argument("-x", type=int, default=2, help="number of pieces in x-axis (default: 2)")
    p.add_argument("-y", type=int, default=2, help="number of pieces in y-axis (default: 2)")
    p.add_argument("-d", "--length-of-digits", default=3, help="length of digits")
    p.add_argument("input", help="input file name")
    p.add_argument("output_prefix", help="prefix of output files")
    p.add_argument("output_suffix", help="suffix of output files")
    return p

def main(args=None):
    def sliding_window(lst):
        return zip(lst[:-1], lst[1:])

    args = args or argument_parser().parse_args()
    pict = load_picture(args.input)
    (ysize, xsize) = pict.shape
    xs = np.linspace(0, xsize, args.x + 1, dtype=int)
    ys = np.linspace(0, ysize, args.y + 1, dtype=int)
    print(xs)
    print(list(sliding_window(xs)))
    for (xi, (xbegin, xend)) in enumerate(sliding_window(xs)):
        for (yi, (ybegin, yend)) in enumerate(sliding_window(ys)):
            subpict = pict[ybegin:yend, xbegin:xend]
            outpath = "{prefix}-{x:0{len}d}_{y:0{len}d}{suffix}".format(
                prefix=args.output_prefix, x=xi, y=yi,
                len=args.length_of_digits, suffix=args.output_suffix
            )
            scipy.misc.imsave(outpath, subpict)



if __name__ == "__main__":
    main()
