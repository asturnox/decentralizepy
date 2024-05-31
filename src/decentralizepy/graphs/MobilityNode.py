import logging
from enum import Enum
from typing import Tuple, Type

import numpy as np


class Direction(Enum):
    """
    Enum for the direction of the node
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class MobilityNode:
    """
    This class defines the node in the graph topology.
    """

    def __init__(self, uid: int, pos_vec: Tuple[float, float], previous_dir: Direction,
                 previous_pos_vec: Tuple[float, float], mobility_prob_vec: Tuple[float, float, float, float],
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
        self.previous_pos_vec = previous_pos_vec
        self.previous_dir = previous_dir
        self.mobility_prob_vec = mobility_prob_vec
        self.velocity = velocity
        self.coverage_area_radius = coverage_area_radius
        self.sim_path_points = None

    def advance(self, seed: int, iteration: int, width: int, height: int):
        """
        Returns a copy of the node after advancing it by one step
        """
        rng = np.random.default_rng(seed + 10000 * iteration)

        dirs = list(Direction)
        direction = rng.choice(dirs, p=self.mobility_prob_vec)
        pos_vec = list(self.pos_vec)
        if direction == Direction.UP:
            unbounded_pos = pos_vec[1] + self.velocity
            excess = max(0, unbounded_pos - height)
            pos_vec[1] = min(unbounded_pos, height) - excess
        elif direction == Direction.DOWN:
            unbounded_pos = pos_vec[1] - self.velocity
            excess = max(0, 0 - unbounded_pos)
            pos_vec[1] = max(unbounded_pos, 0) + excess
        elif direction == Direction.LEFT:
            unbounded_pos = pos_vec[0] - self.velocity
            excess = max(0, 0 - unbounded_pos)
            pos_vec[0] = max(unbounded_pos, 0) + excess
        elif direction == Direction.RIGHT:
            unbounded_pos = pos_vec[0] + self.velocity
            excess = max(0, unbounded_pos - width)
            pos_vec[0] = min(unbounded_pos, width) - excess

        new_pos_vec = tuple(pos_vec)
        old_pos_vec = tuple(list(self.pos_vec))
        return MobilityNode(self.uid, new_pos_vec, direction, old_pos_vec, self.mobility_prob_vec, self.velocity,
                            self.coverage_area_radius)

    def get_sim_path_points(self) -> set[tuple[float, float]]:
        if self.sim_path_points is not None:
            return self.sim_path_points

        return None
