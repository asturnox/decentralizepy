import logging

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
                self.iteration = iteration
                self.graphs.append(
                    self.graphs[iteration - 1].next_graph(self.graph_seed, iteration)
                )
            return self.graphs[iteration].neighbors(node)
        else:
            return self.graph.neighbors(node)

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
        self.graphs = []

        self.graph_seed = int(config["RANDOM_SEED"]["graph_seed"])
        assert self.graph_seed is not None and self.graph_seed >= 0

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

        self.run()

        logging.info("Peer Sampler exiting")
