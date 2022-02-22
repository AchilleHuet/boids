from random import random

from boid import Boid
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, RADIUS
from utilities import get_distance

class Simulation():
    """Handle the global behavior of boids for each step"""

    def __init__(self, screen, num_boids):
        self.screen = screen
        self.num_boids = num_boids
        self.boids = []

    def start(self):
        """Instantiate new boids randomly"""
        for _ in range(self.num_boids):
            x, y, angle = WINDOW_WIDTH*random(), WINDOW_HEIGHT*random(), 6.28*random()
            new_boid = Boid(x, y, angle)
            self.boids.append(new_boid)

    def step(self):
        """Compute and update boids for the current timestep"""
        for boid in self.boids:
            neighbors = []
            for neighbor in self.boids:
                dist = get_distance(boid.pos, neighbor.pos)
                if dist < RADIUS and neighbors is not boid:
                    neighbors.append(neighbor)
            boid.update(neighbors)
            boid.draw(self.screen)
