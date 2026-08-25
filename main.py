import matplotlib.pyplot as plt

from landing.approach import evaluate_approach
from landing.site_detection import find_reachable_sites
from landing.risk_engine import calculate_risk
from simulation.aircraft import Aircraft
from reachability.reachable_area import (
    generate_wind_aware_area
)


print("=================================")
print("        AERIS 0.7")
print("=================================")


# =================================
# CREATE AIRCRAFT
# =================================

aircraft = Aircraft()


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

sites = [

    {
        "name": "Field A",
        "type": "field",

        "x": 10,
        "y": 5,

        "length": 600,
        "width": 80,

        "surface": "grass",

        "slope": 2,

        "population": 10,

        "obstacles": 2,

        "heading": 20
    },


    {
        "name": "Highway B",
        "type": "highway",

        "x": 20,
        "y": 10,

        "length": 1200,
        "width": 20,

        "surface": "asphalt",

        "slope": 1,

        "population": 100,

        "obstacles": 5,

        "heading": 90
    },


    {
        "name": "Airport C",
        "type": "airport",

        "x": 35,
        "y": 5,

        "length": 2500,
        "width": 45,

        "surface": "asphalt",

        "slope": 1,

        "population": 20,

        "obstacles": 1,

        "heading": 100
    },


    {
        "name": "City D",
        "type": "city",

        "x": 15,
        "y": -10,

        "length": 300,
        "width": 50,

        "surface": "concrete",

        "slope": 4,

        "population": 5000,

        "obstacles": 20,

        "heading": 180
    },


    {
        "name": "Field E",
        "type": "field",

        "x": -12,
        "y": -8,

        "length": 250,
        "width": 40,

        "surface": "grass",

        "slope": 8,

        "population": 30,

        "obstacles": 8,

        "heading": 270
    }

]


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
        f"{'YES' if site['approach_feasible'] else 'NO'}"
    )


    print(
        f"{site['name']} "
        f"({site['type']}) "
        f"- Distance: "
        f"{site['distance']:.2f} km "
        f"- Risk: "
        f"{risk:.3f}"
    )


# =================================
# SORT BY RISK
# =================================

feasible_sites = [
    site
    for site in reachable_sites
    if site["approach_feasible"]
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
    "AERIS 0.6 — "
    "Emergency Landing Analysis"
)


plt.axis("equal")

plt.grid(True)

plt.legend()


plt.show()