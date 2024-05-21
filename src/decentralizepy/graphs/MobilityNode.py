from typing import Tuple


class MobilityNode:
    """
    This graph defines the node in the graph topology.
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
