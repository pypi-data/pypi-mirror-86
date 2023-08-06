import sys

import numpy as np
from scipy.ndimage.filters import gaussian_filter, convolve
import scipy.misc
from scipy.ndimage.morphology import binary_dilation, binary_erosion

from homcloud.utils import load_picture, standardize

def gaussian(pict, sigma):
    return gaussian_filter(pict, sigma)

def unsharp(pict, s1, s2):
    "Sharpning filter using the difference of gaussians"
    return gaussian(pict, s1) - gaussian(pict,s2) + pict

def black_tophat(pict, size=(3, 3)):
    from scipy.ndimage.morphology import black_tophat as bt
    return bt(pict, size=size)

def white_tophat(pict, size=(3, 3)):
    from scipy.ndimage.morphology import white_tophat as wt
    return wt(pict, size=size)

def remove_dots(pict, size, d):
    weights = np.ones((size, size), dtype=int)
    w = convolve(np.asarray(pict, dtype=int), weights)
    return pict & (w > d)


def erosion_dilation(pict, d):
    pict = binary_erosion(pict, iterations=d)
    pict = binary_dilation(pict, iterations=d*2)
    pict = binary_erosion(pict, iterations=d)
    return pict

def main(args=None):
    args = args or sys.argv
    args.pop(0)
    pict = None

    def get_float():
        return float(args.pop(0))

    def get_int():
        return int(args.pop(0))

    while True:
        if args == []:
            return

        arg = args.pop(0)
        if arg == "-gaussian":
            sigma = get_float()
            pict = gaussian(pict, sigma)
        elif arg == "-unsharp":
            s1 = get_float()
            s2 = get_float()
            pict = unsharp(pict, s1, s2)
        elif arg == "-binarize":
            threshold = get_float()
            pict = pict > threshold
        elif arg == "-invert":
            pict = ~pict
        elif arg == "-black_tophat":
            pict = black_tophat(pict)
        elif arg == "-white_tophat":
            pict = white_tophat(pict)
        elif arg == "-standardize":
            pict = standardize(pict)
        elif arg == "-erosion_dilation":
            d = int(args.pop(0))
            pict = erosion_dilation(pict, d)
        elif arg == "-remove_dots":
            size = get_int()
            d = get_int()
            pict = remove_dots(pict, size, d)
        elif arg == "-show":
            scipy.misc.imshow(pict)
        elif arg == "-load":
            path = args.pop(0)
            pict = load_picture(path)
        elif arg == "-save":
            path = args.pop(0)
            scipy.misc.imsave(path, pict)
        else:
            raise RuntimeError("Unknown param {}".format(arg))

if __name__ == "__main__":
    main()
