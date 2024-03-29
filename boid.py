import numpy as np
import pygame
import itertools

from utilities import rotation_2d, get_distance
from constants import SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, RADIUS
from species import Species

SCREEN_DIMENSIONS = np.array([[WINDOW_WIDTH], [WINDOW_HEIGHT]])


class Boid:
    """Represent and define boid behavior"""

    boid_count = itertools.count()

    @classmethod
    def init_boid_positions(cls):
        """Instantitate matrices used for storing boid positions.
        Should be called after declaration of species to avoid empty array"""
        cls.boid_positions = np.zeros((Species.total_boids, 2, 1))
        cls.boid_velocities = np.zeros((Species.total_boids, 2, 1))

    def __init__(self, x, y, angle):
        self._id = next(self.boid_count)
        self.species = Species.get_species(self._id)

        self.size = 10
        self.shape = self.get_default_shape()
        self.color = self.species.color

        self.set_pos(np.array([[x], [y]]).astype(float))
        self.set_vel(np.array([[np.cos(angle)], [np.sin(angle)]]) * SPEED)
        self.angle = angle
        self.acc = 0

    @property
    def pos(self):
        return self.boid_positions[self._id]

    def set_pos(self, pos):
        self.boid_positions[self._id] = pos

    @property
    def vel(self):
        return self.boid_velocities[self._id]

    def set_vel(self, vel):
        self.boid_velocities[self._id] = vel

    def update(
        self, neighbor_ids, species_neighbor_ids, neighbor_distances, follow_pointer
    ):
        """Use position of nearby boids to update direction, acceleration and speed of boid"""
        # update position
        self.acc = (
            self.cohesion(species_neighbor_ids, follow_pointer) * 0.5
            + self.alignment(species_neighbor_ids) * 0.5
            + self.separation(neighbor_ids, neighbor_distances) * 5
            + self.avoidance() * 10
        )

        # update velocity with acceleration and normalize
        self.set_vel(self.vel + self.acc)
        self.set_vel(self.vel / np.linalg.norm(self.vel) * SPEED)

        # update position with velocity
        self.set_pos(self.pos + self.vel)

        # update image angle
        self.angle = np.arctan2(self.vel[1], self.vel[0])

    def get_default_shape(self):
        """create default points for a triangle-shaped boid"""
        points = np.zeros((3, 2, 1))
        points[0] = np.array([[self.size], [0]])
        points[1] = np.array([[-self.size // 2], [self.size // 2]])
        points[2] = np.array([[-self.size // 2], [-self.size // 2]])
        return points

    def draw(self, screen):
        """Draw the boid on the given screen"""
        # rotate and translate points to their correct coordinates
        rotated = rotation_2d(self.angle) @ self.shape + self.pos

        # extract (x, y) coordinates and draw shape
        new_points = [(*point[0], *point[1]) for point in rotated.tolist()]
        pygame.draw.polygon(screen, self.color, new_points)

    def cohesion(self, neighbor_ids, follow_pointer):
        """Find the average direction to nearby boids"""
        neighbor_positions = self.boid_positions[neighbor_ids]
        direction = sum(neighbor_positions - self.pos)

        if follow_pointer:
            pointer_x, pointer_y = pygame.mouse.get_pos()
            pointer_pos = np.array([[pointer_x], [pointer_y]])
            if get_distance(pointer_pos, self.pos) < RADIUS * 5:
                direction += (pointer_pos - self.pos) * 1000

        norm = np.linalg.norm(direction)
        if norm > 0:
            direction /= norm
        return direction

    def alignment(self, neighbor_ids):
        """Find the average direction which nearby boids are facing"""
        neighbor_velocities = self.boid_velocities[neighbor_ids]
        direction = sum(neighbor_velocities)
        norm = np.linalg.norm(direction)
        if norm > 0:
            direction /= norm
        return direction

    def separation(self, neighbor_ids, neighbor_distances):
        """Give direction and magnitude of repulsion due to being close to nearby boids.
        Each neighbor pushes back the boid with a strength that is inversely proportional
        to the distance between the two."""
        if len(neighbor_ids) == 0:
            return np.array([[0.0], [0.0]])
        neighbor_positions = self.boid_positions[neighbor_ids]
        direction = np.sum(
            (self.pos - neighbor_positions) / neighbor_distances.reshape(-1, 1, 1) ** 2,
            axis=0,
        )
        return direction

    def avoidance(self):
        """Compute direction allowing to avoid obstacles"""
        # avoid borders
        dist_left = self.pos[0][0]
        dist_right = (SCREEN_DIMENSIONS - self.pos)[0][0]
        dist_top = self.pos[1][0]
        dist_bot = (SCREEN_DIMENSIONS - self.pos)[1][0]

        # calculate
        dir_left = (
            np.array([[-1], [0]]) / dist_right
            if dist_right < RADIUS
            else np.array([[0], [0]])
        )
        dir_right = (
            np.array([[1], [0]]) / dist_left
            if dist_left < RADIUS
            else np.array([[0], [0]])
        )
        dir_top = (
            np.array([[0], [-1]]) / dist_bot
            if dist_bot < RADIUS
            else np.array([[0], [0]])
        )
        dir_bottom = (
            np.array([[0], [1]]) / dist_top
            if dist_top < RADIUS
            else np.array([[0], [0]])
        )

        direction = dir_left + dir_right + dir_top + dir_bottom
        return direction
