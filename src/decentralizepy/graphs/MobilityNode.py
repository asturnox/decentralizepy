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
        self.sim_path_points_cache = None

    def advance(self, seed: int, iteration: int, width: int, height: int):
        """
        Returns a copy of the node after advancing it by one step
        """
        def generate_seed(base_seed, *args):
            combined = (base_seed,) + args
            return hash(combined) % (2**32)
        
        def maybe_reflect_pos(pos, size):
            if pos < 0:
                return -pos
            elif pos > size:
                return 2 * size - pos
            return pos
        
        rng = np.random.default_rng(generate_seed(seed, iteration, self.uid))

        dirs = list(Direction)
        direction = rng.choice(dirs, p=self.mobility_prob_vec)
        pos_vec = list(self.pos_vec)
        if direction == Direction.UP:
            pos_vec[1] = maybe_reflect_pos(pos_vec[1] + self.velocity, height)
        elif direction == Direction.DOWN:
            pos_vec[1] = maybe_reflect_pos(pos_vec[1] - self.velocity, height)
        elif direction == Direction.LEFT:
            pos_vec[0] = maybe_reflect_pos(pos_vec[0] - self.velocity, width)
        elif direction == Direction.RIGHT:
            pos_vec[0] = maybe_reflect_pos(pos_vec[0] + self.velocity, width)

        new_pos_vec = tuple(pos_vec)
        old_pos_vec = tuple(list(self.pos_vec))
        return MobilityNode(self.uid, new_pos_vec, direction, old_pos_vec, self.mobility_prob_vec, self.velocity,
                            self.coverage_area_radius)

    def get_sim_path_points(self, width: int, height: int) -> list[tuple[float, float]]:
        def velocity_vec():
            if self.previous_dir == Direction.UP:
                return np.array([0, self.velocity])
            elif self.previous_dir == Direction.DOWN:
                return np.array([0, -self.velocity])
            elif self.previous_dir == Direction.LEFT:
                return np.array([-self.velocity, 0])
            elif self.previous_dir == Direction.RIGHT:
                return np.array([self.velocity, 0])
            else:
                raise ValueError

        if self.sim_path_points_cache is not None:
            return self.sim_path_points_cache

        sim_path_points = []
        time_steps = 100
        dt = 1.0 / time_steps
        v = velocity_vec()
        p = np.array(self.previous_pos_vec)
        for t in range(time_steps):
            if p[0] < 0 or p[0] > width:
                v[0] *= -1
                p[0] = max(0, min(p[0], width))
            if p[1] < 0 or p[1] > height:
                v[1] *= -1
                p[1] = max(0, min(p[1], height))

            p += (v * dt)
            sim_path_points.append(np.copy(p))

        self.sim_path_points_cache = sim_path_points
        return sim_path_points
