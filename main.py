import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, APP_NAME, BLACK
from simulation import Simulation

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(APP_NAME)

simulation = Simulation(screen, num_boids=30)
simulation.start()

# Main Loop
clock = pygame.time.Clock()
RUN = True
while RUN:

    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    simulation.step()

    pygame.display.flip()

# Exit main loop
pygame.quit()
