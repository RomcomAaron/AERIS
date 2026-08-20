class Aircraft:

    def __init__(self):

        self.altitude = 3000.0

        self.airspeed = 65.0

        self.mass = 1100.0

        self.glide_ratio = 10.0

        self.heading = 0.0

        self.wind_speed = 15.0

        self.wind_direction = 90.0

        self.engine_running = True


    def engine_failure(self):

        self.engine_running = False

        print("\n⚠ ENGINE FAILURE")


    def status(self):

        print("\n--- AIRCRAFT STATUS ---")

        print(
            f"Altitude: "
            f"{self.altitude} m"
        )

        print(
            f"Airspeed: "
            f"{self.airspeed} m/s"
        )

        print(
            f"Mass: "
            f"{self.mass} kg"
        )

        print(
            f"Glide ratio: "
            f"{self.glide_ratio}:1"
        )

        print(
            f"Engine: "
            f"{'RUNNING' if self.engine_running else 'FAILED'}"
        )