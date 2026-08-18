import numpy as np


def generate_reachable_area(max_distance, points=360):
    """
    Generate a simplified circular reachable area.

    max_distance: maximum theoretical glide distance in metres
    points: number of points around the aircraft
    """

    angles = np.linspace(0, 2 * np.pi, points)

    x = max_distance * np.cos(angles)
    y = max_distance * np.sin(angles)

    return x, y