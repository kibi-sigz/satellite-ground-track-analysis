# Computational Methodology

## 1. Introduction

This document describes the computational procedure used to analyse the orbital motion, ground tracks and visibility of five spacecraft in Variant 7.

The simulation uses Python to perform numerical calculations, transform coordinate systems, evaluate satellite visibility and generate graphical representations of the results.

## 2. Input Parameters

The simulation uses the following orbital parameters:

| Parameter | Symbol | Value |
|---|---|---:|
| Earth mean radius | \(R_E\) | 6371 km |
| Gravitational parameter | \(\mu\) | 398600.44 km³/s² |
| Perigee altitude | \(H_p\) | 700 km |
| Apogee altitude | \(H_a\) | 800 km |
| Inclination | \(i\) | 80° |
| Number of spacecraft | \(N\) | 5 |
| Earth rotation rate | \(\omega_E\) | 7.2921159 × 10⁻⁵ rad/s |
| Sampling interval | \(\Delta t\) | 30 s |

The initial RAAN values are:

\[
\Omega=[0^\circ,72^\circ,144^\circ,216^\circ,288^\circ]
\]

The argument of perigee and initial true anomaly must be confirmed against the assignment instructions or explicitly declared as assumptions.

## 3. Orbital Parameter Calculation

The perigee and apogee radii are calculated as:

\[
r_p=R_E+H_p
\]

\[
r_a=R_E+H_a
\]

The semi-major axis is:

\[
a=\frac{r_p+r_a}{2}
\]

The eccentricity is:

\[
e=\frac{r_a-r_p}{r_a+r_p}
\]

The semi-latus rectum is:

\[
p=a(1-e^2)
\]

These values describe the size and shape of the spacecraft orbit.

## 4. Orbital Period and Mean Motion

The orbital period is calculated using:

\[
T=2\pi\sqrt{\frac{a^3}{\mu}}
\]

Mean motion is:

\[
n=\frac{2\pi}{T}
\]

The resulting orbital period is approximately 99.67 minutes.

## 5. Time Discretisation

The simulation evaluates spacecraft positions at discrete time intervals.

The time vector is defined by:

\[
t_k=k\Delta t
\]

Where \(k\) is the sample index and \(\Delta t\) is the sampling interval.

The initial simulation covers approximately two orbital periods.

## 6. Solving Kepler's Equation

For each spacecraft, mean anomaly is calculated:

\[
M=M_0+nt
\]

Eccentric anomaly is obtained by solving:

\[
M=E-e\sin E
\]

The Newton-Raphson method is used:

\[
E_{k+1}=E_k-
\frac{E_k-e\sin E_k-M}
{1-e\cos E_k}
\]

The true anomaly is then calculated from eccentric anomaly.

## 7. Orbital Position Calculation

The orbital radius is calculated as:

\[
r=\frac{p}{1+e\cos\theta}
\]

The argument of latitude is:

\[
u=\omega+\theta
\]

The spacecraft position is initially represented in the orbital plane and subsequently transformed into ECI coordinates.

## 8. Coordinate Transformation

The orbital position is transformed into ECI coordinates using the orbital orientation parameters:

\[
\mathbf r_{ECI}
=
R_3(\Omega)R_1(i)R_3(\omega)\mathbf r_{PQW}
\]

Earth rotation is then applied to obtain ECEF coordinates:

\[
\mathbf r_{ECEF}=R_3(-\omega_E t)\mathbf r_{ECI}
\]

This expression assumes the initial ECI and ECEF axes are aligned.

The resulting ECEF coordinates are converted into geographic latitude and longitude using a spherical Earth approximation.

## 9. Ground-Track Generation

For each spacecraft, the program stores:

- Spacecraft identifier.
- Time.
- Latitude.
- Longitude.
- Orbital altitude.

The resulting dataset is used to generate a combined ground-track visualisation for all five spacecraft.

Longitude discontinuities are handled during plotting to prevent artificial lines across the map.

## 10. Satellite Visibility Calculation

Each observation location is converted into ECEF coordinates.

The line-of-sight vector is:

\[
\boldsymbol{\rho}=\mathbf r_s-\mathbf r_g
\]

The slant range is:

\[
\rho=|\boldsymbol{\rho}|
\]

The local vertical unit vector is calculated from the observer's latitude and longitude.

The elevation angle is:

\[
\varepsilon=
\arcsin
\left(
\frac{\boldsymbol{\rho}\cdot\hat{\mathbf u}}{\rho}
\right)
\]

A binary visibility condition is applied:

\[
V(t)=
\begin{cases}
1,&\varepsilon\geq10^\circ\\
0,&\varepsilon<10^\circ
\end{cases}
\]

The 10-degree threshold is an initial modelling assumption and must be checked against the assignment requirements.

## 11. Data Storage

The simulation produces two main datasets.

### Ground-track dataset

Contains the calculated geographical positions of all spacecraft over time.

### Visibility dataset

Contains the visibility status of every spacecraft relative to each observation location.

The datasets are stored in CSV format to support further analysis and independent verification.

## 12. Graphical Visualisation

Matplotlib is used to generate:

1. A combined ground-track plot.
2. Satellite visibility timelines for the three observation locations.

These figures provide a visual representation of spacecraft trajectories and observation opportunities.

## 13. Software Environment

The computational implementation uses:

- Python 3.
- NumPy for numerical calculations.
- Pandas for structured datasets.
- Matplotlib for graphical visualisation.

## 14. Limitations and Future Improvements

The initial model uses a spherical Earth, simplified Earth rotation and ideal two-body orbital motion.

Future improvements may include:

- J2 perturbation modelling.
- Atmospheric drag.
- Ellipsoidal Earth coordinates.
- More accurate Earth orientation.
- Ground-station elevation constraints based on terrain.
- Communication link-budget analysis.
- Numerical validation against an independent orbital propagator.

## 15. Conclusion

The computational methodology connects the mathematical foundations of orbital mechanics with a reproducible Python simulation.

It provides a systematic approach to calculating spacecraft positions, generating ground tracks and evaluating geometric visibility from selected observation locations.