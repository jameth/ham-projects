#!/usr/bin/env python3
"""
49:1 Unun (EFHW Transformer) Performance Calculator

Models the performance of a tapped autotransformer 49:1 unun for end-fed
half-wave antennas, including:
  - Magnetizing inductance and reactance vs frequency
  - Approximate insertion loss vs frequency
  - SWR at the 50-ohm port with a 2450-ohm load
  - Effect of compensation capacitor

Usage:
    python unun49_performance.py

Outputs:
    - unun49_magnetizing_reactance.png
    - unun49_insertion_loss.png
    - unun49_swr_with_cap.png
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# =============================================================================
# FT-240 Core Geometry
# =============================================================================
OD = 61.0e-3
ID = 35.55e-3
HT = 12.7e-3

le = np.pi * (OD + ID) / 2
Ae = HT * (OD - ID) / 2
MU_0 = 4 * np.pi * 1e-7
CORE_CONST = MU_0 * Ae / le

# =============================================================================
# Complex Permeability Data
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
    Calculate magnetizing impedance of the full winding.

    For the 49:1 tapped autotransformer, the magnetizing inductance is that
    of the FULL winding (all N turns), since that's what the core sees.
    """
    mu_p, mu_pp = interpolate_permeability(material_data, freqs_mhz)
    omega = 2 * np.pi * freqs_mhz * 1e6

    n2 = turns ** 2
    factor = omega * n2 * num_cores * CORE_CONST

    rm = factor * mu_pp
    xm = factor * mu_p
    zm_mag = np.sqrt(rm**2 + xm**2)

    # Low-frequency inductance
    mu_p_low, _ = interpolate_permeability(material_data,
                                           np.array([material_data[0, 0]]))
    lm = n2 * num_cores * CORE_CONST * mu_p_low[0]

    return rm, xm, zm_mag, lm


def unun49_performance(freqs_mhz, total_turns, tap_turns, material_data,
                       num_cores=1, z_source=50.0, z_load=2450.0,
                       c_comp_pf=0.0, coupling_k=0.95):
    """
    Model 49:1 unun performance with leakage inductance and optional
    compensation capacitor.

    Equivalent circuit (referred to primary side):
        Zs ──── Zl_leak ──┬──── Z_load_ref
                          │
                     Zm (mag)  ||  Z_cap
                          │
                        GND

    Where:
    - Zl_leak = leakage inductance from imperfect coupling (series)
    - Zm = magnetizing impedance (shunt, from core)
    - Z_cap = compensation capacitor (shunt, cancels leakage at design freq)
    - Z_load_ref = Z_load / ratio (referred to primary)

    The compensation cap resonates with the leakage inductance to improve
    SWR on the upper harmonic bands.
    """
    ratio = (total_turns / tap_turns) ** 2
    rm, xm, _, lm = magnetizing_impedance(freqs_mhz, total_turns,
                                           material_data, num_cores)
    omega = 2 * np.pi * freqs_mhz * 1e6

    # Magnetizing impedance (complex, referred to full winding)
    zm = rm + 1j * xm

    # Leakage inductance (referred to primary side)
    # For coupling coefficient k, the leakage fraction is (1 - k^2)
    # Referred to primary: L_leak = (1 - k^2) * Lm * (tap/total)^2
    lm_primary = lm / ratio
    l_leak = (1 - coupling_k**2) * lm_primary
    z_leak = 1j * omega * l_leak

    # Load impedance referred to primary side
    z_load_ref = z_load / ratio

    # Shunt elements: Zm (referred to primary) and compensation cap
    zm_primary = zm / ratio  # refer magnetizing impedance to primary side

    if c_comp_pf > 0:
        c_comp = c_comp_pf * 1e-12
        z_cap = 1.0 / (1j * omega * c_comp)
        # Zm_primary || Z_cap
        z_shunt = (zm_primary * z_cap) / (zm_primary + z_cap)
    else:
        z_shunt = zm_primary

    # Total: Z_leak in series with (Z_shunt || Z_load_ref)
    z_parallel = (z_shunt * z_load_ref) / (z_shunt + z_load_ref)
    z_total = z_leak + z_parallel

    # Reflection coefficient
    gamma = (z_total - z_source) / (z_total + z_source)
    return_loss_db = -20 * np.log10(np.abs(gamma) + 1e-12)
    swr = (1 + np.abs(gamma)) / (1 - np.abs(gamma) + 1e-12)
    swr = np.clip(swr, 1.0, 100.0)

    # Insertion loss (transducer power gain)
    # Power delivered to load vs power available from source
    i_total = 1.0 / (z_source + z_total)
    v_parallel = i_total * z_parallel
    i_load = v_parallel / z_load_ref
    p_load = 0.5 * np.abs(i_load)**2 * np.real(z_load_ref)
    p_available = 0.5 / (4 * z_source)
    tpg = p_load / p_available
    insertion_loss_db = -10 * np.log10(tpg + 1e-12)

    return insertion_loss_db, return_loss_db, swr


