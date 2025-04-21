#!/usr/bin/env python3
# Estimate whether the Sun can avoid helium flash via mass offloading
# Input: mass loss rate in gigatonnes per second

import numpy as np
import matplotlib.pyplot as plt
import sys

# --- Parse command-line argument ---
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <mass_loss_in_gigatonnes_per_second>")
    print(f"Example: python {sys.argv[0]} 1.3")
    sys.exit(1)

mass_loss_gtps = float(sys.argv[1])  # User input: mass loss rate in Gt/s

# --- Physical constants and time setup ---
M_sun_initial = 1.989e30                # Initial solar mass in kg
seconds_per_year = 3.154e7              # Seconds in a Julian year

timestep = 1e5 * seconds_per_year       # Time step: 100,000 years
total_sim_time = 15e9 * seconds_per_year  # Simulate for up to 15 billion years

sun_total_lifetime = 8e9 * seconds_per_year  # Hypothetical total lifetime if lighter
sun_remaining_life = 4e9 * seconds_per_year  # Remaining life of the current Sun

# --- Prepare storage for plotting ---
elapsed_times = []
remaining_lifetimes = []

t = 0
while t < total_sim_time:
    mass_loss_kg = mass_loss_gtps * 1e12 * t  # Convert Gt/s to kg
    M_current = M_sun_initial - mass_loss_kg

    if M_current <= 0:
        break  # Sun completely evaporated

    # Lifetime as function of mass ~ M^-2.5
    t_life = sun_total_lifetime * (M_current / M_sun_initial) ** -2.5

    remaining_life = t_life - sun_remaining_life
    if remaining_life <= 0:
        break  # Star would flash before this point

    # Convert to Gyr for plotting
    elapsed_times.append(t / seconds_per_year / 1e9)
    remaining_lifetimes.append(remaining_life / seconds_per_year / 1e9)

    t += timestep

# --- Plot results ---
plt.figure(figsize=(10, 6))
plt.plot(elapsed_times, remaining_lifetimes, label='Remaining Lifetime of the Sun', color='orange')
plt.plot(elapsed_times, elapsed_times, '--', label='Elapsed Time', color='blue')

plt.xlabel('Elapsed Time (billion years)')
plt.ylabel('Remaining Time Before Flash (billion years)')
plt.title(f'Can the Sun Outlive the Flash at {mass_loss_gtps:.2f} Gt/s Mass Loss?')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


