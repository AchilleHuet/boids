import numpy as np
import pygame

from utilities import rotation2D

BLUE = (0, 0, 255)
SPEED = 4
SCREEN = np.array([[1280], [720]])

class Boid():

    def __init__(self, x, y, angle, delta_angle):
        super().__init__()
        self.size = 10

        self.pos = np.array([[x], [y]]).astype(float)
        self.vel = np.array([[np.cos(angle)], [np.sin(angle)]]) * SPEED
        self.angle = angle
        self.acc = delta_angle


    def update(self):
        # update image angle
        self.angle += self.acc

        # update position
        self.vel = np.array([[np.cos(self.angle)], [np.sin(self.angle)]]) * SPEED
        self.pos += self.vel
        self.pos = np.mod(self.pos, SCREEN)


    def draw(self, screen):
        points = np.zeros((3, 2, 1))

        points[0] = np.array([[self.size],[0]])
        points[1] = np.array([[-self.size//2],[self.size//2]])
        points[2] = np.array([[-self.size//2],[-self.size//2]])

        rotated = rotation2D(self.angle) @ points
        rotated = rotated + self.pos

        new_points = [(*point[0], *point[1]) for point in rotated.tolist()]

        pygame.draw.polygon(screen, BLUE, new_points)

