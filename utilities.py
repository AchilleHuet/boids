import math
import numpy as np

def rotation2D(angle):
    return np.array([[math.cos(angle), -math.sin(angle)],
                     [math.sin(angle), math.cos(angle)]])

def get_distance(pos1, pos2):
    vec = pos2 - pos1
    return np.linalg.norm(vec)
