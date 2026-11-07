#  Satellite Orbital Motion and Ground-Track Analysis

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Project](https://img.shields.io/badge/Project-Orbital%20Mechanics-lightgrey)

## 1. Project Overview

This project investigates the orbital motion of five spacecraft and analyses their ground tracks and visibility relative to three observation locations.

The project applies mathematical principles of orbital mechanics, numerical methods, coordinate transformations and scientific programming.

The computational model is implemented in Python.

## 2. Assignment Parameters

| Parameter | Symbol | Value |
|---|---|---:|
| Perigee altitude | \(H_p\) | 700 km |
| Apogee altitude | \(H_a\) | 800 km |
| Orbital inclination | \(i\) | 80° |
| Number of spacecraft | \(N\) | 5 |
| Earth radius | \(R_E\) | 6371 km |
| Gravitational parameter | \(\mu\) | 398600.44 km³/s² |

### Initial RAAN Values

| Spacecraft | RAAN |
|---|---:|
| SC-1 | 0° |
| SC-2 | 72° |
| SC-3 | 144° |
| SC-4 | 216° |
| SC-5 | 288° |

### Observation Locations

- Izhevsk
- Baikonur
- Saratov

Their coordinates are stored in `data/observation_objects.csv`.

## 3. Theoretical Background

The project covers:

1. Orbital elements and orbital geometry.
2. Kepler's three laws.
3. Mean, eccentric and true anomalies.
4. Kepler's equation and Newton-Raphson iteration.
5. Perifocal, ECI and ECEF coordinate systems.
6. Coordinate transformations.
7. Ground-track generation.
8. Satellite elevation angle and visibility.
9. Binary observation and capture analysis.

Detailed explanations are available in the `theory/` directory.

## 4. Computational Method

The simulation follows these main stages:

1. Calculate orbital parameters from perigee and apogee altitudes.
2. Calculate orbital period and mean motion.
3. Generate simulation time points.
4. Solve Kepler's equation to determine spacecraft position.
5. Transform orbital coordinates into ECI and ECEF systems.
6. Calculate geographic latitude and longitude.
7. Generate spacecraft ground tracks.
8. Calculate elevation angles relative to observation locations.
9. Determine satellite visibility.
10. Export datasets and visualisations.

The detailed procedure is documented in `docs/methodology.md`.

## 5. Software and Technologies

| Technology | Purpose |
|---|---|
| Python 3 | Main programming language |
| NumPy | Numerical computation |
| Pandas | Data processing and CSV files |
| Matplotlib | Scientific visualisation |
| Git | Version control |
| GitHub | Project hosting |

## 6. Repository Structure

```text
variant-7-satellite-ground-track-analysis/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── theory/
│   ├── 01_orbital_mechanics.md
│   ├── 02_keplers_laws.md
│   ├── 03_coordinate_systems.md
│   ├── 04_ground_tracks.md
│   └── 05_satellite_visibility.md
│
├── src/
│   └── ground_tracks.py
│
├── data/
│   └── observation_objects.csv
│
├── results/
│
└── docs/
    └── methodology.md
```

## 7. Results

The simulation is intended to generate:

- Combined ground tracks for five spacecraft.
- Spacecraft geographical coordinates over time.
- Visibility datasets for the three observation locations.
- Satellite visibility timelines.

Generated datasets and figures will be placed in the `results/` directory.

*Results will be added after the simulation has been executed and validated.*

## 8. Modelling Assumptions

The initial implementation uses:

- A spherical Earth approximation.
- Ideal two-body orbital motion.
- Simplified Earth rotation.
- A 30-second sampling interval.
- An initial visibility elevation threshold of 10°.

The initial true anomaly and argument of perigee must be confirmed against the assignment instructions. Any temporary assumptions will be documented before the final results are presented.

## 9. Limitations and Future Development

Possible improvements include:

- J2 perturbation modelling.
- More precise Earth reference systems.
- Atmospheric drag modelling.
- More accurate ground-station coordinates.
- Communication link-budget calculations.
- Comparison with an independent orbital propagation model.

## 10. Author

**Field:** Rocket Systems and Cosmonautics  
**University:** Samara National Research University  
**Name:** kibipi ndomele buhilya

---

*This project is developed for academic study of spacecraft orbital motion, ground-track analysis and satellite observation opportunities.*
*This repository is managed using Git and Github.*