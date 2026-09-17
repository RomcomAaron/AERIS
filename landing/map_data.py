import osmnx as ox


def get_map_features(
    latitude,
    longitude,
    radius=5000
):
    """
    Download real OpenStreetMap features
    around the aircraft.

    radius is in metres.
    """

    print("\n--- DOWNLOADING MAP DATA ---")

    tags = {
        "highway": True,
        "aeroway": True,
        "landuse": True
    }

    try:

        features = ox.features_from_point(
            (latitude, longitude),
            tags=tags,
            dist=radius
        )

        print(
            f"Downloaded "
            f"{len(features)} map features."
        )

        return features

    except Exception as error:

        print(
            "Unable to download map data."
        )

        print(
            f"Error: {error}"
        )

        return None