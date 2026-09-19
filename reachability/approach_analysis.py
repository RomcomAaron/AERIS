import math


def angle_difference(angle1, angle2):
    """
    Calculate the smallest difference between
    two headings.

    Result: 0 to 180 degrees.
    """

    difference = abs(angle1 - angle2)

    if difference > 180:
        difference = 360 - difference

    return difference


def calculate_bearing(
    aircraft_latitude,
    aircraft_longitude,
    candidate_latitude,
    candidate_longitude
):
    """
    Calculate approximate bearing from the aircraft
    to the candidate.

    0° = North
    90° = East
    180° = South
    270° = West
    """

    lat1 = math.radians(
        aircraft_latitude
    )

    lat2 = math.radians(
        candidate_latitude
    )

    delta_longitude = math.radians(
        candidate_longitude -
        aircraft_longitude
    )

    x = (
        math.sin(delta_longitude)
        * math.cos(lat2)
    )

    y = (
        math.cos(lat1)
        * math.sin(lat2)
        -
        math.sin(lat1)
        * math.cos(lat2)
        * math.cos(delta_longitude)
    )

    bearing = math.degrees(
        math.atan2(x, y)
    )

    return (bearing + 360) % 360


def analyze_approach(
    candidate,
    aircraft_latitude,
    aircraft_longitude,
    wind_direction
):
    """
    Analyse the geometric approach to a candidate.

    This is a research prototype and does NOT
    determine whether an actual aircraft approach
    is operationally safe.
    """

    # ---------------------------------
    # Direction from aircraft
    # ---------------------------------

    bearing = calculate_bearing(
        aircraft_latitude,
        aircraft_longitude,
        candidate["latitude"],
        candidate["longitude"]
    )

    # ---------------------------------
    # Turn required
    # ---------------------------------

    turn_angle = angle_difference(
        bearing,
        candidate["heading"]
    )

    # ---------------------------------
    # Wind alignment
    # ---------------------------------

    # Aircraft ideally approaches into the wind.
    # Wind direction represents the direction
    # the wind is coming FROM.

    landing_direction = (
        candidate["heading"] + 180
    ) % 360

    wind_alignment = angle_difference(
        landing_direction,
        wind_direction
    )

    # ---------------------------------
    # Approach classification
    # ---------------------------------

    if turn_angle <= 30:

        turn_status = "GOOD"

    elif turn_angle <= 60:

        turn_status = "MODERATE"

    else:

        turn_status = "DIFFICULT"


    if wind_alignment <= 30:

        wind_status = "GOOD"

    elif wind_alignment <= 60:

        wind_status = "MODERATE"

    else:

        wind_status = "UNFAVORABLE"


    # ---------------------------------
    # Store results
    # ---------------------------------

    candidate["bearing"] = bearing

    candidate["turn_angle"] = turn_angle

    candidate["wind_alignment"] = wind_alignment

    candidate["turn_status"] = turn_status

    candidate["wind_status"] = wind_status

    return candidate


def analyze_candidates(
    candidates,
    aircraft_latitude,
    aircraft_longitude,
    wind_direction
):
    """
    Analyse approach geometry for all
    reachable candidates.
    """

    analyzed = []

    print(
        "\n--- APPROACH ANALYSIS ---"
    )

    for candidate in candidates:

        result = analyze_approach(
            candidate,
            aircraft_latitude,
            aircraft_longitude,
            wind_direction
        )

        analyzed.append(result)

    return analyzed