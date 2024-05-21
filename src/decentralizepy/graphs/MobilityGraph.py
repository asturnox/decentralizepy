import networkx as nx
import numpy as np

from decentralizepy.graphs.MobilityNode import MobilityNode


class MobilityGraph:
    """
    This class defines the graph topology.
    Adapted from https://github.com/sacs-epfl/decentralizepy/blob/a5d46be907bc745652d5482c34117be388324439/src/decentralizepy/graphs/Graph.py
    """

    def __init__(self, nodes: list[MobilityNode]):
        """
        Constructor

        Parameters
        ----------
        nodes : list[MobilityNode]
            List of nodes in the graph
        """
        self.nodes = nodes

    def get_all_nodes(self):
        return self.nodes

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
            while (line := inf.readline()) != "":  # Read until EOF
                pos_vec = tuple(map(float, line.strip().split()))
                assert len(pos_vec) == 2, "Position vector must have 2 elements"

                line = inf.readline()
                mobility_prob_vec = tuple(map(float, line.strip().split()))
                assert len(mobility_prob_vec) == 4, "Mobility probability vector must have 4 elements"

                line = inf.readline()
                velocity = float(line.strip())

                line = inf.readline()
                coverage_area_radius = float(line.strip())

                node = MobilityNode(uid, pos_vec, mobility_prob_vec, velocity, coverage_area_radius)
                nodes.append(node)

        self.nodes = nodes
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
            of.write(str(self.n_procs) + "\n")
            for node in self.nodes:
                of.write(" ".join(map(str, node.pos_vec)) + "\n")
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

        neighbours = set()
        for node in self.nodes:
            if node.uid == uid:
                continue

            if np.linalg.norm(np.array(node.pos_vec) - np.array(self.nodes[uid].pos_vec)) <= self.nodes[
                uid].coverage_area_radius:
                neighbours.add(node.uid)

        return neighbours
