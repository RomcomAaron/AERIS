import numpy as np


def generate_wind_aware_area(
    altitude,
    glide_ratio,
    airspeed,
    wind_speed,
    wind_direction,
    points=360
):
    """
    Generate a simplified wind-aware reachable area.

    All distances are in metres.
    Directions are measured in degrees:
        0   = North
        90  = East
        180 = South
        270 = West
    """

    # Theoretical still-air glide distance
    max_distance = altitude * glide_ratio

    # Convert angles to radians
    angles = np.linspace(0, 2 * np.pi, points)

    # Convert wind direction to radians
    wind_angle = np.radians(wind_direction)

    # Direction of each candidate point
    direction_difference = angles - wind_angle

    # Wind component in each direction
    wind_component = wind_speed * np.cos(direction_difference)

    # Approximate time available for the glide
    glide_time = max_distance / airspeed

    # Wind contribution
    wind_distance = wind_component * glide_time

    # Total reachable distance
    distances = max_distance + wind_distance

    # Prevent negative distances
    distances = np.maximum(distances, 0)

    # Convert polar coordinates to x/y
    x = distances * np.sin(angles)
    y = distances * np.cos(angles)

    return x, y, distances