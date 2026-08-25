import matplotlib.pyplot as plt

from landing.coordinates import latlon_to_xy
from landing.site_loader import load_landing_sites
from landing.trajectory import evaluate_trajectory
from landing.approach import evaluate_approach
from landing.site_detection import find_reachable_sites
from landing.risk_engine import calculate_risk
from simulation.aircraft import Aircraft
from reachability.reachable_area import (
    generate_wind_aware_area
)


print("=================================")
print("        AERIS 1.0")
print("=================================")


# =================================
# CREATE AIRCRAFT
# =================================

aircraft = Aircraft()

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
# RANGE
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
# LANDING SITES
# =================================

sites = load_landing_sites(
    "data/landing_sites.json"
)

for site in sites:

    x, y = latlon_to_xy(

        site["latitude"],
        site["longitude"],

        aircraft_latitude,
        aircraft_longitude
    )

    site["x"] = x
    site["y"] = y

# =================================
# FIND REACHABLE SITES
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

print("\n--- CANDIDATE LANDING SITES ---")


for site in reachable_sites:

    # -----------------------------
    # Risk calculation
    # -----------------------------

    risk = calculate_risk(
        site,
        maximum_range / 1000
    )

    site["risk"] = risk


    # -----------------------------
    # Approach calculation
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
    # Trajectory calculation
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
# SORT BY RISK
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


feasible_sites.sort(
    key=lambda site:
    site["risk"]
)


# =================================
# RECOMMENDATION
# =================================

print("\n--- AERIS RECOMMENDATION ---")


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


# Reachable boundary

plt.plot(

    x / 1000,

    y / 1000,

    label="Reachable boundary"
)


# Aircraft

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


# Landing sites

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


# Graph labels

plt.xlabel(
    "East / West (km)"
)

plt.ylabel(
    "North / South (km)"
)


plt.title(
    "AERIS 1.0 — Geographic Emergency Landing Analysis"
)


plt.axis("equal")

plt.grid(True)

plt.legend()


plt.show()