import logging
import os.path

from decentralizepy.graphs.MobilityGraph import MobilityGraph
from decentralizepy.mappings.Mapping import Mapping
from decentralizepy.node.PeerSampler import PeerSampler


class PeerSamplerDynamic(PeerSampler):
    """
    This class defines the peer sampling service

    """

    def get_neighbors(self, node, iteration=None):
        if iteration != None:
            if iteration > self.iteration:
                logging.debug(
                    "iteration, self.iteration: {}, {}".format(
                        iteration, self.iteration
                    )
                )
                assert iteration == self.iteration + 1
                # self.iteration is actually 1 behind the iteration that we have already generated
                # hence the latest graph is at self.graphs[iteration]
                self.iteration = iteration

            return self.graphs[iteration].neighbors(node)
        else:
            return self.graph.neighbors(node)
        
    def precompute_graphs(self):
        for i in range(self.iterations):
            new_graph: MobilityGraph = self.graphs[i].next_graph(i + 1)
            new_graph.precompute_neighbours()
            self.graphs.append(
                new_graph
            )
            new_graph.write_graph_to_file(os.path.join(self.log_dir, f"graph_{i + 1}.txt"))

    def __init__(
            self,
            rank: int,
            machine_id: int,
            mapping: Mapping,
            graph: MobilityGraph,
            config,
            iterations=1,
            log_dir=".",
            log_level=logging.INFO,
            *args
    ):
        """
        Constructor

        Parameters
        ----------
        rank : int
            Rank of process local to the machine
        machine_id : int
            Machine ID on which the process in running
        mapping : decentralizepy.mappings
            The object containing the mapping rank <--> uid
        graph : decentralizepy.graphs
            The object containing the global graph
        config : dict
            A dictionary of configurations. Must contain the following:
            [DATASET]
                dataset_package
                dataset_class
                model_class
            [OPTIMIZER_PARAMS]
                optimizer_package
                optimizer_class
            [TRAIN_PARAMS]
                training_package = decentralizepy.training.Training
                training_class = Training
                epochs_per_round = 25
                batch_size = 64
            [RANDOM_SEED]
                graph_seed
        iterations : int
            Number of iterations (communication steps) for which the model should be trained
        log_dir : str
            Logging directory
        log_level : logging.Level
            One of DEBUG, INFO, WARNING, ERROR, CRITICAL
        args : optional
            Other arguments

        """

        self.iteration = -1
        self.graphs = [graph]  # Start with the initial graph

        self.instantiate(
            rank,
            machine_id,
            mapping,
            graph,
            config,
            iterations,
            log_dir,
            log_level,
            *args
        )

        self.precompute_graphs()

        self.run()

        logging.info("Peer Sampler exiting")
