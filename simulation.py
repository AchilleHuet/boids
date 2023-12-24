from random import random
import numpy as np

from boid import Boid
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, RADIUS
from utilities import get_all_distances, get_distance_from_matrix, clamp_positions

follow_pointer = False


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
            neighbord_ids_of_same_species = [
                boid_id
                for boid_id in neighbor_ids
                if ((i // 100) * 100 < boid_id) * (boid_id < (i // 100 + 1) * 100)
            ]
            neighbor_distances = get_distance_from_matrix(distances, neighbor_ids, i)
            boid.update(
                neighbor_ids,
                neighbord_ids_of_same_species,
                neighbor_distances,
                follow_pointer,
            )
            boid.draw(self.screen)

        # keep boids from going out of bounds
        Boid.boid_positions = clamp_positions(
            Boid.boid_positions, 1, WINDOW_WIDTH - 1, 1, WINDOW_HEIGHT - 1
        )
