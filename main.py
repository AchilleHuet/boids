from utilities import get_distance
import pygame

from boid import Boid
from random import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

APP_NAME = "Boids"

BLACK = (0, 0, 0)

FPS = 60
NUM_BOIDS = 20
RADIUS = 100

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(APP_NAME)

boids = []
for _ in range(NUM_BOIDS):
    x, y, angle, acc = WINDOW_WIDTH*random(), WINDOW_HEIGHT*random(), 6.28*random(), 0
    new_boid = Boid(x, y, angle)
    boids.append(new_boid)

# Main Loop
clock = pygame.time.Clock()
RUN = True
while RUN:

    clock.tick(FPS)

    window.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    for boid in boids:
        neighbors = []
        for neighbor in boids:
            dist = get_distance(boid.pos, neighbor.pos)
            if dist < RADIUS and neighbors is not boid:
                neighbors.append(neighbor)
        boid.draw(window)
        boid.update(neighbors)

    pygame.display.flip()

# Exit main loop
pygame.quit()
