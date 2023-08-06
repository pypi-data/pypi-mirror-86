import argparse
from collections import namedtuple, OrderedDict
import operator
import json

import msgpack

from homcloud.version import __version__
from homcloud.pict.utils import nd_indices, load_nd_picture
from homcloud.license import add_argument_for_license

Pixel = namedtuple("Pixel", ["level", "pos"])

def pixels_from_pict(pict):
    indices = nd_indices(pict.shape)
    return [Pixel(float(level), tuple(pos.tolist())) for (level, pos) in zip(pict.ravel(), indices)]

def main(args=None):
    args = args or argument_parser().parse_args()
    pict = load_nd_picture(args.input, args.type)
    if args.mode == "superlevel":
        pict = -pict.astype(float)
    elif args.mode == "sublevel":
        pass
    else:
        raise RuntimeError("mode must be superlevel or subelvel")

    output(MergeTree.from_pict(pict), args.output, args.output_type)

def output(merge_tree, path, output_type):
    if output_type == "json":
        with open(path, "w") as f:
            json.dump(merge_tree.to_dict(), f)
    if output_type == "msgpack":
        with open(path, "wb") as f:
            msgpack.dump(merge_tree.to_dict(), f)

def adjacent_pixels(pixel):
    ret = []
    for k in range(len(pixel.pos)):
        for d in (-1, 1):
            ret.append(pixel.pos[:k] + (pixel.pos[k] + d, ) + pixel.pos[k+1:])
    return ret

class MergeTree(object):
    def __init__(self):
        self.nodes = OrderedDict()

    def add(self, pixel):
        node = MergeTree.Node(pixel, self.next_node_index())
        self.nodes[pixel.pos] = node
        for adjacent in adjacent_pixels(pixel):
            if adjacent not in self.nodes:
                continue
            self.merge(self.nodes[adjacent], node, pixel.level, pixel.pos)

    def to_dict(self):
        return {
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "graph": [[node.parent.index, node.index] for node in self.nodes.values()
                      if not node.isroot()]
        }

    def next_node_index(self):
        return len(self.nodes)

    class Node(object):
        def __init__(self, pixel, index):
            self.pixel = pixel
            self.index = index
            self.parent = None
            self.upper = None
            self.death_time = None
            self.death_pos = None

        def level(self):
            return self.pixel.level

        def root(self):
            if self.isroot():
                return self
            if self.upper.isroot():
                return self.upper
            self.upper = self.upper.root()
            return self.upper

        def root_level(self):
            return self.root().level()

        def isroot(self):
            return self.parent is None

        def set_parent(self, node, level, death_pos):
            assert self.isroot()
            self.parent = self.upper = node
            self.death_time = level
            self.death_pos = death_pos

        def to_dict(self):
            return {
                "level": self.pixel.level,
                "death_time": self.death_time,
                "pos": list(self.pixel.pos),
                "death_pos": list(self.death_pos) if self.death_pos else None,
            }

    @staticmethod
    def merge(node1, node2, level, death_pos):
        root1 = node1.root()
        root2 = node2.root()
        if root1 is root2:
            return
        if root1.level() > root2.level():
            root1, root2 = root2, root1
        root2.set_parent(root1, level, death_pos)

    @staticmethod
    def from_pict(pict):
        merge_tree = MergeTree()
        for pixel in sorted(pixels_from_pict(pict), key=operator.attrgetter("level")):
            merge_tree.add(pixel)
        return merge_tree

def argument_parser():
    p = argparse.ArgumentParser()
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    p.add_argument("-m", "--mode", default="sublevel", help="superlevel/sublevel")
    p.add_argument(
        "-T", "--type", default="text_nd",
        help="input data format (text2d, text_nd(default), picture2d, picture3d, npy"
    )
    p.add_argument("-t", "--output-type", default="msgpack",
                   help="output file format (json, msgpack(default)")
    p.add_argument("-o", "--output", required=True, help="output file")
    p.add_argument("input", nargs="*", help="input files")
    return p


if __name__ == "__main__":
    main()
