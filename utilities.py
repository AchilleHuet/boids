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


def get_all_distances(boid_positions):
    """
    Compute the distance matrix for a list of boids.
    Uses complex numbers properties to speed up matrix computations.
    """
    z = np.array([[complex(x, y) for [x], [y] in boid_positions]])
    return abs(z.T - z)


def clamp_positions(positions, x_min, x_max, y_min, y_max):
    return np.clip(
        positions, np.array([[x_min], [y_min]]), np.array([[x_max], [y_max]])
    )
