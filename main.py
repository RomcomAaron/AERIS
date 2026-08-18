import matplotlib.pyplot as plt

from landing.site_detection import find_reachable_sites
from landing.risk_engine import calculate_risk
from simulation.aircraft import Aircraft
from reachability.reachable_area import generate_wind_aware_area


print("=================================")
print("        AERIS 0.5")
print("=================================")

# ---------------------------------
# Create aircraft
# ---------------------------------

aircraft = Aircraft()

# Simulate emergency
aircraft.engine_failure()


# ---------------------------------
# Aircraft information
# ---------------------------------

print("\n--- AIRCRAFT ---")
print(f"Altitude: {aircraft.altitude} m")
print(f"Airspeed: {aircraft.airspeed} m/s")
print(f"Glide ratio: {aircraft.glide_ratio}:1")


# ---------------------------------
# Wind information
# ---------------------------------

print("\n--- WIND ---")
print(f"Wind speed: {aircraft.wind_speed} m/s")
print(f"Wind direction: {aircraft.wind_direction}°")


# ---------------------------------
# Generate reachable area
# ---------------------------------

x, y, distances = generate_wind_aware_area(
    aircraft.altitude,
    aircraft.glide_ratio,
    aircraft.airspeed,
    aircraft.wind_speed,
    aircraft.wind_direction
)


# Find minimum and maximum range
minimum_range = distances.min()
maximum_range = distances.max()

print("\n--- REACHABILITY ---")
print(f"Minimum range: {minimum_range / 1000:.2f} km")
print(f"Maximum range: {maximum_range / 1000:.2f} km")


# ---------------------------------
# Candidate landing sites
# ---------------------------------

sites = [
    {
        "name": "Field A",
        "type": "field",
        "x": 10,
        "y": 5
    },
    {
        "name": "Highway B",
        "type": "highway",
        "x": 20,
        "y": 10
    },
    {
        "name": "Airport C",
        "type": "airport",
        "x": 35,
        "y": 5
    },
    {
        "name": "City D",
        "type": "city",
        "x": 15,
        "y": -10
    },
    {
        "name": "Field E",
        "type": "field",
        "x": -12,
        "y": -8
    }
]


# ---------------------------------
# Find reachable sites
# ---------------------------------

reachable_sites = find_reachable_sites(
    sites,
    0,
    0,
    maximum_range / 1000
)


# ---------------------------------
# Calculate risk
# ---------------------------------

print("\n--- CANDIDATE LANDING SITES ---")

for site in reachable_sites:

    risk = calculate_risk(
        site,
        maximum_range / 1000
    )

    site["risk"] = risk

    print(
        f"{site['name']} "
        f"({site['type']}) "
        f"- {site['distance']:.2f} km "
        f"- Risk: {risk:.3f}"
    )


# ---------------------------------
# Rank landing sites
# ---------------------------------

reachable_sites.sort(
    key=lambda site: site["risk"]
)


# ---------------------------------
# AERIS recommendation
# ---------------------------------

print("\n--- AERIS RECOMMENDATION ---")

if reachable_sites:

    best_site = reachable_sites[0]

    print(f"Recommended site: {best_site['name']}")
    print(f"Type: {best_site['type']}")
    print(f"Distance: {best_site['distance']:.2f} km")
    print(f"Risk score: {best_site['risk']:.3f}")

else:

    print("NO REACHABLE LANDING SITE FOUND")


# ---------------------------------
# Plot reachable area
# ---------------------------------

plt.figure(figsize=(9, 9))


# Reachable boundary

plt.plot(
    x / 1000,
    y / 1000,
    label="Reachable boundary"
)


# Aircraft position

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


# ---------------------------------
# Plot landing sites
# ---------------------------------

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


# ---------------------------------
# Graph settings
# ---------------------------------

plt.xlabel("East / West (km)")
plt.ylabel("North / South (km)")

plt.title(
    "AERIS 0.5 — Emergency Landing Site Analysis"
)

plt.axis("equal")

plt.grid(True)

plt.legend()

plt.show()