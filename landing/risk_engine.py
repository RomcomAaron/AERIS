def clamp(value, minimum=0.0, maximum=1.0):
    """
    Keep a value between minimum and maximum.
    """

    return max(
        minimum,
        min(value, maximum)
    )


# =================================
# DISTANCE RISK
# =================================

def calculate_distance_risk(
    distance,
    maximum_range
):
    """
    Distance risk.

    A candidate closer to the aircraft receives
    a lower distance-risk contribution.

    Prototype scoring model.
    """

    if maximum_range <= 0:
        return 1.0

    ratio = distance / maximum_range

    return clamp(ratio)


# =================================
# TURN RISK
# =================================

def calculate_turn_risk(turn_angle):
    """
    Risk contribution from required turn angle.
    """

    if turn_angle <= 30:
        return 0.0

    if turn_angle <= 60:
        return 0.35

    if turn_angle <= 90:
        return 0.70

    return 1.0


# =================================
# WIND RISK
# =================================

def calculate_wind_risk(wind_alignment):
    """
    Risk contribution from wind alignment.
    """

    if wind_alignment <= 30:
        return 0.0

    if wind_alignment <= 60:
        return 0.35

    if wind_alignment <= 90:
        return 0.70

    return 1.0


# =================================
# SIZE RISK
# =================================

def calculate_size_risk(
    length,
    width
):
    """
    Estimate geometric size risk.

    Larger areas receive lower risk.
    """

    if length >= 300:
        length_risk = 0.0

    elif length >= 200:
        length_risk = 0.25

    elif length >= 100:
        length_risk = 0.60

    else:
        length_risk = 1.0


    if width >= 50:
        width_risk = 0.0

    elif width >= 30:
        width_risk = 0.25

    elif width >= 15:
        width_risk = 0.60

    else:
        width_risk = 1.0


    return (
        length_risk * 0.6
        +
        width_risk * 0.4
    )


# =================================
# TYPE RISK
# =================================

def calculate_type_risk(
    candidate_type
):
    """
    Preliminary geographic feature risk.

    This is NOT a statement that a feature
    type is actually safe for aircraft landing.
    """

    type_risks = {

        "open_land": 0.10,

        "natural_area": 0.30,

        "recreational_area": 0.35,

        "airport": 0.05,

        "major_road": 0.50,

        "minor_road": 0.60
    }

    return type_risks.get(
        candidate_type,
        0.70
    )


# =================================
# NEW OSM CANDIDATE RISK
# =================================

def calculate_candidate_risk(
    candidate,
    maximum_range
):
    """
    Calculate risk for the NEW geographic
    OSM-based candidates.

    This requires:
        distance
        turn_angle
        wind_alignment
        length
        width
        type

    Prototype score only.
    """

    distance_risk = calculate_distance_risk(
        candidate["distance"],
        maximum_range
    )

    turn_risk = calculate_turn_risk(
        candidate["turn_angle"]
    )

    wind_risk = calculate_wind_risk(
        candidate["wind_alignment"]
    )

    size_risk = calculate_size_risk(
        candidate["length"],
        candidate["width"]
    )

    type_risk = calculate_type_risk(
        candidate["type"]
    )


    # ---------------------------------
    # Weighted risk model
    # ---------------------------------

    total_risk = (

        distance_risk * 0.20

        +

        turn_risk * 0.20

        +

        wind_risk * 0.20

        +

        size_risk * 0.25

        +

        type_risk * 0.15
    )


    total_risk = clamp(
        total_risk
    )


    candidate["distance_risk"] = (
        distance_risk
    )

    candidate["turn_risk"] = (
        turn_risk
    )

    candidate["wind_risk"] = (
        wind_risk
    )

    candidate["size_risk"] = (
        size_risk
    )

    candidate["type_risk"] = (
        type_risk
    )

    candidate["risk_score"] = (
        total_risk
    )


    return candidate


# =================================
# NEW CANDIDATE RANKING
# =================================

def rank_candidates(
    candidates,
    maximum_range
):
    """
    Rank NEW OSM candidates by their
    prototype risk score.

    Lower modeled risk appears first.
    """

    analyzed = []


    for candidate in candidates:

        result = calculate_candidate_risk(
            candidate,
            maximum_range
        )

        analyzed.append(
            result
        )


    analyzed.sort(
        key=lambda candidate:
        candidate["risk_score"]
    )


    return analyzed


# =================================
# OLD / MANUAL SITE RISK
# =================================

def calculate_risk(
    site,
    maximum_range
):
    """
    Risk calculation for the ORIGINAL
    manual landing-site system.

    Kept separate from the new OSM
    candidate risk engine so the old
    AERIS pipeline remains compatible.
    """

    distance_risk = calculate_distance_risk(
        site["distance"],
        maximum_range
    )


    # The original manual sites do not
    # contain turn/wind information when
    # this function is called.

    size_risk = calculate_size_risk(
        site.get("length", 300),
        site.get("width", 50)
    )


    type_risk = calculate_type_risk(
        site.get("type", "unknown")
    )


    total_risk = (

        distance_risk * 0.50

        +

        size_risk * 0.30

        +

        type_risk * 0.20
    )


    return clamp(
        total_risk
    )