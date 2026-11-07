
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# 1. CONSTANTS AND VARIANT 7 INPUT DATA
# =====================================================

R_EARTH = 6371.0
MU = 398600.44
OMEGA_EARTH = 7.2921159e-5

HP = 700.0
HA = 800.0
INC_DEG = 80.0

RAAN_LIST = [0, 72, 144, 216, 288]

# Temporary assumptions: confirm with lecturer
ARG_PERIGEE_DEG = 0.0
THETA0_DEG = 0.0

# Observation objects: approximate city-centre coordinates
# Latitude and longitude in degrees
objects = {
    "Izhevsk": (56.8498, 53.2045),
    "Baikonur": (45.6167, 63.3167),
    "Saratov": (51.5333, 46.0342)
}

MIN_ELEVATION_DEG = 10.0
TIME_STEP = 30.0

# =====================================================
# 2. CALCULATE ORBITAL PARAMETERS
# =====================================================

rp = R_EARTH + HP
ra = R_EARTH + HA

a = (rp + ra) / 2
e = (ra - rp) / (ra + rp)

p = a * (1 - e**2)

T = 2 * math.pi * math.sqrt(a**3 / MU)
n = 2 * math.pi / T

inc = math.radians(INC_DEG)
argp = math.radians(ARG_PERIGEE_DEG)

print("Semi-major axis:", a, "km")
print("Eccentricity:", e)
print("Orbital period:", T / 60, "minutes")
print("Mean motion:", n, "rad/s")

# =====================================================
# 3. INITIAL TRUE ANOMALY TO INITIAL MEAN ANOMALY
# =====================================================

theta0 = math.radians(THETA0_DEG)

E0 = math.atan2(
    math.sqrt(1 - e**2) * math.sin(theta0),
    e + math.cos(theta0)
)

M0 = E0 - e * math.sin(E0)

# =====================================================
# 4. TIME ARRAY
# =====================================================

times = np.arange(0, 2 * T + TIME_STEP, TIME_STEP)

# =====================================================
# 5. PREPARE DATA STORAGE
# =====================================================

ground_track_data = []
capture_data = []

# =====================================================
# 6. CONVERT OBSERVATION OBJECTS TO ECEF
# =====================================================

object_ecef = {}

for name, (lat_deg, lon_deg) in objects.items():

    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)

    x = R_EARTH * math.cos(lat) * math.cos(lon)
    y = R_EARTH * math.cos(lat) * math.sin(lon)
    z = R_EARTH * math.sin(lat)

    object_ecef[name] = np.array([x, y, z])

# =====================================================
# 7. CALCULATE EACH SPACECRAFT TRAJECTORY
# =====================================================