def print_performance_table(freqs, total_turns, tap_turns, material_data,
                            num_cores, c_comp_pf, label):
    """Print performance at ham band frequencies."""
    il, rl, swr = unun49_performance(freqs, total_turns, tap_turns,
                                      material_data, num_cores,
                                      c_comp_pf=c_comp_pf)
    _, _, zm_mag, lm = magnetizing_impedance(freqs, total_turns,
                                              material_data, num_cores)
    ratio = (total_turns / tap_turns) ** 2

    print(f"\n{'='*75}")
    print(f"  {label}")
    print(f"  Ratio: ({total_turns}/{tap_turns})² = {ratio:.0f}:1")
    print(f"  Lm (full winding) = {lm*1e6:.1f} μH")
    print(f"  Compensation cap: {c_comp_pf:.0f} pF" if c_comp_pf > 0 else
          f"  Compensation cap: none")
    print(f"{'='*75}")
    print(f"  {'Band':<6} {'Freq':>6} {'|Zm|':>8} {'IL':>8} {'RL':>8} {'SWR':>6}")
    print(f"  {'':─<6} {'(MHz)':─>6} {'(Ω)':─>8} {'(dB)':─>8} {'(dB)':─>8} {'':─>6}")

    for name, f in HAM_BANDS.items():
        idx = np.argmin(np.abs(freqs - f))
        print(f"  {name:<6} {f:>6.1f} {zm_mag[idx]:>8.0f} "
              f"{il[idx]:>8.2f} {rl[idx]:>8.1f} {swr[idx]:>6.2f}")


