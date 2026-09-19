import matplotlib.pyplot as plt

from landing.coordinates import latlon_to_xy
from landing.site_loader import load_landing_sites
from landing.trajectory import evaluate_trajectory
from landing.approach import evaluate_approach
from landing.site_detection import find_reachable_sites
from landing.risk_engine import calculate_risk

from simulation.aircraft import Aircraft

from landing.map_data import (
    get_map_features,
    classify_features
)

from landing.candidate_generator import (
    generate_candidates
)

from reachability.reachable_area import (
    generate_wind_aware_area
)

from reachability.reachability_filter import (
    filter_reachable_candidates
)

from reachability.approach_analysis import (
    analyze_candidates
)


print("=================================")
print("        AERIS 1.6")
print("=================================")


# =================================
# CREATE AIRCRAFT
# =================================

aircraft = Aircraft()


# =================================
# AIRCRAFT LOCATION
# =================================

aircraft_latitude = 13.0827
aircraft_longitude = 80.2707


# =================================
# SIMULATE EMERGENCY
# =================================

aircraft.engine_failure()


# =================================
# AIRCRAFT INFORMATION
# =================================

print("\n--- AIRCRAFT ---")

print(
    f"Altitude: "
    f"{aircraft.altitude} m"
)

print(
    f"Airspeed: "
    f"{aircraft.airspeed} m/s"
)

print(
    f"Glide ratio: "
    f"{aircraft.glide_ratio}:1"
)


# =================================
# WIND INFORMATION
# =================================

print("\n--- WIND ---")

print(
    f"Wind speed: "
    f"{aircraft.wind_speed} m/s"
)

print(
    f"Wind direction: "
    f"{aircraft.wind_direction}°"
)


# =================================
# GENERATE REACHABLE AREA
# =================================

x, y, distances = generate_wind_aware_area(

    aircraft.altitude,

    aircraft.glide_ratio,

    aircraft.airspeed,

    aircraft.wind_speed,

    aircraft.wind_direction
)


# =================================
# CALCULATE REACHABLE RANGE
# =================================

minimum_range = distances.min()

maximum_range = distances.max()


print("\n--- REACHABILITY ---")

print(
    f"Minimum range: "
    f"{minimum_range / 1000:.2f} km"
)

print(
    f"Maximum range: "
    f"{maximum_range / 1000:.2f} km"
)


# =================================
# DOWNLOAD REAL MAP DATA
# =================================

map_features = get_map_features(

    aircraft_latitude,

    aircraft_longitude,

    radius=5000
)


# =================================
# CLASSIFY MAP FEATURES
# =================================

classified_features = classify_features(
    map_features
)


# =================================
# MAP FEATURE SUMMARY
# =================================

print("\n--- MAP FEATURE SUMMARY ---")

feature_counts = {}


for feature in classified_features:

    feature_type = feature["type"]

    if feature_type not in feature_counts:

        feature_counts[feature_type] = 0

    feature_counts[feature_type] += 1


for feature_type, count in feature_counts.items():

    print(
        f"{feature_type}: {count}"
    )


# =================================
# GENERATE GEOGRAPHIC CANDIDATES
# =================================

candidates = generate_candidates(

    classified_features,

    minimum_length=100,

    minimum_width=15,

    maximum_candidates=50
)


# =================================
# DISPLAY GEOGRAPHIC CANDIDATES
# =================================

print(
    "\n--- AERIS GEOGRAPHIC CANDIDATES ---"
)

print(
    f"Candidates found: "
    f"{len(candidates)}"
)


for i, candidate in enumerate(
    candidates,
    start=1
):

    print(

        f"{i}. "

        f"{candidate['type']} | "

        f"Length: "
        f"{candidate['length']:.0f} m | "

        f"Width: "
        f"{candidate['width']:.0f} m | "

        f"Heading: "
        f"{candidate['heading']:.1f}° | "

        f"Location: "
        f"{candidate['latitude']:.5f}, "
        f"{candidate['longitude']:.5f}"

    )


# =================================
# FILTER BY AIRCRAFT REACHABILITY
# =================================

reachable_candidates = (
    filter_reachable_candidates(

        candidates,

        aircraft_latitude,

        aircraft_longitude,

        maximum_range / 1000
    )
)

analyzed_candidates = analyze_candidates(
    reachable_candidates,
    aircraft_latitude,
    aircraft_longitude,
    aircraft.wind_direction
)

print(
    "\n--- APPROACH RESULTS ---"
)

for i, candidate in enumerate(
    analyzed_candidates,
    start=1
):

    print(
        f"{i}. "
        f"{candidate['type']} | "
        f"Distance: "
        f"{candidate['distance']:.2f} km | "
        f"Turn: "
        f"{candidate['turn_angle']:.1f}° "
        f"({candidate['turn_status']}) | "
        f"Wind alignment: "
        f"{candidate['wind_alignment']:.1f}° "
        f"({candidate['wind_status']})"
    )


# =================================
# DISPLAY REACHABLE CANDIDATES
# =================================

