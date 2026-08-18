def calculate_risk(site, maximum_range):
    """
    Calculate a simplified landing risk score.

    Lower score = safer landing location.
    """

    # Distance risk
    distance_ratio = site["distance"] / maximum_range

    # Limit distance contribution
    distance_risk = min(distance_ratio, 1.0)

    # Surface risk
    surface_risk = {
        "field": 0.2,
        "highway": 0.4,
        "airport": 0.05,
        "city": 0.9
    }

    # Population risk
    population_risk = {
        "field": 0.1,
        "highway": 0.4,
        "airport": 0.1,
        "city": 1.0
    }

    # Obstacle risk
    obstacle_risk = {
        "field": 0.3,
        "highway": 0.5,
        "airport": 0.1,
        "city": 0.9
    }

    site_type = site["type"]

    # Weighted risk score
    risk_score = (
        0.25 * distance_risk +
        0.30 * surface_risk[site_type] +
        0.30 * population_risk[site_type] +
        0.15 * obstacle_risk[site_type]
    )

    return risk_score