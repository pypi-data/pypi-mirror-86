import argparse
from homcloud.index_map import MapType

import homcloud.utils as utils
from homcloud.version import __version__
from homcloud.diagram import PD


def argument_parser():
    """Returns the parser of args
    """
    p = argparse.ArgumentParser(description="Dump pairs in dipha's diagram")
    p.add_argument("-V", "--version", action="version", version=__version__)
    utils.add_arguments_for_load_diagrams(p)
    p.add_argument("-o", "--output", help="output text file")
    p.add_argument("-S", "--show-simplices", type=utils.parse_bool, default=True,
                   help="show birth/death simplices (yes/no, default:yes)")
    p.add_argument("-E", "--show-essential-pairs", type=utils.parse_bool,
                   default=False, help="show essential pairs (yes/no, default:no)")
    p.add_argument("-s", "--symbols", type=utils.parse_bool,
                   default=False, help="show birth/death simplices by symbols"
                   "(yes/no default:no)")
    p.add_argument("input", nargs="*", help="input dipha diagram")
    return p


def format_pixel(at):
    return "(" + ",".join([str(x) for x in at]) + ")"


def format_simplex(vertices):
    return "{" + ",".join([format_pixel(vertex) for vertex in vertices]) + "}"


def output_io(args):
    import sys
    if args.output:
        return open(args.output, "w")
    else:
        return sys.stdout


def write_pairs_with_positions(diagram, io, show_essential_pairs):
    if diagram.filtration_type in [MapType.bitmap, MapType.cubical]:
        formatter = format_pixel
    elif diagram.filtration_type == MapType.alpha:
        formatter = format_simplex
    elif diagram.filtration_type == MapType.abstract:
        formatter = lambda x: x
    else:
        raise RuntimeError("Unkndown index map format")

    for (birth, death, birth_pos, death_pos) in zip(diagram.births,
                                                    diagram.deaths,
                                                    diagram.birth_positions,
                                                    diagram.death_positions):
        io.write("{} {} {} {}\n".format(birth, death,
                                        formatter(birth_pos), formatter(death_pos)))

    if show_essential_pairs:
        inf = inf_string(diagram)
        for (birth, birth_pos) in zip(diagram.essential_births,
                                      diagram.essential_birth_positions):
            io.write("{} {} {} unavaliable\n".format(birth, inf, formatter(birth_pos)))


def write_pairs(diagram, io, show_essential_pairs):
    for (birth, death) in zip(diagram.births, diagram.deaths):
        io.write("{} {}\n".format(birth, death))

    if show_essential_pairs:
        for birth in diagram.essential_births:
            io.write("{} inf\n".format(birth))


def write_pairs_with_symbolic_simplices(diagram, io, show_essential_pairs):
    geom_resolver = diagram.index_map.geometry_resolver(diagram)

    def format_simplex(idx):
        return " ".join(geom_resolver.cell_symbols(idx))

    for (birth_idx, death_idx) in zip(diagram.birth_indices, diagram.death_indices):
        birth_time = diagram.index_map.resolve_level(birth_idx)
        death_time = diagram.index_map.resolve_level(death_idx)
        if birth_time == death_time:
            continue
        print("{} {} ({}) ({})".format(
            birth_time, death_time, format_simplex(birth_idx), format_simplex(death_idx)
        ), file=io)

    if show_essential_pairs:
        inf = inf_string(diagram)
        for birth_idx in diagram.essential_birth_indices:
            print("{} {} ({}) unavailable".format(
                diagram.index_map.resolve_level(birth_idx), inf, format_simplex(birth_idx)
            ), file=io)


def inf_string(diagram):
    return "-inf" if diagram.sign_flipped else "inf"


def main(args=None):
    args = args or argument_parser().parse_args()
    diagram = PD.load_diagrams(args.type, args.input, args.degree, args.negate)
    output = output_io(args)
    if diagram.filtration_type == MapType.abstract and args.show_simplices:
        write_pairs_with_positions(diagram, output, args.show_essential_pairs)
    elif args.symbols:
        if not args.show_simplices:
            raise(ValueError, "-s must be with -S option")
        if not diagram.index_map:
            raise(ValueError, ".idiagram file is required for -s option")
        write_pairs_with_symbolic_simplices(diagram, output, args.show_essential_pairs)
    elif diagram.filtration_type and args.show_simplices:
        write_pairs_with_positions(diagram, output, args.show_essential_pairs)
    else:
        write_pairs(diagram, output, args.show_essential_pairs)


if __name__ == "__main__":
    main()