for satellite_number, raan_deg in enumerate(RAAN_LIST, start=1):

    raan = math.radians(raan_deg)

    for t in times:

        # ---------------------------------------------
        # A. Mean anomaly
        # ---------------------------------------------

        M = M0 + n * t

        # ---------------------------------------------
        # B. Solve Kepler's equation using Newton method
        # ---------------------------------------------

        E = M

        for _ in range(10):
            E = E - (
                (E - e * math.sin(E) - M) /
                (1 - e * math.cos(E))
            )

        # ---------------------------------------------
        # C. Calculate true anomaly
        # ---------------------------------------------

        theta = math.atan2(
            math.sqrt(1 - e**2) * math.sin(E),
            math.cos(E) - e
        )

        # ---------------------------------------------
        # D. Calculate orbital radius
        # ---------------------------------------------

        r = p / (1 + e * math.cos(theta))

        # ---------------------------------------------
        # E. Calculate argument of latitude
        # ---------------------------------------------

        u = argp + theta

        # ---------------------------------------------
        # F. Orbital plane coordinates -> ECI
        # ---------------------------------------------

        x_eci = r * (
            math.cos(raan) * math.cos(u)
            - math.sin(raan) * math.sin(u) * math.cos(inc)
        )

        y_eci = r * (
            math.sin(raan) * math.cos(u)
            + math.cos(raan) * math.sin(u) * math.cos(inc)
        )

        z_eci = r * math.sin(u) * math.sin(inc)

        # ---------------------------------------------
        # G. ECI -> ECEF (simplified Earth rotation)
        # ---------------------------------------------

        alpha = OMEGA_EARTH * t

        x_ecef = (
            x_eci * math.cos(alpha)
            + y_eci * math.sin(alpha)
        )

        y_ecef = (
            -x_eci * math.sin(alpha)
            + y_eci * math.cos(alpha)
        )

        z_ecef = z_eci

        # ---------------------------------------------
        # H. ECEF -> latitude and longitude
        # ---------------------------------------------

        lat = math.degrees(
            math.atan2(
                z_ecef,
                math.sqrt(x_ecef**2 + y_ecef**2)
            )
        )

        lon = math.degrees(
            math.atan2(y_ecef, x_ecef)
        )

        # Convert longitude to 0–360 degrees
        lon_360 = lon % 360

        ground_track_data.append({
            "satellite": satellite_number,
            "time_s": t,
            "latitude": lat,
            "longitude": lon_360,
            "altitude_km": r - R_EARTH
        })

        # ---------------------------------------------
        # I. Calculate visibility of observation objects
        # ---------------------------------------------

        satellite_position = np.array([
            x_ecef, y_ecef, z_ecef
        ])

        for object_name, site_position in object_ecef.items():

            line_of_sight = (
                satellite_position - site_position
            )

            distance = np.linalg.norm(line_of_sight)

            # Local vertical direction at observation object
            up = site_position / R_EARTH

            sin_elevation = np.dot(
                line_of_sight, up
            ) / distance

            sin_elevation = np.clip(
                sin_elevation, -1.0, 1.0
            )

            elevation = math.degrees(
                math.asin(sin_elevation)
            )

            visible = int(
                elevation >= MIN_ELEVATION_DEG
            )

            capture_data.append({
                "satellite": satellite_number,
                "object": object_name,
                "time_s": t,
                "elevation_deg": elevation,
                "captured": visible
            })

# =====================================================
# 8. CREATE DATAFRAMES AND SAVE CSV FILES
# =====================================================

ground_df = pd.DataFrame(ground_track_data)
capture_df = pd.DataFrame(capture_data)

ground_df.to_csv(
    "ground_tracks_variant7.csv",
    index=False
)

capture_df.to_csv(
    "capture_results_variant7.csv",
    index=False
)

print("\nGround track data saved.")
print("Capture results saved.")

# =====================================================
# 9. PLOT GROUND TRACKS
# =====================================================

plt.figure(figsize=(13, 6))

for satellite_number in range(1, 6):

    data = ground_df[
        ground_df["satellite"] == satellite_number
    ]

    lon = data["longitude"].to_numpy()
    lat = data["latitude"].to_numpy()

    # Break lines at longitude wraparound
    lon_plot = lon.copy()
    jumps = np.where(np.abs(np.diff(lon)) > 180)[0]
    lon_plot[jumps + 1] = np.nan

    plt.plot(
        lon_plot,
        lat,
        label=f"Satellite {satellite_number}"
    )

for name, (lat, lon) in objects.items():

    plt.scatter(lon % 360, lat, marker="x", s=80)
    plt.annotate(name, (lon % 360, lat))

plt.xlim(0, 360)
plt.ylim(-90, 90)
plt.xlabel("Longitude (degrees)")
plt.ylabel("Latitude (degrees)")
plt.title("Variant 7 - Five Spacecraft Ground Tracks")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("ground_tracks_variant7.png", dpi=200)
plt.show()

# =====================================================
# 10. PLOT CAPTURE TIMELINES
# =====================================================

fig, axes = plt.subplots(
    len(objects), 1,
    figsize=(13, 9),
    sharex=True
)

for ax, object_name in zip(axes, objects.keys()):

    data = capture_df[
        capture_df["object"] == object_name
    ]

    for satellite_number in range(1, 6):

        sat_data = data[
            data["satellite"] == satellite_number
        ]

        ax.step(
            sat_data["time_s"] / 60,
            sat_data["captured"],
            where="post",
            label=f"Satellite {satellite_number}"
        )

    ax.set_title(object_name)
    ax.set_ylabel("Captured")
    ax.set_yticks([0, 1])
    ax.grid()

axes[-1].set_xlabel("Time (minutes)")
axes[0].legend(ncol=5)

plt.suptitle("Observation Object Capture Timelines")
plt.tight_layout()
plt.savefig("capture_timelines_variant7.png", dpi=200)
plt.show()

print("\nAll calculations and plots completed.")
