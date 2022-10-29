from random import random
import numpy as np

from boid import Boid
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, RADIUS
from utilities import get_all_distances, get_distance_from_matrix


class Simulation:
    """Handle the global behavior of boids for each step"""

    def __init__(self, screen, num_boids):
        self.screen = screen
        self.num_boids = num_boids
        self.boids = []

    def start(self):
        """Instantiate new boids randomly"""
        for _ in range(self.num_boids):
            x, y, angle = (
                WINDOW_WIDTH * random(),
                WINDOW_HEIGHT * random(),
                6.28 * random(),
            )
            new_boid = Boid(x, y, angle)
            self.boids.append(new_boid)

    def step(self):
        """Compute and update boids for the current timestep"""
        distances = get_all_distances(Boid.boid_positions)
        for i, boid in enumerate(self.boids):
            neighbor_ids = np.where((0 < distances[i]) * (distances[i] < RADIUS))[0]
            neighbor_distances = get_distance_from_matrix(distances, neighbor_ids, i)
            boid.update(neighbor_ids, neighbor_distances)
            boid.draw(self.screen)
