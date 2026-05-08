#!/usr/bin/env python3
"""
9:1 Unun Performance Calculator

Models the performance of a trifilar autotransformer 9:1 unun on ferrite
toroid cores, including:
  - Magnetizing inductance and reactance vs frequency
  - Approximate insertion loss vs frequency
  - Return loss / SWR at the 50-ohm port with a 450-ohm load

Usage:
    python unun_performance.py

Outputs:
    - unun_magnetizing_inductance.png
    - unun_insertion_loss.png
    - unun_swr.png
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# =============================================================================
# FT-240 Core Geometry
# =============================================================================
OD = 61.0e-3       # m
ID = 35.55e-3       # m
HT = 12.7e-3        # m

le = np.pi * (OD + ID) / 2     # effective path length (m)
Ae = HT * (OD - ID) / 2        # effective cross-section (m^2)
MU_0 = 4 * np.pi * 1e-7        # H/m

CORE_CONST = MU_0 * Ae / le    # H (per turn^2, per unit mu)

# =============================================================================
# Complex Permeability Data (same as choke project)
# =============================================================================

MIX31_DATA = np.array([
    [  0.5, 1700,  150],
    [  1.0, 1500,  300],
    [  2.0, 1100,  550],
    [  3.0,  850,  680],
    [  5.0,  500,  700],
    [  7.0,  320,  620],
    [ 10.0,  200,  510],
    [ 15.0,  115,  380],
    [ 20.0,   72,  295],
    [ 25.0,   50,  235],
    [ 30.0,   38,  192],
    [ 40.0,   24,  135],
    [ 50.0,   17,  100],
])

MIX43_DATA = np.array([
    [  0.5,  750,   60],
    [  1.0,  720,  110],
    [  2.0,  660,  200],
    [  3.0,  600,  280],
    [  5.0,  480,  370],
    [  7.0,  380,  410],
    [ 10.0,  270,  420],
    [ 15.0,  165,  390],
    [ 20.0,  110,  340],
    [ 25.0,   78,  285],
    [ 30.0,   58,  245],
    [ 40.0,   35,  180],
    [ 50.0,   24,  140],
])

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
    """Log-log interpolation of complex permeability."""
    f_data = data[:, 0]
    log_f = np.log10(f_data)
    log_freqs = np.log10(freqs_mhz)

    interp_mu_p = interp1d(log_f, np.log10(data[:, 1]), kind="cubic",
                           fill_value="extrapolate")
    interp_mu_pp = interp1d(log_f, np.log10(data[:, 2]), kind="cubic",
                            fill_value="extrapolate")

    return 10 ** interp_mu_p(log_freqs), 10 ** interp_mu_pp(log_freqs)


def magnetizing_impedance(freqs_mhz, turns, material_data, num_cores=1):
    """
    Calculate the magnetizing impedance of the transformer winding.

    For the 9:1 autotransformer, the magnetizing inductance is that of the
    full winding (all N turns) since the three series-connected windings
    form a single N-turn inductor when the secondary is open.

    Returns: Zm_real, Zm_imag, Zm_mag, Lm (low-freq inductance in H)
    """
    mu_p, mu_pp = interpolate_permeability(material_data, freqs_mhz)
    omega = 2 * np.pi * freqs_mhz * 1e6

    n2 = turns ** 2
    factor = omega * n2 * num_cores * CORE_CONST

    # Magnetizing impedance: Zm = Rm + jXm
    rm = factor * mu_pp       # loss (resistive)
    xm = factor * mu_p        # reactive (inductive)
    zm_mag = np.sqrt(rm**2 + xm**2)

    # Low-frequency inductance (use lowest frequency permeability)
    mu_p_low, _ = interpolate_permeability(material_data,
                                           np.array([material_data[0, 0]]))
    lm = n2 * num_cores * CORE_CONST * mu_p_low[0]

    return rm, xm, zm_mag, lm


def unun_performance(freqs_mhz, turns, material_data, num_cores=1,
                     z_source=50.0, z_load=450.0):
    """
    Model 9:1 unun performance.

    Uses a simplified equivalent circuit: ideal 9:1 transformer with
    magnetizing impedance Zm in parallel with the load (referred to
    the primary side).

    Returns:
        insertion_loss_db: power loss through the transformer
        return_loss_db: return loss at the 50-ohm port
        swr: SWR at the 50-ohm port
    """
    rm, xm, _, _ = magnetizing_impedance(freqs_mhz, turns, material_data,
                                          num_cores)
    omega = 2 * np.pi * freqs_mhz * 1e6

    # Magnetizing impedance (complex)
    zm = rm + 1j * xm

    # Load impedance referred to primary (50-ohm) side
    # For 9:1 unun: Z_load_referred = Z_load / 9
    z_load_ref = z_load / 9.0  # = 50 ohms ideally

    # Total impedance seen at primary: Zm in parallel with Z_load_referred
    # (magnetizing impedance shunts current away from the ideal transformer)
    z_total = (zm * z_load_ref) / (zm + z_load_ref)

    # Reflection coefficient at primary port
    gamma = (z_total - z_source) / (z_total + z_source)
    return_loss_db = -20 * np.log10(np.abs(gamma) + 1e-12)
    swr = (1 + np.abs(gamma)) / (1 - np.abs(gamma) + 1e-12)

    # Insertion loss: power delivered to load vs available power
    # Power available from source: Pav = |Vs|^2 / (8 * Rs)
    # Power to load: P_load = |I|^2 * Re(Z_load_ref)
    #   where I = Vs / (Zs + Z_total)
    # But Z_load_ref is purely real (450/9=50), and Zm shunts some current.
    #
    # Fraction of input power lost in the magnetizing impedance:
    # The current splits between Zm and Z_load_ref.
    # I_load = I_total * Zm / (Zm + Z_load_ref)
    # P_load / P_input = |Zm / (Zm + Z_load_ref)|^2 * Re(Z_load_ref) / Re(Z_total)

    # More directly: insertion loss = mismatch loss + dissipative loss
    # Dissipative loss from Zm:
    i_total = 1.0 / (z_source + z_total)  # normalized to 1V source
    v_across = i_total * z_total
    i_load = v_across / z_load_ref
    i_mag = v_across / zm

    p_load = 0.5 * np.abs(i_load)**2 * np.real(z_load_ref)
    p_available = 0.5 * 1.0**2 / (4 * z_source)  # max available from source

    # Transducer power gain
    tpg = p_load / p_available
    insertion_loss_db = -10 * np.log10(tpg + 1e-12)

    return insertion_loss_db, return_loss_db, swr


def print_performance_table(freqs_mhz, turns, material_data, num_cores, label):
    """Print performance at ham band frequencies."""
    il, rl, swr = unun_performance(freqs_mhz, turns, material_data, num_cores)
    rm, xm, zm_mag, lm = magnetizing_impedance(freqs_mhz, turns, material_data,
                                                 num_cores)

    print(f"\n{'='*72}")
    print(f"  {label}")
    print(f"  Lm (low-freq) = {lm*1e6:.1f} μH")
    print(f"{'='*72}")
    print(f"  {'Band':<6} {'Freq':>6} {'|Zm|':>8} {'IL':>8} {'RL':>8} {'SWR':>6}")
    print(f"  {'':─<6} {'(MHz)':─>6} {'(Ω)':─>8} {'(dB)':─>8} {'(dB)':─>8} {'':─>6}")

    for name, f in HAM_BANDS.items():
        idx = np.argmin(np.abs(freqs_mhz - f))
        print(f"  {name:<6} {f:>6.1f} {zm_mag[idx]:>8.0f} "
              f"{il[idx]:>8.2f} {rl[idx]:>8.1f} {swr[idx]:>6.2f}")


def main():
    freqs = np.logspace(np.log10(1), np.log10(55), 500)

    designs = [
        ("A: FT-240-43 / 12T trifilar",  12, MIX43_DATA, 1),
        ("B: FT-240-31 / 10T trifilar",  10, MIX31_DATA, 1),
        ("C: 2x FT-240-43 / 10T trifilar", 10, MIX43_DATA, 2),
    ]

    print("9:1 Unun Performance Calculator")
    print(f"Core: FT-240 (OD={OD*1e3:.1f}mm, ID={ID*1e3:.2f}mm, H={HT*1e3:.1f}mm)")
    print(f"Core constant: {CORE_CONST:.4e} H")
    print(f"Load: 450 Ω → 50 Ω (9:1 ratio)")

    # Print tables
    for label, turns, data, cores in designs:
        print_performance_table(freqs, turns, data, cores, label)

    # =========================================================================
    # Plot 1: Magnetizing Reactance vs Frequency
    # =========================================================================
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    colors = ["#2196F3", "#4CAF50", "#FF9800"]

    for (label, turns, data, cores), color in zip(designs, colors):
        _, xm, _, lm = magnetizing_impedance(freqs, turns, data, cores)
        ax1.semilogx(freqs, xm, color=color, linewidth=2.5,
                     label=f"{label} (Lm={lm*1e6:.0f}μH)")

    # Mark the 4x load impedance threshold
    ax1.axhline(y=4*450, color="red", linestyle="--", alpha=0.5, linewidth=1)
    ax1.text(1.1, 4*450 + 100, "4 × 450 Ω = 1800 Ω (design minimum)",
             color="red", fontsize=9, alpha=0.7)

    ax1.axhline(y=450, color="gray", linestyle=":", alpha=0.5, linewidth=1)
    ax1.text(1.1, 500, "Z_load = 450 Ω", color="gray", fontsize=9, alpha=0.7)

    for name, f in HAM_BANDS.items():
        ax1.axvline(x=f, color="gray", alpha=0.12, linewidth=1)
        ax1.text(f, 200, name, ha="center", fontsize=7, color="gray", alpha=0.7)

    ax1.set_xlabel("Frequency (MHz)", fontsize=12)
    ax1.set_ylabel("Magnetizing Reactance Xm (Ω)", fontsize=12)
    ax1.set_title("9:1 Unun — Magnetizing Reactance vs Frequency", fontsize=14)
    ax1.legend(fontsize=10)
    ax1.set_xlim(1, 50)
    ax1.set_ylim(0, None)
    ax1.grid(True, which="both", alpha=0.3)
    fig1.tight_layout()
    fig1.savefig("unun_magnetizing_reactance.png", dpi=150)
    print(f"\nSaved: unun_magnetizing_reactance.png")

    # =========================================================================
    # Plot 2: Insertion Loss
    # =========================================================================
    fig2, ax2 = plt.subplots(figsize=(12, 7))

    for (label, turns, data, cores), color in zip(designs, colors):
        il, _, _ = unun_performance(freqs, turns, data, cores)
        ax2.semilogx(freqs, il, color=color, linewidth=2.5, label=label)

    ax2.axhline(y=0.5, color="red", linestyle="--", alpha=0.5, linewidth=1)
    ax2.text(30, 0.55, "0.5 dB target max", color="red", fontsize=9, alpha=0.7)

    for name, f in HAM_BANDS.items():
        ax2.axvline(x=f, color="gray", alpha=0.12, linewidth=1)

    ax2.set_xlabel("Frequency (MHz)", fontsize=12)
    ax2.set_ylabel("Insertion Loss (dB)", fontsize=12)
    ax2.set_title("9:1 Unun — Insertion Loss (lower is better)", fontsize=14)
    ax2.legend(fontsize=10)
    ax2.set_xlim(1, 50)
    ax2.set_ylim(0, 3)
    ax2.invert_yaxis()
    ax2.grid(True, which="both", alpha=0.3)
    fig2.tight_layout()
    fig2.savefig("unun_insertion_loss.png", dpi=150)
    print(f"Saved: unun_insertion_loss.png")

    # =========================================================================
    # Plot 3: SWR at 50-ohm port (with 450-ohm load)
    # =========================================================================
    fig3, ax3 = plt.subplots(figsize=(12, 7))

    for (label, turns, data, cores), color in zip(designs, colors):
        _, _, swr = unun_performance(freqs, turns, data, cores)
        ax3.semilogx(freqs, swr, color=color, linewidth=2.5, label=label)

    ax3.axhline(y=1.5, color="orange", linestyle="--", alpha=0.5, linewidth=1)
    ax3.text(30, 1.55, "1.5:1 SWR", color="orange", fontsize=9, alpha=0.7)

    ax3.axhline(y=2.0, color="red", linestyle="--", alpha=0.5, linewidth=1)
    ax3.text(30, 2.05, "2.0:1 SWR", color="red", fontsize=9, alpha=0.7)

    for name, f in HAM_BANDS.items():
        ax3.axvline(x=f, color="gray", alpha=0.12, linewidth=1)

    ax3.set_xlabel("Frequency (MHz)", fontsize=12)
    ax3.set_ylabel("SWR at 50 Ω port", fontsize=12)
    ax3.set_title("9:1 Unun — SWR with 450 Ω Load (ideal = 1.0)", fontsize=14)
    ax3.legend(fontsize=10)
    ax3.set_xlim(1, 50)
    ax3.set_ylim(1, 4)
    ax3.grid(True, which="both", alpha=0.3)
    fig3.tight_layout()
    fig3.savefig("unun_swr.png", dpi=150)
    print(f"Saved: unun_swr.png")

    plt.show()


if __name__ == "__main__":
    main()
