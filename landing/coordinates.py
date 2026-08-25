import math


EARTH_RADIUS_KM = 6371.0


def latlon_to_xy(
    latitude,
    longitude,
    origin_latitude,
    origin_longitude
):
    """
    Convert latitude/longitude into a local
    X/Y coordinate system in kilometres.

    X = East/West
    Y = North/South
    """

    latitude_difference = math.radians(
        latitude - origin_latitude
    )

    longitude_difference = math.radians(
        longitude - origin_longitude
    )

    mean_latitude = math.radians(
        (latitude + origin_latitude) / 2
    )

    x = (
        longitude_difference
        * EARTH_RADIUS_KM
        * math.cos(mean_latitude)
    )

    y = (
        latitude_difference
        * EARTH_RADIUS_KM
    )

    return x, y