import matplotlib.pyplot as plt

from landing.site_detection import find_reachable_sites
from simulation.aircraft import Aircraft
from reachability.reachable_area import generate_wind_aware_area


print("=================================")
print("        AERIS 0.4")
print("=================================")

aircraft = Aircraft()

aircraft.engine_failure()

print("\n--- AIRCRAFT ---")
print(f"Altitude: {aircraft.altitude} m")
print(f"Airspeed: {aircraft.airspeed} m/s")
print(f"Glide ratio: {aircraft.glide_ratio}:1")

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


reachable_sites = find_reachable_sites(
    sites,
    0,
    0,
    maximum_range / 1000
)


print("\n--- CANDIDATE LANDING SITES ---")

for site in reachable_sites:
    print(
        f"{site['name']} "
        f"({site['type']}) "
        f"- {site['distance']:.2f} km"
    )


# ---------------------------------
# Plot
# ---------------------------------

plt.figure(figsize=(9, 9))

# Reachable boundary
plt.plot(
    x / 1000,
    y / 1000,
    label="Reachable boundary"
)

# Aircraft
plt.scatter(0, 0, s=100)
plt.text(0, 0, "  AIRCRAFT")


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


plt.xlabel("East / West (km)")
plt.ylabel("North / South (km)")

plt.title("AERIS 0.4 — Candidate Landing Sites")

plt.axis("equal")
plt.grid(True)
plt.legend()

plt.show()