def main():
    freqs = np.logspace(np.log10(1), np.log10(55), 500)

    designs = [
        ("A: FT-240-43 / 14T tap@2T",           14, 2, MIX43_DATA, 1),
        ("B: FT-240-31 / 14T tap@2T",           14, 2, MIX31_DATA, 1),
        ("C: 2x FT-240-43 / 14T tap@2T",        14, 2, MIX43_DATA, 2),
        ("D: FT-240-43 / 21T tap@3T",           21, 3, MIX43_DATA, 1),
    ]

    print("49:1 Unun (EFHW Transformer) Performance Calculator")
    print(f"Core: FT-240 (OD={OD*1e3:.1f}mm, ID={ID*1e3:.2f}mm, H={HT*1e3:.1f}mm)")
    print(f"Core constant: {CORE_CONST:.4e} H")
    print(f"Load: 2450 Ω → 50 Ω (49:1 ratio)")

    # Print tables without compensation cap
    for label, tt, tap, data, cores in designs:
        print_performance_table(freqs, tt, tap, data, cores, 0, label)

    # Print table with compensation cap for Design A
    print_performance_table(freqs, 14, 2, MIX43_DATA, 1, 100,
                            "A + 100 pF compensation cap")
    print_performance_table(freqs, 14, 2, MIX43_DATA, 1, 150,
                            "A + 150 pF compensation cap")

    # =========================================================================
    # Plot 1: Magnetizing Reactance
    # =========================================================================
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"]

    for (label, tt, tap, data, cores), color in zip(designs, colors):
        _, xm, _, lm = magnetizing_impedance(freqs, tt, data, cores)
        ax1.semilogx(freqs, xm, color=color, linewidth=2.5,
                     label=f"{label} (Lm={lm*1e6:.0f}μH)")

    # Threshold lines
    ax1.axhline(y=4*2450, color="red", linestyle="--", alpha=0.5, linewidth=1)
    ax1.text(1.1, 4*2450 + 300, "4 × 2450 Ω = 9800 Ω (design target)",
             color="red", fontsize=9, alpha=0.7)

    ax1.axhline(y=2450, color="gray", linestyle=":", alpha=0.5, linewidth=1)
    ax1.text(1.1, 2600, "Z_load = 2450 Ω", color="gray", fontsize=9, alpha=0.7)

    for name, f in HAM_BANDS.items():
        ax1.axvline(x=f, color="gray", alpha=0.12, linewidth=1)
        ax1.text(f, 500, name, ha="center", fontsize=7, color="gray", alpha=0.7)

    ax1.set_xlabel("Frequency (MHz)", fontsize=12)
    ax1.set_ylabel("Magnetizing Reactance Xm (Ω)", fontsize=12)
    ax1.set_title("49:1 Unun — Magnetizing Reactance vs Frequency", fontsize=14)
    ax1.legend(fontsize=10)
    ax1.set_xlim(1, 50)
    ax1.set_ylim(0, None)
    ax1.grid(True, which="both", alpha=0.3)
    fig1.tight_layout()
    fig1.savefig("unun49_magnetizing_reactance.png", dpi=150)
    print(f"\nSaved: unun49_magnetizing_reactance.png")

    # =========================================================================
    # Plot 2: Insertion Loss Comparison (no comp cap)
    # =========================================================================
    fig2, ax2 = plt.subplots(figsize=(12, 7))

    for (label, tt, tap, data, cores), color in zip(designs, colors):
        il, _, _ = unun49_performance(freqs, tt, tap, data, cores)
        ax2.semilogx(freqs, il, color=color, linewidth=2.5, label=label)

    ax2.axhline(y=0.5, color="red", linestyle="--", alpha=0.5, linewidth=1)
    ax2.text(30, 0.55, "0.5 dB target max", color="red", fontsize=9, alpha=0.7)

    for name, f in HAM_BANDS.items():
        ax2.axvline(x=f, color="gray", alpha=0.12, linewidth=1)

    ax2.set_xlabel("Frequency (MHz)", fontsize=12)
    ax2.set_ylabel("Insertion Loss (dB)", fontsize=12)
    ax2.set_title("49:1 Unun — Insertion Loss without Compensation Cap",
                  fontsize=14)
    ax2.legend(fontsize=10)
    ax2.set_xlim(1, 50)
    ax2.set_ylim(0, 3)
    ax2.invert_yaxis()
    ax2.grid(True, which="both", alpha=0.3)
    fig2.tight_layout()
    fig2.savefig("unun49_insertion_loss.png", dpi=150)
    print(f"Saved: unun49_insertion_loss.png")

    # =========================================================================
    # Plot 3: SWR with Compensation Capacitor (Design A)
    # =========================================================================
    fig3, ax3 = plt.subplots(figsize=(12, 7))

    cap_values = [0, 82, 100, 120, 150]
    cap_colors = ["#9E9E9E", "#FF9800", "#2196F3", "#4CAF50", "#9C27B0"]
    cap_styles = [":", "--", "-", "--", ":"]

    for c_pf, color, style in zip(cap_values, cap_colors, cap_styles):
        _, _, swr = unun49_performance(freqs, 14, 2, MIX43_DATA, 1,
                                        c_comp_pf=c_pf)
        lbl = f"No cap" if c_pf == 0 else f"{c_pf} pF"
        lw = 2.5 if c_pf == 100 else 1.8
        ax3.semilogx(freqs, swr, style, color=color, linewidth=lw, label=lbl)

    ax3.axhline(y=1.5, color="orange", linestyle="--", alpha=0.4, linewidth=1)
    ax3.axhline(y=2.0, color="red", linestyle="--", alpha=0.4, linewidth=1)
    ax3.text(35, 1.53, "1.5:1", color="orange", fontsize=8, alpha=0.7)
    ax3.text(35, 2.03, "2.0:1", color="red", fontsize=8, alpha=0.7)

    for name, f in HAM_BANDS.items():
        ax3.axvline(x=f, color="gray", alpha=0.12, linewidth=1)

    ax3.set_xlabel("Frequency (MHz)", fontsize=12)
    ax3.set_ylabel("SWR at 50 Ω port", fontsize=12)
    ax3.set_title("Design A (14T/2T FT-240-43) — SWR vs Compensation Capacitor\n"
                  "(with ideal 2450 Ω load)", fontsize=13)
    ax3.legend(fontsize=10, title="Comp. Cap", title_fontsize=10)
    ax3.set_xlim(1, 50)
    ax3.set_ylim(1, 4)
    ax3.grid(True, which="both", alpha=0.3)
    fig3.tight_layout()
    fig3.savefig("unun49_swr_with_cap.png", dpi=150)
    print(f"Saved: unun49_swr_with_cap.png")

    plt.show()


if __name__ == "__main__":
    main()
