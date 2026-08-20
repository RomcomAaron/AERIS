import numpy as np


def generate_wind_aware_area(
    altitude,
    glide_ratio,
    airspeed,
    wind_speed,
    wind_direction,
    points=360
):

    max_distance = altitude * glide_ratio

    angles = np.linspace(
        0,
        2 * np.pi,
        points
    )

    wind_angle = np.radians(
        wind_direction
    )

    direction_difference = (
        angles - wind_angle
    )

    wind_component = (
        wind_speed *
        np.cos(direction_difference)
    )

    glide_time = (
        max_distance /
        airspeed
    )

    wind_distance = (
        wind_component *
        glide_time
    )

    distances = (
        max_distance +
        wind_distance
    )

    distances = np.maximum(
        distances,
        0
    )

    x = (
        distances *
        np.sin(angles)
    )

    y = (
        distances *
        np.cos(angles)
    )

    return x, y, distances