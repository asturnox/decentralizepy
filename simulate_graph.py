import getopt
import sys

from decentralizepy.graphs.FullyConnected import FullyConnected
from decentralizepy.graphs.MobilityGraph import MobilityGraph
from decentralizepy.graphs.MobilityNode import MobilityNode
from decentralizepy.graphs.Regular import Regular
from decentralizepy.graphs.Ring import Ring
from decentralizepy.graphs.SmallWorld import SmallWorld
from decentralizepy.graphs.Star import Star

import numpy as np

def simulate_graph(file_path: str) -> list[MobilityGraph]: 
    iterations = 1000

    g = MobilityGraph()
    g.read_graph_from_file(file_path)

    stripped_file_name = file_path.split("/")[-1]
    graphs = [g]
    
    for i in range(iterations):
        new_graph = graphs[-1].next_graph(i)
        graphs.append(new_graph)
        new_graph.write_graph_to_file(f'.sim/graph_{i}.txt')

    return graphs

if __name__ == "__main__":
    """
    Script to generate a graph file.

    Usage
    -----
    python generate_graph.py -g <graph_type> -n <num_nodes> -s <seed> -d <degree> -k <k_over_2> -b <beta> -f <file_name> -a

    Parameters
    ----------
    graph_type : str
        One of {"Regular", "FullyConnected", "Ring", "SmallWorld", "Star"}
    num_nodes : int
        Number of nodes in the graph
    seed : int, optional
        Seed for random number generator
    degree : int, optional
        Degree of the graph
    k_over_2 : int, optional
        Parameter for smallworld
    beta : float, optional
        Parameter for smallworld
    file_name : str, optional
        Name of the file to write the graph to
    a : flag, optional
        If set, the graph is written in adjacency list format, otherwise in edge list format
    h : flag, optional
        Prints this help message

    """
    if len(sys.argv) == 1:
        print("No arguments provided. " + __doc__)
        sys.exit(2)

    file_path = sys.argv[1]
    simulate_graph(file_path)
