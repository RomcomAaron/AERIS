from simulation.aircraft import Aircraft
from reachability.glide import calculate_glide_distance


print("=================================")
print("        AERIS 0.1")
print("=================================")

aircraft = Aircraft()

aircraft.status()

print("\nSimulating emergency...")
aircraft.engine_failure()

# Calculate theoretical glide distance
glide_distance = calculate_glide_distance(
    aircraft.altitude,
    aircraft.glide_ratio
)

print("\n--- REACHABILITY ---")
print(f"Theoretical glide distance: {glide_distance:.0f} m")
print(f"Theoretical glide distance: {glide_distance / 1000:.2f} km")