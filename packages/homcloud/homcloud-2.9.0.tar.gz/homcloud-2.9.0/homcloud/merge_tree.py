import itertools

import msgpack

class MergeTree(object):
    def __init__(self, nodes):
        self.nodes = nodes

    @staticmethod
    def load_from_dict(dic):
        nodes = [MergeTree.Node(index, n["level"], n["death_time"], n["pos"])
                 for (index, n) in enumerate(dic["nodes"])]
        for (parent_index, child_index) in dic["graph"]:
            nodes[child_index].parent = nodes[parent_index]
            nodes[parent_index].children.append(nodes[child_index])

        return MergeTree(nodes)

    @staticmethod
    def load_from_pmt(f):
        return MergeTree.load_from_dict(msgpack.unpack(f, raw=False))

    @staticmethod
    def load_from_pmcfile(path):
        with open(path, "rb") as f:
            return MergeTree.load_from_pmt(f)

    class Node(object):
        def __init__(self, index, level, death_time, pos):
            self.index = index
            self.level = level
            self.death_time = death_time
            self.pos = pos
            self.parent = None
            self.children = []

        def birth_time(self):
            return self.level

        def append_volume_to(self, lst, death_time):
            if death_time == self.level:
                return

            lst.append(self)
            for child in self.children:
                child.append_volume_to(lst, death_time)

        def volume(self, with_death_time_nodes=True):
            death_time = "invalid" if with_death_time_nodes else self.death_time
            lst = []
            self.append_volume_to(lst, death_time)
            return lst

