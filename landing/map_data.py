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
        "landuse": True,
        "natural": True,
        "leisure": True
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

        # ---------------------------------
        # DEBUG: Inspect OSM tags
        # ---------------------------------

        print("\n--- OSM TAG INSPECTION ---")

        for column in [
            "landuse",
            "natural",
            "leisure",
            "highway",
            "aeroway"
        ]:

            if column in features.columns:

                values = (
                    features[column]
                    .dropna()
                    .astype(str)
                    .value_counts()
                    .head(15)
                )

                print(f"\n{column}:")

                if len(values) == 0:

                    print("  No values found.")

                else:

                    for value, count in values.items():

                        print(
                            f"  {value}: {count}"
                        )

            else:

                print(
                    f"\n{column}: COLUMN NOT FOUND"
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
    categories relevant to AERIS.

    Classification does NOT mean that a
    location is safe for landing.
    """

    if features is None:
        return []

    classified = []

    for _, feature in features.iterrows():

        feature_type = "unknown"

        # ---------------------------------
        # 1. AIRPORT / RUNWAY / HELIPAD
        # ---------------------------------

        if feature.get("aeroway") in [
            "aerodrome",
            "runway",
            "helipad"
        ]:

            feature_type = "airport"


        # ---------------------------------
        # 2. OPEN LAND
        # ---------------------------------

        elif feature.get("landuse") in [
            "grass",
            "farmland",
            "meadow",
            "recreation_ground",
            "village_green",
            "brownfield"
        ]:

            feature_type = "open_land"


        # ---------------------------------
        # 3. RECREATIONAL AREAS
        # ---------------------------------

        elif feature.get("leisure") in [
            "park",
            "pitch",
            "common"
        ]:

            feature_type = "recreational_area"


        # ---------------------------------
        # 4. NATURAL OPEN AREAS
        # ---------------------------------

        elif feature.get("natural") in [
            "grassland",
            "heath"
        ]:

            feature_type = "natural_area"


        # ---------------------------------
        # 5. ROADS
        # ---------------------------------

        elif feature.get("highway"):

            highway_type = feature.get(
                "highway"
            )

            if highway_type in [
                "motorway",
                "trunk",
                "primary",
                "secondary",
                "tertiary"
            ]:

                feature_type = "major_road"

            elif highway_type in [
                "residential",
                "living_street"
            ]:

                feature_type = "minor_road"


        # ---------------------------------
        # 6. SAVE
        # ---------------------------------

        if feature_type != "unknown":

            classified.append({
                "type": feature_type,
                "geometry": feature.geometry
            })

    return classified