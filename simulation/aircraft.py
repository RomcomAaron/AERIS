class Aircraft:

    def __init__(self):
        self.altitude = 3000.0       # metres
        self.airspeed = 65.0        # m/s
        self.mass = 1100.0          # kg
        self.glide_ratio = 10.0     # 10:1
        self.heading = 0.0          # degrees
        self.wind_speed = 30.0
        self.wind_direction = 90.0

        self.engine_running = True

    def engine_failure(self):
        self.engine_running = False
        print("\n⚠ ENGINE FAILURE")

    def status(self):
        print("\n--- AIRCRAFT STATUS ---")
        print(f"Altitude: {self.altitude} m")
        print(f"Airspeed: {self.airspeed} m/s")
        print(f"Mass: {self.mass} kg")
        print(f"Glide ratio: {self.glide_ratio}:1")
        print(
            f"Engine: "
            f"{'RUNNING' if self.engine_running else 'FAILED'}"
        )