def calculate_risk(site, maximum_range):
    """
    Calculate a simplified landing risk score.

    Lower score = safer landing location.

    This is a simulation model and is NOT
    intended for real flight operations.
    """

    # ---------------------------------
    # 1. Distance risk
    # ---------------------------------

    distance_ratio = site["distance"] / maximum_range

    distance_risk = min(distance_ratio, 1.0)


    # ---------------------------------
    # 2. Surface risk
    # ---------------------------------

    surface_risk = {
        "grass": 0.25,
        "asphalt": 0.05,
        "concrete": 0.10
    }

    surface = surface_risk.get(
        site["surface"],
        0.50
    )


    # ---------------------------------
    # 3. Length risk
    # ---------------------------------

    # Longer landing area = safer

    if site["length"] >= 1000:
        length_risk = 0.05

    elif site["length"] >= 500:
        length_risk = 0.20

    elif site["length"] >= 300:
        length_risk = 0.50

    else:
        length_risk = 0.90


    # ---------------------------------
    # 4. Width risk
    # ---------------------------------

    if site["width"] >= 50:
        width_risk = 0.10

    elif site["width"] >= 30:
        width_risk = 0.40

    else:
        width_risk = 0.80


    # ---------------------------------
    # 5. Slope risk
    # ---------------------------------

    slope = site["slope"]

    if slope <= 2:
        slope_risk = 0.05

    elif slope <= 5:
        slope_risk = 0.30

    elif slope <= 8:
        slope_risk = 0.60

    else:
        slope_risk = 0.90


    # ---------------------------------
    # 6. Population risk
    # ---------------------------------

    population_risk = min(
        site["population"] / 5000,
        1.0
    )


    # ---------------------------------
    # 7. Obstacle risk
    # ---------------------------------

    obstacle_risk = min(
        site["obstacles"] / 20,
        1.0
    )


    # ---------------------------------
    # 8. Final weighted risk
    # ---------------------------------

    risk_score = (

        0.15 * distance_risk +

        0.10 * surface +

        0.20 * length_risk +

        0.10 * width_risk +

        0.15 * slope_risk +

        0.20 * population_risk +

        0.10 * obstacle_risk
    )


    return risk_score