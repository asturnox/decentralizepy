import numpy as np

from decentralizepy.sharing.Sharing import Sharing
from decentralizepy.graphs.MobilityGraph import MobilityGraph

import logging

import torch


class MobilityAwareSharing(Sharing):
    def __init__(
            self,
            rank,
            machine_id,
            communication,
            mapping,
            graph: MobilityGraph,
            model,
            dataset,
            log_dir,
            alpha=2.0,
            compress=False,
            compression_package=None,
            compression_class=None,
            float_precision=None,
    ):
        """
        Constructor

        Parameters
        ----------
        rank : int
            Local rank
        machine_id : int
            Global machine id
        communication : decentralizepy.communication.Communication
            Communication module used to send and receive messages
        mapping : decentralizepy.mappings.Mapping
            Mapping (rank, machine_id) -> uid
        graph : decentralizepy.graphs.Graph
            Graph reprensenting neighbors
        model : decentralizepy.models.Model
            Model to train
        dataset : decentralizepy.datasets.Dataset
            Dataset for sharing data.
        log_dir : str
            Location to write shared_params (only writing for 2 procs per machine)

        """

        print("MobilityAwareSharing constructor called alpha: ", alpha)

        super().__init__(
            rank,
            machine_id,
            communication,
            mapping,
            graph,
            model,
            dataset,
            log_dir,
            compress,
            compression_package,
            compression_class,
            float_precision,
        )
        self.alpha = alpha
        self.velocity_map = {node.uid: node.velocity for node in graph.nodes}

    def averaging_weights(self, dv_lst):
        N = len(dv_lst)
        x = np.array(dv_lst)
        norm_x = x / np.sum(x)

        logging.info("norm_x: {}".format(norm_x))
        w = (1 / N) + (self.alpha * (norm_x - (1/N)))
        logging.info("w: {}".format(w))
        return w

    def _averaging(self, peer_deques):
        if len(peer_deques) == 0:
            self.model.load_state_dict(self.model.state_dict())
            self._post_step()
            self.communication_round += 1
            return

        known_velocity_total = self.velocity_map[self.uid]
        for i, n in enumerate(peer_deques):
            known_velocity_total += self.velocity_map[n]
        known_velocity_avg = known_velocity_total / (len(peer_deques) + 1)

        self.received_this_round = 0
        with torch.no_grad():
            total = dict()

            # own_dv = self.alpha * (self.velocity_map[self.uid])
            own_dv = self.velocity_map[self.uid]
            own_data = self.model.state_dict()

            data_lst = [own_data]
            dv_lst = [own_dv]
            for i, n in enumerate(peer_deques):
                self.received_this_round += 1
                data = peer_deques[n].popleft()
                iteration = data["iteration"]
                del data["iteration"]
                del data["CHANNEL"]
                logging.info(
                    "Averaging model from neighbor {} of iteration {} velocity {}".format(
                        n, iteration, self.velocity_map[n]
                    )
                )
                data = self.deserialized_model(data)

                dv = self.velocity_map[n]
                data_lst.append(data)
                dv_lst.append(dv)

            w = self.averaging_weights(dv_lst)
            data_w = zip(data_lst, w)

            logging.info("Averaging model APSDPOADQWPO")
            logging.info("alpha: {}".format(self.alpha))
            logging.info("dvs: {}".format(dv_lst))
            logging.info("w: {}".format(w))
            logging.info("data_w: {}".format(data_w))

            for data, weight in data_w:
                for key, value in data.items():
                    if key in total:
                        total[key] += value * weight
                    else:
                        total[key] = value * weight

        self.model.load_state_dict(total)
        self._post_step()
        self.communication_round += 1
