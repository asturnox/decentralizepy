import logging
from enum import Enum
from typing import Tuple, Type

import numpy as np


class MobilityNode:
    """
    This class defines the node in the graph topology.
    """

    def __init__(self, uid: int, pos_vec: Tuple[float, float], mobility_prob_vec: Tuple[float, float, float, float],
                 velocity: float,
                 coverage_area_radius: float):
        """
        Constructor

        Parameters
        ----------
        uid : int
            The unique identifier of the node
        pos_vec : (float, float)
            The position vector of the node
        mobility_prob_vec : (float, float, float, float)
            The probability vector for the node to move in the four directions
        velocity : float
            The velocity of the node
        coverage_area_radius : float
            The coverage area radius of the node

        """
        self.uid = uid
        self.pos_vec = pos_vec
        self.mobility_prob_vec = mobility_prob_vec
        self.velocity = velocity
        self.coverage_area_radius = coverage_area_radius

    def advance(self, seed: int, iteration: int):
        """
        Returns a copy of the node after advancing it by one step
        """
        rng = np.random.default_rng(seed + 10000 * iteration)

        dirs = list(Direction)
        direction = rng.choice(dirs, p=self.mobility_prob_vec)
        pos_vec = list(self.pos_vec)
        if direction == Direction.UP:
            pos_vec[1] += self.velocity
        elif direction == Direction.DOWN:
            pos_vec[1] -= self.velocity
        elif direction == Direction.LEFT:
            pos_vec[0] -= self.velocity
        elif direction == Direction.RIGHT:
            pos_vec[0] += self.velocity

        new_pos_vec = tuple(pos_vec)
        return MobilityNode(self.uid, new_pos_vec, self.mobility_prob_vec, self.velocity,
                            self.coverage_area_radius)


class Direction(Enum):
    """
    Enum for the direction of the node
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
