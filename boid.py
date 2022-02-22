import numpy as np
import pygame

from utilities import rotation_2d, get_distance
from constants import SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, BLUE, RADIUS

SCREEN_DIMENSIONS = np.array([[WINDOW_WIDTH], [WINDOW_HEIGHT]])

class Boid():
    """Represent and define boid behavior"""

    def __init__(self, x, y, angle):
        self.size = 10

        self.pos = np.array([[x], [y]]).astype(float)
        self.vel = np.array([[np.cos(angle)], [np.sin(angle)]]) * SPEED
        self.angle = angle
        self.acc = 0


    def update(self, neighbors):
        """Use position of nearby boids to update direction, acceleration and speed of boid"""
        # update position
        self.acc = (
            self.cohesion(neighbors) * 0.5
            + self.alignment(neighbors) * 0.5
            + self.separation(neighbors) * 5
            + self.avoidance() * 10
        )
        self.vel += self.acc
        self.vel = self.vel / np.linalg.norm(self.vel) * SPEED

        self.pos += self.vel
        self.pos = np.mod(self.pos, SCREEN_DIMENSIONS)

        # update image angle
        self.angle = np.arctan2(self.vel[1], self.vel[0])


    def draw(self, screen):
        """Draw the boid on the given screen"""
        # create default points for a triangle-shaped boid
        points = np.zeros((3, 2, 1))
        points[0] = np.array([[self.size],[0]])
        points[1] = np.array([[-self.size//2],[self.size//2]])
        points[2] = np.array([[-self.size//2],[-self.size//2]])

        # rotate and translate points to their correct coordinates
        rotated = rotation_2d(self.angle) @ points
        rotated = rotated + self.pos

        # extract (x, y) coordinates and draw shape
        new_points = [(*point[0], *point[1]) for point in rotated.tolist()]
        pygame.draw.polygon(screen, BLUE, new_points)

    def cohesion(self, neighbors):
        """Find the average direction to nearby boids"""
        direction = np.array([[0.], [0.]])
        for other in neighbors:
            direction += other.pos - self.pos
        norm = np.linalg.norm(direction)
        if norm > 0:
            direction /= norm
        return direction

    def alignment(self, neighbors):
        """Find the average direction which nearby boids are facing"""
        direction = np.array([[0.], [0.]])
        for other in neighbors:
            direction += other.vel
        norm = np.linalg.norm(direction)
        if norm > 0:
            direction /= norm
        return direction

    def separation(self, neighbors):
        """Give direction and magnitude of repulsion due to being close to nearby boids"""
        direction = np.array([[0.], [0.]])
        for other in neighbors:
            dist = get_distance(self.pos, other.pos)
            if dist > 0:
                direction += (self.pos - other.pos) / dist**2
        # norm = np.linalg.norm(direction)
        # if norm > 0:
        #     direction /= norm
        return direction

    def avoidance(self):
        """Compute direction allowing to avoid obstacles"""
        # avoid borders
        dist_left = self.pos[0][0]
        dist_right = (SCREEN_DIMENSIONS - self.pos)[0][0]
        dist_top = self.pos[1][0]
        dist_bot = (SCREEN_DIMENSIONS - self.pos)[1][0]

        # calculate
        dir_left = np.array([[-1], [0]]) / dist_right if dist_right < RADIUS else np.array([[0], [0]])
        dir_right = np.array([[1], [0]]) / dist_left if dist_left < RADIUS else np.array([[0], [0]])
        dir_top = np.array([[0], [-1]]) / dist_bot if dist_bot < RADIUS else np.array([[0], [0]])
        dir_bot = np.array([[0], [1]]) / dist_top if dist_top < RADIUS else np.array([[0], [0]])

        direction = dir_left + dir_right + dir_top + dir_bot
        return direction
