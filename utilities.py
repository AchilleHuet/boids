import math
import numpy as np

def rotation2D(angle):
    return np.array([[math.cos(angle), -math.sin(angle)],
                     [math.sin(angle), math.cos(angle)]])
