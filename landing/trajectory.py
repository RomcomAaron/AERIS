import math


def calculate_bearing(
    aircraft_x,
    aircraft_y,
    site_x,
    site_y
):
    """
    Calculate the bearing from the aircraft
    to the landing site.

    Coordinates are in kilometres.
    """

    dx = site_x - aircraft_x
    dy = site_y - aircraft_y

    angle = math.degrees(
        math.atan2(dx, dy)
    )

    return angle % 360


def calculate_glide_altitude(
    altitude,
    distance,
    glide_ratio
):
    """
    Estimate altitude required to travel
    a given distance using the aircraft's
    glide ratio.

    altitude -> metres
    distance -> kilometres
    """

    distance_m = distance * 1000

    required_altitude = (
        distance_m / glide_ratio
    )

    remaining_altitude = (
        altitude - required_altitude
    )

    return remaining_altitude


def evaluate_trajectory(
    altitude,
    glide_ratio,
    aircraft_x,
    aircraft_y,
    aircraft_heading,
    site_x,
    site_y
):
    """
    Simplified trajectory feasibility model.

    This is a simulation and NOT an
    operational flight model.
    """

    # -----------------------------
    # Distance
    # -----------------------------

    dx = site_x - aircraft_x
    dy = site_y - aircraft_y

    distance = math.sqrt(
        dx ** 2 +
        dy ** 2
    )


    # -----------------------------
    # Required bearing
    # -----------------------------

    bearing = calculate_bearing(
        aircraft_x,
        aircraft_y,
        site_x,
        site_y
    )


    # -----------------------------
    # Required turn
    # -----------------------------

    turn_angle = abs(
        bearing -
        aircraft_heading
    )

    if turn_angle > 180:
        turn_angle = 360 - turn_angle


    # -----------------------------
    # Glide altitude
    # -----------------------------

    remaining_altitude = (
        calculate_glide_altitude(
            altitude,
            distance,
            glide_ratio
        )
    )


    # -----------------------------
    # Trajectory feasibility
    # -----------------------------

    altitude_available = (
        remaining_altitude >= 0
    )

    turn_feasible = (
        turn_angle <= 45
    )

    trajectory_feasible = (
        altitude_available
        and
        turn_feasible
    )


    return {
        "distance": distance,
        "bearing": bearing,
        "turn_angle": turn_angle,
        "remaining_altitude": remaining_altitude,
        "feasible": trajectory_feasible
    }