import matplotlib.pyplot as plt

from simulation.aircraft import Aircraft
from reachability.reachable_area import generate_wind_aware_area


print("=================================")
print("        AERIS 0.3")
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

# Generate reachable area
x, y, distances = generate_wind_aware_area(
    aircraft.altitude,
    aircraft.glide_ratio,
    aircraft.airspeed,
    aircraft.wind_speed,
    aircraft.wind_direction
)

# Find minimum and maximum reachable distances
minimum_range = distances.min()
maximum_range = distances.max()

print("\n--- REACHABILITY ---")
print(f"Minimum range: {minimum_range / 1000:.2f} km")
print(f"Maximum range: {maximum_range / 1000:.2f} km")

# Plot
plt.figure(figsize=(9, 9))

plt.plot(
    x / 1000,
    y / 1000,
    label="Wind-aware reachable boundary"
)

# Aircraft
plt.scatter(0, 0, s=100)

plt.text(0, 0, "  AIRCRAFT")

plt.xlabel("East / West (km)")
plt.ylabel("North / South (km)")

plt.title("AERIS 0.3 — Wind-Aware Reachability")

plt.axis("equal")
plt.grid(True)
plt.legend()

plt.show()