def calculate_glide_distance(altitude, glide_ratio):
    """
    Calculate theoretical maximum horizontal glide distance.

    altitude: altitude above landing surface in metres
    glide_ratio: horizontal distance travelled per metre descended
    """

    distance = altitude * glide_ratio

    return distance