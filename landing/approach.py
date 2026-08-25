import math


def normalize_angle(angle):
    """
    Convert an angle to the range 0–360 degrees.
    """

    return angle % 360


def calculate_turn_angle(
    aircraft_heading,
    target_heading
):
    """
    Calculate the smallest angle the aircraft
    needs to turn.
    """

    aircraft_heading = normalize_angle(
        aircraft_heading
    )

    target_heading = normalize_angle(
        target_heading
    )

    difference = abs(
        target_heading -
        aircraft_heading
    )

    if difference > 180:
        difference = 360 - difference

    return difference


def evaluate_approach(
    aircraft_heading,
    site_heading,
    maximum_turn=45
):
    """
    Determine whether a simplified approach
    is feasible.

    Lower turn angle = better.

    This is a simulation model and NOT
    intended for real flight operations.
    """

    turn_angle = calculate_turn_angle(
        aircraft_heading,
        site_heading
    )

    if turn_angle <= maximum_turn:

        feasible = True

    else:

        feasible = False

    return {
        "turn_angle": turn_angle,
        "feasible": feasible
    }