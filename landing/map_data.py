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


def classify_features(features):
    """
    Classify OpenStreetMap features into
    broad categories useful to AERIS.
    """

    if features is None:
        return []

    classified = []

    for _, feature in features.iterrows():

        feature_type = "unknown"

        # -----------------------------
        # Airport / runway
        # -----------------------------

        if feature.get("aeroway") in [
            "aerodrome",
            "runway",
            "helipad"
        ]:

            feature_type = "airport"


        # -----------------------------
        # Roads
        # -----------------------------

        elif feature.get("highway"):

            feature_type = "road"


        # -----------------------------
        # Land
        # -----------------------------

        elif feature.get("landuse") in [
            "farmland",
            "meadow",
            "grass"
        ]:

            feature_type = "open_land"


        # -----------------------------
        # Save feature
        # -----------------------------

        if feature_type != "unknown":

            classified.append({

                "type": feature_type,

                "geometry":
                    feature.geometry

            })

    return classified