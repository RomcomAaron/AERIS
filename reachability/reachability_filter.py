import math


def calculate_distance(
    aircraft_latitude,
    aircraft_longitude,
    candidate_latitude,
    candidate_longitude
):
    """
    Calculate approximate distance between
    aircraft and candidate using the Haversine formula.

    Returns distance in kilometres.
    """

    earth_radius = 6371.0

    lat1 = math.radians(
        aircraft_latitude
    )

    lat2 = math.radians(
        candidate_latitude
    )

    delta_lat = math.radians(
        candidate_latitude -
        aircraft_latitude
    )

    delta_lon = math.radians(
        candidate_longitude -
        aircraft_longitude
    )

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


def filter_reachable_candidates(
    candidates,
    aircraft_latitude,
    aircraft_longitude,
    maximum_range_km
):
    """
    Remove geographic candidates that are
    outside the aircraft's current estimated
    reachable range.

    This is an initial screening model.
    """

    reachable = []

    print(
        "\n--- REACHABILITY FILTER ---"
    )

    for candidate in candidates:

        distance = calculate_distance(
            aircraft_latitude,
            aircraft_longitude,
            candidate["latitude"],
            candidate["longitude"]
        )

        candidate["distance"] = distance

        if distance <= maximum_range_km:

            candidate["reachable"] = True

            reachable.append(
                candidate
            )

        else:

            candidate["reachable"] = False

    print(
        f"Reachable candidates: "
        f"{len(reachable)}"
    )

    print(
        f"Unreachable candidates: "
        f"{len(candidates) - len(reachable)}"
    )

    return reachable