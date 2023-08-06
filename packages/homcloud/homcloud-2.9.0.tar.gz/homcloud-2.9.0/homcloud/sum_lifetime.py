import argparse
import json

from .diagram import PD

def argument_parser():
    p = argparse.ArgumentParser(description="Calculate the sum of (lifetime)^p")
    p.add_argument("-d", "--degree", type=int, default=1,
                   help="Degree of PH (default=1)")
    p.add_argument("-i", "--indexed", default=None,
                   help="Index json file")
    p.add_argument("exponent", type=float, help="Exponent (p)")
    p.add_argument("diagram", help="Dipha persistence diagram file name")
    return p

def main(args):
    with open(args.diagram, "rb") as f:
        pd = PD.load_from_dipha(f, args.degree)

    if args.indexed:
        with open(args.indexed) as f:
            indices = json.load(f)
            pd.restore_index(indices)

    sum_lifetime = 0.0
    for (b, d) in zip(pd.births, pd.deaths):
        sum_lifetime += (d - b)**args.exponent
    print(sum_lifetime)

if __name__ == "__main__":
    main(argument_parser().parse_args())
