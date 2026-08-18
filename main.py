import matplotlib.pyplot as plt

from simulation.aircraft import Aircraft
from reachability.glide import calculate_glide_distance
from reachability.reachable_area import generate_reachable_area


print("=================================")
print("        AERIS 0.2")
print("=================================")

aircraft = Aircraft()

# Simulate emergency
aircraft.engine_failure()

# Calculate maximum theoretical glide distance
glide_distance = calculate_glide_distance(
    aircraft.altitude,
    aircraft.glide_ratio
)

print(f"\nTheoretical glide distance: {glide_distance / 1000:.2f} km")

# Generate reachable area
x, y = generate_reachable_area(glide_distance)

# Plot
plt.figure(figsize=(8, 8))

plt.plot(x / 1000, y / 1000)

# Aircraft position
plt.scatter(0, 0, s=100)

plt.text(0, 0, "  AIRCRAFT")

plt.xlabel("Distance East/West (km)")
plt.ylabel("Distance North/South (km)")

plt.title("AERIS — Theoretical Reachable Area")

plt.axis("equal")
plt.grid(True)

plt.show()