print(
    "\n--- REACHABLE LANDING CANDIDATES ---"
)

print(
    f"Reachable candidates: "
    f"{len(reachable_candidates)}"
)


for i, candidate in enumerate(

    reachable_candidates,

    start=1

):

    print(

        f"{i}. "

        f"{candidate['type']} | "

        f"Distance: "
        f"{candidate['distance']:.2f} km | "

        f"Length: "
        f"{candidate['length']:.0f} m | "

        f"Width: "
        f"{candidate['width']:.0f} m | "

        f"Heading: "
        f"{candidate['heading']:.1f}°"

    )


# =================================
# OLD / MANUAL LANDING SITES
# =================================
# Kept for compatibility with the
# existing AERIS risk/trajectory system.
# =================================

sites = load_landing_sites(
    "data/landing_sites.json"
)


for site in sites:

    x_site, y_site = latlon_to_xy(

        site["latitude"],

        site["longitude"],

        aircraft_latitude,

        aircraft_longitude
    )

    site["x"] = x_site

    site["y"] = y_site


# =================================
# FIND REACHABLE MANUAL SITES
# =================================

reachable_sites = find_reachable_sites(

    sites,

    0,

    0,

    maximum_range / 1000
)


# =================================
# RISK ANALYSIS
# =================================

print(
    "\n--- CANDIDATE LANDING SITES ---"
)


for site in reachable_sites:

    # -----------------------------
    # Risk
    # -----------------------------

    risk = calculate_risk(

        site,

        maximum_range / 1000
    )

    site["risk"] = risk


    # -----------------------------
    # Approach
    # -----------------------------

    approach = evaluate_approach(

        aircraft.heading,

        site["heading"],

        maximum_turn=45
    )

    site["turn_angle"] = (
        approach["turn_angle"]
    )

    site["approach_feasible"] = (
        approach["feasible"]
    )


    # -----------------------------
    # Trajectory
    # -----------------------------

    trajectory = evaluate_trajectory(

        aircraft.altitude,

        aircraft.glide_ratio,

        0,

        0,

        aircraft.heading,

        site["x"],

        site["y"]
    )

    site["trajectory_feasible"] = (
        trajectory["feasible"]
    )

    site["bearing"] = (
        trajectory["bearing"]
    )

    site["remaining_altitude"] = (
        trajectory["remaining_altitude"]
    )


    # -----------------------------
    # Display
    # -----------------------------

    print(

        f"{site['name']} "

        f"({site['type']}) "

        f"- Distance: "
        f"{site['distance']:.2f} km "

        f"- Risk: "
        f"{risk:.3f} "

        f"- Turn: "
        f"{site['turn_angle']:.1f}° "

        f"- Approach: "
        f"{'YES' if site['approach_feasible'] else 'NO'} "

        f"- Altitude margin: "
        f"{site['remaining_altitude']:.0f} m "

        f"- Trajectory: "
        f"{'YES' if site['trajectory_feasible'] else 'NO'}"

    )


# =================================
# FIND FEASIBLE MANUAL SITES
# =================================

feasible_sites = [

    site

    for site in reachable_sites

    if (

        site["approach_feasible"]

        and

        site["trajectory_feasible"]

    )

]


# =================================
# SORT BY RISK
# =================================

feasible_sites.sort(

    key=lambda site:
    site["risk"]

)


# =================================
# RECOMMENDATION
# =================================

print(
    "\n--- AERIS RECOMMENDATION ---"
)


if feasible_sites:

    best_site = feasible_sites[0]


    print(

        f"Recommended site: "
        f"{best_site['name']}"

    )

    print(

        f"Type: "
        f"{best_site['type']}"

    )

    print(

        f"Distance: "
        f"{best_site['distance']:.2f} km"

    )

    print(

        f"Risk score: "
        f"{best_site['risk']:.3f}"

    )

else:

    print(
        "NO REACHABLE SITE WITH "
        "FEASIBLE APPROACH FOUND"
    )


# =================================
# PLOT
# =================================

plt.figure(
    figsize=(9, 9)
)


# =================================
# REACHABLE BOUNDARY
# =================================

plt.plot(

    x / 1000,

    y / 1000,

    label="Reachable boundary"
)


# =================================
# AIRCRAFT
# =================================

plt.scatter(

    0,

    0,

    s=100
)


plt.text(

    0,

    0,

    "  AIRCRAFT"
)


# =================================
# MANUAL LANDING SITES
# =================================

for site in sites:

    if site in reachable_sites:

        marker = "o"

    else:

        marker = "x"


    plt.scatter(

        site["x"],

        site["y"],

        marker=marker,

        s=100
    )


    plt.text(

        site["x"],

        site["y"],

        f"  {site['name']}"

    )


# =================================
# GRAPH LABELS
# =================================

plt.xlabel(
    "East / West (km)"
)

plt.ylabel(
    "North / South (km)"
)


plt.title(
    "AERIS 1.6 — Approach & Landing Direction Analysis"
)


plt.axis("equal")

plt.grid(True)

plt.legend()


plt.show()