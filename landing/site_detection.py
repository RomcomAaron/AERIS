import math


def calculate_distance(x1, y1, x2, y2):
    """
    Calculate straight-line distance between two points.
    """

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def find_reachable_sites(sites, aircraft_x, aircraft_y, max_range):
    """
    Find landing sites that are within the aircraft's
    theoretical maximum range.

    Coordinates are in kilometres.
    """

    reachable_sites = []

    for site in sites:

        distance = calculate_distance(
            aircraft_x,
            aircraft_y,
            site["x"],
            site["y"]
        )

        if distance <= max_range:
            site_copy = site.copy()
            site_copy["distance"] = distance
            site_copy["reachable"] = True

            reachable_sites.append(site_copy)

    return reachable_sites