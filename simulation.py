from random import random
import numpy as np

from boid import Boid
from species import Species
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, RADIUS, BLUE, RED, GREEN
from utilities import get_all_distances, get_distance_from_matrix, clamp_positions

follow_pointer = False

blue_species = Species(num_boids=20, color=BLUE)
red_species = Species(num_boids=60, color=RED)
green_species = Species(num_boids=100, color=GREEN)


class Simulation:
    """Handle the global behavior of boids for each step"""

    def __init__(self, screen):
        self.screen = screen
        self.num_boids = Species.total_boids
        self.boids = []
        Boid.init_boid_positions()

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
            # get useful information about neighboring boids
            neighbor_ids = np.where((0 < distances[i]) * (distances[i] < RADIUS))[0]
            species_neighbor_ids = [id for id in neighbor_ids if id in boid.species.ids]
            neighbor_distances = get_distance_from_matrix(distances, neighbor_ids, i)

            # update boid position, direction and image
            boid.update(
                neighbor_ids, species_neighbor_ids, neighbor_distances, follow_pointer
            )
            boid.draw(self.screen)

        # keep boids from going out of bounds
        Boid.boid_positions = clamp_positions(
            Boid.boid_positions, 1, WINDOW_WIDTH - 1, 1, WINDOW_HEIGHT - 1
        )
