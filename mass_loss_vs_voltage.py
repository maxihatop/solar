#!/usr/bin/python

import numpy as np
import sys
from scipy.integrate import quad

# Command-line argument parsing
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <Sun_voltage_in_volts>")
    print(f"Example: python {sys.argv[0]} 630")
    sys.exit(1)

# --- Physical constants and parameters ---
k_B_eV = 8.617e-5                 # Boltzmann constant in eV/K
T_K = 1_000_000                   # Chromospheric temperature in Kelvin
T_eV = T_K * k_B_eV               # Temperature in eV

# Solar parameters
G = 6.67430e-11                   # Gravitational constant, m^3/kg/s^2
M_sun = 1.989e30                  # Mass of the Sun, kg
R_sun = 6.9634e8                  # Radius of the Sun, m
m_p = 1.6726e-27                  # Mass of proton, kg
e_charge = 1.6022e-19             # Elementary charge, C

# Compute gravitational potential barrier in volts
phi_grav = G * M_sun * m_p / (R_sun * e_charge)  # in volts

# User-specified voltage
added_voltage = float(sys.argv[1])               # External potential, V
phi_eff = phi_grav - added_voltage               # Effective potential barrier

# Baseline solar wind loss rate (tons/sec)
solar_wind_loss = 2.1e6 / 2                      # Approx. average loss

# Maxwell-Boltzmann energy distribution (normalized in energy space)
def maxwell_energy_dist(E, T_eV):
    return np.sqrt(E) * np.exp(-E / T_eV)

# Integrate tail of distribution (particles that escape)
f0, _ = quad(lambda E: maxwell_energy_dist(E, T_eV), phi_grav, np.inf)
f_with_voltage, _ = quad(lambda E: maxwell_energy_dist(E, T_eV), phi_eff, np.inf)

# Compute mass loss rate
mass_loss_rate = solar_wind_loss / f0 * f_with_voltage
ratio = f_with_voltage / f0

# --- Output ---
print(f"Computed solar gravitational potential barrier: {phi_grav:.1f} V")
print(f"Solar mass ejection with V = {added_voltage:.1f} V:")
print(f"  Escaping particle fraction: {f_with_voltage:.3e}")
print(f"  Relative to natural solar wind: {ratio:.3f}x")
print(f"  Estimated mass loss: {mass_loss_rate:.3e} tons/sec")

