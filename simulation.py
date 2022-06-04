from random import random
import numpy as np

from boid import Boid
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, RADIUS
from utilities import get_all_distances


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
            neighbor_indices = np.where(distances[i] < RADIUS)[0]
            neighbors = [self.boids[j] for j in neighbor_indices if j != i]
            boid.update(neighbors, neighbor_indices)
            boid.draw(self.screen)
