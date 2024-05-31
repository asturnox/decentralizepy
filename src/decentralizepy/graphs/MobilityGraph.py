import logging
import sys
from collections import defaultdict

import numpy as np

from decentralizepy.graphs.MobilityNode import MobilityNode, Direction


class MobilityGraph:
    """
    This class defines the graph topology.
    Adapted from https://github.com/sacs-epfl/decentralizepy/blob/a5d46be907bc745652d5482c34117be388324439/src/decentralizepy/graphs/Graph.py
    """

    def __init__(self, seed: int = None, nodes: list[MobilityNode] = None):
        """
        Constructor

        Parameters
        ----------
        nodes : list[MobilityNode]
            List of nodes in the graph
        seed : int
            Random seed
        """
        self.nodes: list[MobilityNode] = []
        self.n_procs = 0
        self.seed = 0
        self.neighbours_cache = defaultdict(set)

        self.width = 500
        self.height = 500

        if seed is not None:
            self.seed = seed

        if nodes is not None:
            self.nodes: list[MobilityNode] = nodes
            self.n_procs = len(nodes)

    def get_all_nodes(self):
        print("get_all_nodes")
        return [i for i in range(self.n_procs)]

    def read_graph_from_file(self, file):
        """
        Reads the graph from a given file

        Parameters
        ----------
        file : str
            path to the file

        Returns
        -------
        int
            Number of processes, read from the first line of the file

        Raises
        ------
        ValueError
            If the type is not either `edges` or `adjacency`

        """

        nodes = []
        with open(file, "r") as inf:
            uid = 0
            self.seed = int(inf.readline().strip())

            while (line := inf.readline()) != "":  # Read until EOF
                pos_vec = tuple(map(float, line.strip().split()))
                assert len(pos_vec) == 2, "Position vector must have 2 elements"

                line = inf.readline()
                dir = Direction(int(line.strip()))
                assert dir is not None, f"Invalid dir {dir}"

                previous_pos_vec = tuple(map(float, inf.readline().strip().split()))
                assert len(previous_pos_vec) == 2, "Previous position vector must have 2 elements"

                line = inf.readline()
                mobility_prob_vec = tuple(map(float, line.strip().split()))
                assert len(mobility_prob_vec) == 4, "Mobility probability vector must have 4 elements"

                line = inf.readline()
                velocity = float(line.strip())

                line = inf.readline()
                coverage_area_radius = float(line.strip())

                node = MobilityNode(uid, pos_vec, dir, previous_pos_vec, mobility_prob_vec, velocity,
                                    coverage_area_radius)
                nodes.append(node)

                uid += 1

        self.nodes = nodes
        self.n_procs = len(nodes)
        return len(nodes)

    def write_graph_to_file(self, file):
        """
        Writes graph to file

        Parameters
        ----------
        file : str
            File path
        """
        with open(file, "w") as of:
            of.write(str(self.seed) + "\n")
            for node in self.nodes:
                of.write(" ".join(map(str, node.pos_vec)) + "\n")
                of.write(str(node.previous_dir.value) + "\n")
                of.write(" ".join(map(str, node.previous_pos_vec)) + "\n")
                of.write(" ".join(map(str, node.mobility_prob_vec)) + "\n")
                of.write(str(node.velocity) + "\n")
                of.write(str(node.coverage_area_radius) + "\n")

    def neighbors(self, uid):
        """
        Gives the neighbors of a node

        Parameters
        ----------
        uid : int
            globally unique identifier of the node

        Returns
        -------
        set(int)
            a set of neighbours
        """
        if uid in self.neighbours_cache:
            return self.neighbours_cache[uid]

        neighbours = set()
        node: MobilityNode = next(filter(lambda x: x.uid == uid, self.nodes))
        sim_path_points = node.get_sim_path_points(self.width, self.height)
        r = node.coverage_area_radius
        for other_node in self.nodes:
            if other_node.uid == uid:
                continue

            for q in other_node.get_sim_path_points(self.width, self.height):
                for p in sim_path_points:
                    if np.linalg.norm(p - q) <= r:
                        neighbours.add(other_node.uid)

        self.neighbours_cache[uid] = neighbours
        return neighbours

    def next_graph(self, iteration: int):
        """
        Generates the next graph in the sequence

        Parameters
        ----------
        seed : int
            Random seed
        iteration : int
            Iteration number

        Returns
        -------
        MobilityGraph
            The next graph in the sequence
        """
        new_nodes = []
        for node in self.nodes:
            new_nodes.append(node.advance(self.seed, iteration, self.width, self.height))

        return MobilityGraph(self.seed, new_nodes)
