import getopt
import sys

from decentralizepy.graphs.MobilityGraph import MobilityGraph
from decentralizepy.graphs.MobilityNode import MobilityNode, Direction

import numpy as np

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
    __doc__ = "Usage: python3 generate_graph.py -g <graph_type> -n <num_nodes> -s <seed> -d <degree> -k <k_over_2> -b <beta> -f <file_name> -a -h"
    assert __doc__
    argumentList = sys.argv[1:]

    options = "hg:n:s:d:k:b:f:a"

    long_options = [
        "seed=",
        "nodes=",
        "file=",
        "size=",
        "velocityStep=",
        "highMobilityProportion=",
        "help",
    ]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        seed = None
        file_name = None
        # Defaults for convenience
        num_nodes = 128
        size = 500
        velocity_step = 0.1
        high_mobility_proportion = 0.2

        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--help"):
                print(__doc__)
                exit(0)
            elif currentArgument in ("-n", "--nodes"):
                num_nodes = int(currentValue)
            elif currentArgument in ("-s", "--seed"):
                seed = int(currentValue)
            elif currentArgument in ("-f", "--file"):
                file_name = currentValue
            elif currentArgument in ("-w", "--size"):
                size = int(currentValue)
            elif currentArgument in ("-v", "--velocityStep"):
                velocity_step = float(currentValue)
            elif currentArgument in ("-m", "--highMobilityProportion"):
                high_mobility_proportion = float(currentValue)

        if file_name is None:
            file_name = f"tutorial/dynamic_{num_nodes}_{str(high_mobility_proportion).replace('.', '_')}.txt"
            print(file_name)

        if seed is None:
            seed = np.random.randint(0, 100000)

        rng = np.random.RandomState(seed)
        nodes = []
        for i in range(num_nodes):
            pos_vec = (rng.uniform(0, size), rng.uniform(0, size))

            mobility_prob_vec = tuple([0.25 for _ in range(4)])

            velocity_min = 0
            velocity_mul = 1
            if i / num_nodes < high_mobility_proportion:
                # These are clients with high mobility
                # At least as velocity_mul times as fast as the fastest low-mobility nodes
                velocity_mul = 1.75
                velocity_min = size * velocity_step

            velocity = rng.uniform(velocity_min, velocity_min + (size * velocity_step)) * velocity_mul
            if velocity > size:
                # sanity check 
                print(f"Velocity too high: {velocity}, {size}")
                sys.exit(1)

            coverage_area_radius = 45

            node = MobilityNode(i, pos_vec, Direction.UP, pos_vec, mobility_prob_vec, velocity, coverage_area_radius)
            nodes.append(node)

        g = MobilityGraph(seed, nodes=nodes)

        if file_name is not None:
            g.write_graph_to_file(file_name)
        else:
            raise ValueError("No file name. " + __doc__)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)
