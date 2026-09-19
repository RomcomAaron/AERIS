import math
import geopandas as gpd


def estimate_dimensions(geometry):
    """
    Estimate approximate length, width and heading
    of a geographic feature.

    This is a screening estimate only.
    It is NOT an aviation safety certification.
    """

    try:

        gdf = gpd.GeoDataFrame(
            geometry=[geometry],
            crs="EPSG:4326"
        )

        # Use a projected coordinate system
        projected = gdf.to_crs(
            gdf.estimate_utm_crs()
        )

        geom = projected.geometry.iloc[0]

        # ---------------------------------
        # Polygon
        # ---------------------------------

        if geom.geom_type == "Polygon":

            rectangle = (
                geom.minimum_rotated_rectangle
            )

            coordinates = list(
                rectangle.exterior.coords
            )

            edges = []

            for i in range(
                len(coordinates) - 1
            ):

                x1, y1 = coordinates[i]
                x2, y2 = coordinates[i + 1]

                length = math.sqrt(
                    (x2 - x1) ** 2 +
                    (y2 - y1) ** 2
                )

                edges.append(
                    (
                        length,
                        x1,
                        y1,
                        x2,
                        y2
                    )
                )

            edges.sort(
                reverse=True,
                key=lambda x: x[0]
            )

            longest = edges[0][0]
            shortest = edges[1][0]

            x1 = edges[0][1]
            y1 = edges[0][2]
            x2 = edges[0][3]
            y2 = edges[0][4]

            heading = math.degrees(
                math.atan2(
                    x2 - x1,
                    y2 - y1
                )
            ) % 360

            return {
                "length": longest,
                "width": shortest,
                "heading": heading
            }

        # ---------------------------------
        # MultiPolygon
        # ---------------------------------

        elif geom.geom_type == "MultiPolygon":

            largest = max(
                geom.geoms,
                key=lambda polygon: polygon.area
            )

            rectangle = (
                largest.minimum_rotated_rectangle
            )

            coordinates = list(
                rectangle.exterior.coords
            )

            edges = []

            for i in range(
                len(coordinates) - 1
            ):

                x1, y1 = coordinates[i]
                x2, y2 = coordinates[i + 1]

                length = math.sqrt(
                    (x2 - x1) ** 2 +
                    (y2 - y1) ** 2
                )

                edges.append(
                    (
                        length,
                        x1,
                        y1,
                        x2,
                        y2
                    )
                )

            edges.sort(
                reverse=True,
                key=lambda x: x[0]
            )

            longest = edges[0][0]
            shortest = edges[1][0]

            x1 = edges[0][1]
            y1 = edges[0][2]
            x2 = edges[0][3]
            y2 = edges[0][4]

            heading = math.degrees(
                math.atan2(
                    x2 - x1,
                    y2 - y1
                )
            ) % 360

            return {
                "length": longest,
                "width": shortest,
                "heading": heading
            }

        # ---------------------------------
        # Lines
        # ---------------------------------

        elif geom.geom_type == "LineString":

            length = geom.length

            coordinates = list(
                geom.coords
            )

            if len(coordinates) >= 2:

                x1, y1 = coordinates[0]
                x2, y2 = coordinates[-1]

                heading = math.degrees(
                    math.atan2(
                        x2 - x1,
                        y2 - y1
                    )
                ) % 360

            else:

                heading = 0

            return {
                "length": length,
                "width": 10,
                "heading": heading
            }

    except Exception:

        pass

    return {
        "length": 0,
        "width": 0,
        "heading": 0
    }


def generate_candidates(
    classified_features,
    minimum_length=100,
    minimum_width=15,
    maximum_candidates=50
):
    """
    Generate geographic candidate landing areas.

    These are potential candidates only.
    They are NOT declared safe landing sites.
    """

    candidates = []

    print("\n--- GENERATING CANDIDATES ---")

    # ---------------------------------
    # Process only useful feature types
    # ---------------------------------

    useful_types = [
        "open_land",
        "recreational_area",
        "natural_area",
        "airport"
    ]

    useful_features = [
        feature
        for feature in classified_features
        if feature["type"] in useful_types
    ]

    print(
        f"Features considered: "
        f"{len(useful_features)}"
    )

    # ---------------------------------
    # Limit expensive processing
    # ---------------------------------

    for feature in useful_features:

        geometry = feature["geometry"]

        dimensions = estimate_dimensions(
            geometry
        )

        length = dimensions["length"]
        width = dimensions["width"]
        heading = dimensions["heading"]

        # -----------------------------
        # Size filter
        # -----------------------------

        if length < minimum_length:
            continue

        if width < minimum_width:
            continue

        # -----------------------------
        # Location
        # -----------------------------

        try:

            centroid = geometry.centroid

            latitude = centroid.y
            longitude = centroid.x

        except Exception:

            continue

        candidates.append({

            "type": feature["type"],

            "latitude": latitude,

            "longitude": longitude,

            "length": length,

            "width": width,

            "heading": heading,

            "geometry": geometry
        })

        if len(candidates) >= maximum_candidates:

            break

    print(
        f"Candidates generated: "
        f"{len(candidates)}"
    )

    return candidates