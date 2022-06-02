import math
import numpy as np


def rotation_2d(angle):
    """Return the matrix which rotates a vector by the given angle"""
    return np.array(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ]
    )


def get_distance(pos1, pos2):
    """Compute the distance between 2 positions"""
    vec = pos2 - pos1
    return np.linalg.norm(vec)


def get_distance_from_matrix(distance_matrix, boid_id1, boid_id2):
    return distance_matrix[boid_id1, boid_id2]


def get_all_distances(boids):
    """Compute the distance matrix for a list of boids"""
    distances = np.zeros((len(boids), len(boids)))
    for i, boid in enumerate(boids):
        for j, other in zip(range(i + 1, len(boids)), boids[i + 1 :]):
            dist = get_distance(boid.pos, other.pos)
            distances[i, j] = dist
            distances[j, i] = dist
    return distances
