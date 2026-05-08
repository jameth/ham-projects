#!/usr/bin/env python3
"""
Common Mode Choke Impedance Calculator

Calculates and plots the choking impedance of toroidal common-mode chokes
using Fair-Rite mix 31 and mix 43 complex permeability data.

Usage:
    python choke_impedance.py

Outputs:
    - choke_impedance_comparison.png  (all designs on one plot)
    - choke_impedance_detail.png      (Rs vs Xs breakdown for recommended design)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# =============================================================================
# FT-240 Core Geometry
# =============================================================================
OD = 61.0e-3       # outer diameter (m)
ID = 35.55e-3       # inner diameter (m)
HT = 12.7e-3        # height (m)

# Effective magnetic path length and cross-sectional area (toroid approximations)
le = np.pi * (OD + ID) / 2                  # effective path length (m)
Ae = HT * (OD - ID) / 2                     # effective cross-section area (m^2)

MU_0 = 4 * np.pi * 1e-7                     # permeability of free space (H/m)

# Core constant: C = mu_0 * Ae / le  (H)
# Impedance of N turns: Z = j * 2*pi*f * N^2 * (mu' - j*mu'') * C
CORE_CONST = MU_0 * Ae / le

# =============================================================================
# Complex Permeability Data (approximate, from Fair-Rite published curves)
#
# Format: (frequency_MHz, mu_prime, mu_double_prime)
# mu' = real part (reactive/inductive)
# mu'' = imaginary part (loss/resistive)
# =============================================================================

# Mix 31: Optimized for 1-30 MHz HF applications
MIX31_DATA = np.array([
    #  f(MHz)   mu'    mu''
    [  0.5,    1700,    150],
    [  1.0,    1500,    300],
    [  2.0,    1100,    550],
    [  3.0,     850,    680],
    [  5.0,     500,    700],
    [  7.0,     320,    620],
    [ 10.0,     200,    510],
    [ 15.0,     115,    380],
    [ 20.0,      72,    295],
    [ 25.0,      50,    235],
    [ 30.0,      38,    192],
    [ 40.0,      24,    135],
    [ 50.0,      17,    100],
    [ 70.0,      10,     62],
    [100.0,       6,     38],
])

# Mix 43: Optimized for 20-250 MHz, higher frequency applications
MIX43_DATA = np.array([
    #  f(MHz)   mu'    mu''
    [  0.5,     750,     60],
    [  1.0,     720,    110],
    [  2.0,     660,    200],
    [  3.0,     600,    280],
    [  5.0,     480,    370],
    [  7.0,     380,    410],
    [ 10.0,     270,    420],
    [ 15.0,     165,    390],
    [ 20.0,     110,    340],
    [ 25.0,      78,    285],
    [ 30.0,      58,    245],
    [ 40.0,      35,    180],
    [ 50.0,      24,    140],
    [ 70.0,      13,     90],
    [100.0,       7,     55],
    [150.0,       4,     32],
    [200.0,       3,     22],
])

# =============================================================================
# Ham Band Frequencies for Annotation
# =============================================================================
HAM_BANDS = {
    "160m": 1.8,
    "80m":  3.5,
    "40m":  7.0,
    "30m": 10.1,
    "20m": 14.0,
    "17m": 18.1,
    "15m": 21.0,
    "12m": 24.9,
    "10m": 28.0,
}


def interpolate_permeability(data, freqs_mhz):
    """Interpolate complex permeability to arbitrary frequencies (log-log)."""
    f_data = data[:, 0]
    mu_p = data[:, 1]
    mu_pp = data[:, 2]

    # Log-log interpolation for smoother curves
    log_f = np.log10(f_data)
    log_freqs = np.log10(freqs_mhz)

    interp_mu_p = interp1d(log_f, np.log10(mu_p), kind="cubic",
                           fill_value="extrapolate")
    interp_mu_pp = interp1d(log_f, np.log10(mu_pp), kind="cubic",
                            fill_value="extrapolate")

    mu_prime = 10 ** interp_mu_p(log_freqs)
    mu_dprime = 10 ** interp_mu_pp(log_freqs)
    return mu_prime, mu_dprime


def choke_impedance(freqs_mhz, turns, material_data, num_cores=1):
    """
    Calculate common-mode choke impedance.

    Returns:
        rs:    resistive component (ohms) — dissipates CM energy
        xs:    reactive component (ohms) — reflects CM energy
        z_mag: impedance magnitude (ohms)
    """
    mu_prime, mu_dprime = interpolate_permeability(material_data, freqs_mhz)
    omega = 2 * np.pi * freqs_mhz * 1e6

    # Z = j * omega * N^2 * num_cores * (mu' - j*mu'') * core_const
    # Expanding: Z = omega * N^2 * C * (mu'' + j*mu')  [resistive + reactive]
    n2 = turns ** 2
    factor = omega * n2 * num_cores * CORE_CONST

    rs = factor * mu_dprime       # resistive (from mu'', the loss factor)
    xs = factor * mu_prime        # reactive (from mu', the permeability)
    z_mag = np.sqrt(rs**2 + xs**2)

    return rs, xs, z_mag


def print_band_table(freqs_mhz, rs, xs, z_mag, label):
    """Print impedance at ham band frequencies."""
    print(f"\n{'='*65}")
    print(f"  {label}")
    print(f"{'='*65}")
    print(f"  {'Band':<6} {'Freq':>6} {'|Z|':>8} {'Rs':>8} {'Xs':>8}  {'Character'}")
    print(f"  {'':─<6} {'(MHz)':─>6} {'(Ω)':─>8} {'(Ω)':─>8} {'(Ω)':─>8}  {'':─<12}")

    for name, f in HAM_BANDS.items():
        idx = np.argmin(np.abs(freqs_mhz - f))
        r, x, z = rs[idx], xs[idx], z_mag[idx]
        if r > 2 * x:
            char = "Resistive"
        elif r > 0.5 * x:
            char = "Mixed"
        else:
            char = "Reactive"
        print(f"  {name:<6} {f:>6.1f} {z:>8.0f} {r:>8.0f} {x:>8.0f}  {char}")


def plot_comparison(freqs):
    """Plot impedance magnitude comparison of all designs."""
    designs = [
        ("A: RG316 / 1x FT-240-31 / 12T",     12, MIX31_DATA, 1),
        ("B: Bifilar / 1x FT-240-31 / 18T",    18, MIX31_DATA, 1),
        ("C: RG316 / 2x FT-240-31 / 12T",      12, MIX31_DATA, 2),
        ("D: RG316 / 1x FT-240-43 / 12T",      12, MIX43_DATA, 1),
    ]

    fig, ax = plt.subplots(figsize=(12, 7))

    colors = ["#2196F3", "#4CAF50", "#FF9800", "#F44336"]
    styles = ["-", "--", "-.", ":"]

    for (label, turns, data, cores), color, style in zip(designs, colors, styles):
        rs, xs, z_mag = choke_impedance(freqs, turns, data, cores)
        ax.semilogx(freqs, z_mag, style, color=color, linewidth=2.5, label=label)

        # Print table
        print_band_table(freqs, rs, xs, z_mag, label)

    # 1000-ohm threshold line
    ax.axhline(y=1000, color="gray", linestyle="--", alpha=0.5, linewidth=1)
    ax.text(0.55, 1050, "1000 Ω target minimum", color="gray", fontsize=9)

    # Mark ham bands
    for name, f in HAM_BANDS.items():
        ax.axvline(x=f, color="gray", alpha=0.15, linewidth=1)
        ax.text(f, ax.get_ylim()[1] * 0.02, name, ha="center", fontsize=7,
                color="gray", alpha=0.7)

    ax.set_xlabel("Frequency (MHz)", fontsize=12)
    ax.set_ylabel("Choking Impedance |Z| (Ω)", fontsize=12)
    ax.set_title("Common Mode Choke — Impedance Comparison", fontsize=14)
    ax.legend(fontsize=10, loc="upper right")
    ax.set_xlim(1, 50)
    ax.set_ylim(0, None)
    ax.grid(True, which="both", alpha=0.3)
    ax.tick_params(labelsize=10)

    fig.tight_layout()
    fig.savefig("choke_impedance_comparison.png", dpi=150)
    print(f"\nSaved: choke_impedance_comparison.png")
    return fig


def plot_detail(freqs):
    """Plot Rs vs Xs breakdown for Design A (recommended build)."""
    rs, xs, z_mag = choke_impedance(freqs, 12, MIX31_DATA, 1)

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.semilogx(freqs, z_mag, "-", color="#2196F3", linewidth=2.5, label="|Z| total")
    ax.semilogx(freqs, rs, "-", color="#F44336", linewidth=2, label="Rs (resistive)")
    ax.semilogx(freqs, xs, "-", color="#4CAF50", linewidth=2, label="Xs (reactive)")

    # Fill to show which component dominates
    ax.fill_between(freqs, rs, xs, where=(rs > xs), alpha=0.1, color="#F44336",
                    label="Rs dominant (good)")
    ax.fill_between(freqs, rs, xs, where=(rs <= xs), alpha=0.1, color="#4CAF50",
                    label="Xs dominant")

    # 1000-ohm threshold
    ax.axhline(y=1000, color="gray", linestyle="--", alpha=0.5, linewidth=1)

    # Mark ham bands
    for name, f in HAM_BANDS.items():
        ax.axvline(x=f, color="gray", alpha=0.15, linewidth=1)
        ax.text(f, ax.get_ylim()[1] * 0.02 if ax.get_ylim()[1] > 0 else 50,
                name, ha="center", fontsize=7, color="gray", alpha=0.7)

    ax.set_xlabel("Frequency (MHz)", fontsize=12)
    ax.set_ylabel("Impedance (Ω)", fontsize=12)
    ax.set_title("Design A: RG316 / 1x FT-240-31 / 12 Turns — Impedance Breakdown",
                 fontsize=14)
    ax.legend(fontsize=10, loc="upper right")
    ax.set_xlim(1, 50)
    ax.set_ylim(0, None)
    ax.grid(True, which="both", alpha=0.3)
    ax.tick_params(labelsize=10)

    fig.tight_layout()
    fig.savefig("choke_impedance_detail.png", dpi=150)
    print(f"Saved: choke_impedance_detail.png")
    return fig


def main():
    freqs = np.logspace(np.log10(1), np.log10(55), 500)  # 1-55 MHz, 500 points

    print("Common Mode Choke Impedance Calculator")
    print("Core: FT-240 (OD=61mm, ID=35.55mm, H=12.7mm)")
    print(f"Core constant (μ₀·Ae/le): {CORE_CONST:.4e} H")

    plot_comparison(freqs)
    plot_detail(freqs)

    plt.show()


if __name__ == "__main__":
    main()
