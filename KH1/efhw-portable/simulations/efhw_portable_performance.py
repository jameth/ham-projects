#!/usr/bin/env python3
"""
Portable EFHW Unun + 1:1 CMC Performance Calculator

Models the integrated EFHW unun (FT-50-43 at 23T/3T = 58.8:1, K6ARK
recommended) and 1:1 CMC (FT-50-43, 12T bifilar) for the KH1 portable
EFHW antenna system. The "49:1" community name is a misnomer — the
actual ratio is 58.8:1 in K6ARK's recommended build. See README.md for
why and for alternative turn counts (21T/49:1, 24T/64:1, etc.).

Extends the parent project's 49:1 simulator (../../../49-1-unun/simulations/
unun49_performance.py) with FT-50 geometry and adds CMC analysis.

Usage:
    MPLBACKEND=Agg python efhw_portable_performance.py

Outputs:
    - efhw_portable_unun_il.png       (insertion loss across designs)
    - efhw_portable_unun_swr.png      (SWR with comp cap sweep)
    - efhw_portable_cmc_z.png         (CMC choking impedance)
    - efhw_portable_combined.png      (system view: unun IL + CMC Z)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.interpolate import interp1d


# =============================================================================
# Core Geometries
# =============================================================================

class CoreGeometry:
    """Toroid geometry and derived constants."""
    def __init__(self, name, od_mm, id_mm, ht_mm):
        self.name = name
        self.OD = od_mm * 1e-3
        self.ID = id_mm * 1e-3
        self.HT = ht_mm * 1e-3
        self.le = np.pi * (self.OD + self.ID) / 2
        self.Ae = self.HT * (self.OD - self.ID) / 2
        self.MU_0 = 4 * np.pi * 1e-7
        self.CORE_CONST = self.MU_0 * self.Ae / self.le

    def __repr__(self):
        return (f"{self.name}: OD={self.OD*1e3:.1f} mm, ID={self.ID*1e3:.2f} mm, "
                f"H={self.HT*1e3:.2f} mm, Ae={self.Ae*1e6:.2f} mm², "
                f"le={self.le*1e3:.2f} mm, C={self.CORE_CONST:.3e} H")


FT240 = CoreGeometry("FT-240", 61.0, 35.55, 12.7)   # bench reference
FT82  = CoreGeometry("FT-82",  21.0, 13.1,   6.35)  # mid-size portable
FT50  = CoreGeometry("FT-50",  12.7,  7.15,  4.85)  # micro-portable (target)


# =============================================================================
# Complex Permeability (matches parent project tables for cross-validation)
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

KH1_BANDS = {
    "40m":  7.05,
    "30m": 10.12,
    "20m": 14.06,
    "17m": 18.09,
    "15m": 21.06,
}


def interpolate_permeability(data, freqs_mhz):
    """Log-log interpolation of complex permeability. Identical to parent project."""
    f_data = data[:, 0]
    log_f = np.log10(f_data)
    log_freqs = np.log10(freqs_mhz)
    interp_mu_p = interp1d(log_f, np.log10(data[:, 1]), kind="cubic",
                           fill_value="extrapolate")  # type: ignore[arg-type]
    interp_mu_pp = interp1d(log_f, np.log10(data[:, 2]), kind="cubic",
                            fill_value="extrapolate")  # type: ignore[arg-type]
    return 10 ** interp_mu_p(log_freqs), 10 ** interp_mu_pp(log_freqs)


def magnetizing_impedance(freqs_mhz, turns, material_data, core, num_cores=1):
    """
    Calculate magnetizing impedance of a winding on a given core.
    Generalizes the parent project's function to accept any core geometry.
    """
    mu_p, mu_pp = interpolate_permeability(material_data, freqs_mhz)
    omega = 2 * np.pi * freqs_mhz * 1e6
    n2 = turns ** 2
    factor = omega * n2 * num_cores * core.CORE_CONST
    rm = factor * mu_pp
    xm = factor * mu_p
    zm_mag = np.sqrt(rm**2 + xm**2)
    mu_p_low, _ = interpolate_permeability(material_data,
                                           np.array([material_data[0, 0]]))
    lm = n2 * num_cores * core.CORE_CONST * mu_p_low[0]
    return rm, xm, zm_mag, lm


def unun49_performance(freqs_mhz, total_turns, tap_turns, material_data, core,
                       num_cores=1, z_source=50.0, z_load=None,
                       c_comp_pf=0.0, coupling_k=0.95):
    """
    EFHW unun performance: insertion loss, return loss, SWR.

    The transformation ratio is (total_turns / tap_turns)². The default
    load is the "natural matched" load z_source × ratio, so each design
    is tested against its own correct load (21T/3T → 2450 Ω, 23T/3T →
    2939 Ω, 24T/3T → 3200 Ω, etc.). Pass z_load explicitly to test a
    design against a deliberately mismatched load.

    Same model as parent project, generalized for arbitrary core.
    """
    ratio = (total_turns / tap_turns) ** 2
    if z_load is None:
        z_load = z_source * ratio  # natural matched load for this design
    rm, xm, _, lm = magnetizing_impedance(freqs_mhz, total_turns,
                                           material_data, core, num_cores)
    omega = 2 * np.pi * freqs_mhz * 1e6
    zm = rm + 1j * xm
    lm_primary = lm / ratio
    l_leak = (1 - coupling_k**2) * lm_primary
    z_leak = 1j * omega * l_leak
    z_load_ref = z_load / ratio
    zm_primary = zm / ratio

    if c_comp_pf > 0:
        c_comp = c_comp_pf * 1e-12
        z_cap = 1.0 / (1j * omega * c_comp)
        z_shunt = (zm_primary * z_cap) / (zm_primary + z_cap)
    else:
        z_shunt = zm_primary

    z_parallel = (z_shunt * z_load_ref) / (z_shunt + z_load_ref)
    z_total = z_leak + z_parallel

    gamma = (z_total - z_source) / (z_total + z_source)
    return_loss_db = -20 * np.log10(np.abs(gamma) + 1e-12)
    swr = (1 + np.abs(gamma)) / (1 - np.abs(gamma) + 1e-12)
    swr = np.clip(swr, 1.0, 100.0)

    i_total = 1.0 / (z_source + z_total)
    v_parallel = i_total * z_parallel
    i_load = v_parallel / z_load_ref
    p_load = 0.5 * np.abs(i_load)**2 * np.real(z_load_ref)
    p_available = 0.5 / (4 * z_source)
    tpg = p_load / p_available
    insertion_loss_db = -10 * np.log10(tpg + 1e-12)

    return insertion_loss_db, return_loss_db, swr


def cmc_choking_impedance(freqs_mhz, turns, material_data, core, num_cores=1):
    """
    1:1 CMC choking impedance for a bifilar-wound choke.
    For a bifilar choke, common-mode impedance equals the magnetizing
    impedance of one winding (the differential mode is balanced and
    presents low impedance).
    """
    rm, xm, zm_mag, _ = magnetizing_impedance(freqs_mhz, turns, material_data,
                                               core, num_cores)
    return rm, xm, zm_mag


def print_unun_performance(freqs, design):
    """Print 49:1 unun performance table for a design tuple."""
    label, total, tap, mat, core, num, c_comp = design
    il, rl, swr = unun49_performance(freqs, total, tap, mat, core, num,
                                      c_comp_pf=c_comp)
    _, _, zm_mag, lm = magnetizing_impedance(freqs, total, mat, core, num)
    ratio = (total / tap) ** 2
    print(f"\n{'='*78}")
    print(f"  {label}")
    print(f"  Core: {core.name} × {num}, {total}T tap@{tap}T, ratio={ratio:.0f}:1")
    print(f"  Lm (full winding) = {lm*1e6:.1f} μH")
    print(f"  Compensation cap: {c_comp:.0f} pF" if c_comp > 0 else
          f"  Compensation cap: none")
    print(f"{'='*78}")
    print(f"  {'Band':<6} {'Freq':>6} {'|Zm|':>8} {'IL':>7} {'RL':>7} {'SWR':>6}")
    print(f"  {'─'*6} {'─'*6} {'─'*8} {'─'*7} {'─'*7} {'─'*6}")
    for name, f in KH1_BANDS.items():
        idx = np.argmin(np.abs(freqs - f))
        print(f"  {name:<6} {f:>6.2f} {zm_mag[idx]:>8.0f} "
              f"{il[idx]:>7.2f} {rl[idx]:>7.1f} {swr[idx]:>6.2f}")


def print_cmc_performance(freqs, design):
    """Print CMC performance table."""
    label, turns, mat, core, num = design
    rm, xm, zm = cmc_choking_impedance(freqs, turns, mat, core, num)
    print(f"\n{'='*78}")
    print(f"  {label}")
    print(f"  Core: {core.name} × {num}, {turns}T bifilar")
    print(f"{'='*78}")
    print(f"  {'Band':<6} {'Freq':>6} {'|Z|':>8} {'Rs':>8} {'Xs':>8}")
    print(f"  {'─'*6} {'─'*6} {'─'*8} {'─'*8} {'─'*8}")
    for name, f in KH1_BANDS.items():
        idx = np.argmin(np.abs(freqs - f))
        print(f"  {name:<6} {f:>6.2f} {zm[idx]:>8.0f} "
              f"{rm[idx]:>8.0f} {xm[idx]:>8.0f}")


def main():
    freqs = np.logspace(np.log10(1), np.log10(50), 600)

    print("Portable EFHW 49:1 Unun + 1:1 CMC Performance Calculator")
    print(f"\nCore geometries:")
    print(f"  {FT240}")
    print(f"  {FT82}")
    print(f"  {FT50}")

    # =========================================================================
    # Unun designs
    # =========================================================================
    unun_designs = [
        # label, total_turns, tap_turns, mix_data, core, num_cores, c_comp_pf
        # Each design is tested against its natural matched load:
        # z_load = 50 × (total/tap)². So 21T/3T uses 2450 Ω, 23T/3T
        # uses 2939 Ω, 24T/3T uses 3200 Ω, etc.
        ("Old A: 1× FT-50-43, 14T/2T (49:1), 100 pF",   14, 2, MIX43_DATA, FT50,  1, 100),
        ("Old B: 2× FT-50-43, 14T/2T (49:1), 100 pF",   14, 2, MIX43_DATA, FT50,  2, 100),
        ("True 49:1: 1× FT-50-43, 21T/3T, 100 pF",      21, 3, MIX43_DATA, FT50,  1, 100),
        ("K6ARK recommended: 1× FT-50-43, 23T/3T (59:1), 100 pF", 23, 3, MIX43_DATA, FT50, 1, 100),
        ("K6ARK image-count: 1× FT-50-43, 24T/3T (64:1), 100 pF", 24, 3, MIX43_DATA, FT50, 1, 100),
        ("All-FT-50 stacked: 2× FT-50-43, 23T/3T, 100 pF", 23, 3, MIX43_DATA, FT50,  2, 100),
        ("K6ARK: 1× FT-82-43, 21T/3T (49:1), no cap",   21, 3, MIX43_DATA, FT82,  1,   0),
        ("K6ARK: 1× FT-82-43, 21T/3T (49:1), 100 pF",   21, 3, MIX43_DATA, FT82,  1, 100),
        ("K6ARK on FT-82: 1× FT-82-43, 23T/3T (59:1), 100 pF", 23, 3, MIX43_DATA, FT82, 1, 100),
        ("Alt: 1× FT-82-43, 14T/2T (49:1), 100 pF",     14, 2, MIX43_DATA, FT82,  1, 100),
        ("Reference: 1× FT-240-43, 14T/2T (49:1), 100 pF", 14, 2, MIX43_DATA, FT240, 1, 100),
    ]

    for d in unun_designs:
        print_unun_performance(freqs, d)

    # =========================================================================
    # CMC designs
    # =========================================================================
    cmc_designs = [
        # label, turns, mix_data, core, num_cores
        # FT-50-31 is NOT readily available; mix 43 alternatives below
        ("CMC: 1× FT-50-43, 9T bifilar",      9, MIX43_DATA, FT50, 1),
        ("CMC: 1× FT-50-43, 12T bifilar",    12, MIX43_DATA, FT50, 1),
        ("CMC: 2× FT-50-43, 9T bifilar",      9, MIX43_DATA, FT50, 2),
        ("CMC: 2× FT-50-43, 12T bifilar",    12, MIX43_DATA, FT50, 2),
        ("Reference: 1× FT-50-31, 10T (theory)", 10, MIX31_DATA, FT50, 1),
    ]

    for d in cmc_designs:
        print_cmc_performance(freqs, d)

    # =========================================================================
    # Plot 1: Unun insertion loss across variants
    # =========================================================================
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    plot_designs = [
        ("1× FT-50-43, 14T/2T (49:1, old A)",       14, 2, MIX43_DATA, FT50,  1, 100, "#FF9800", ":"),
        ("1× FT-50-43, 21T/3T (true 49:1)",         21, 3, MIX43_DATA, FT50,  1, 100, "#E91E63", "--"),
        ("1× FT-50-43, 23T/3T (K6ARK recommended, 59:1)", 23, 3, MIX43_DATA, FT50, 1, 100, "#E91E63", "-"),
        ("1× FT-50-43, 24T/3T (K6ARK image, 64:1)", 24, 3, MIX43_DATA, FT50,  1, 100, "#E91E63", ":"),
        ("2× FT-50-43, 23T/3T (all-FT-50)",         23, 3, MIX43_DATA, FT50,  2, 100, "#FF5722", "--"),
        ("1× FT-82-43, 21T/3T (FT-82 49:1)",        21, 3, MIX43_DATA, FT82,  1, 100, "#2196F3", "--"),
        ("1× FT-82-43, 23T/3T (FT-82 59:1)",        23, 3, MIX43_DATA, FT82,  1, 100, "#2196F3", "-"),
        ("Bench ref: 1× FT-240-43, 14T/2T",         14, 2, MIX43_DATA, FT240, 1, 100, "#4CAF50", "--"),
    ]
    for label, total, tap, mat, core, num, c_pf, color, style in plot_designs:
        il, _, _ = unun49_performance(freqs, total, tap, mat, core, num,
                                       c_comp_pf=c_pf)
        ax1.semilogx(freqs, il, style, color=color, linewidth=2, label=label)

    ax1.axhline(y=1.0, color="orange", linestyle="--", alpha=0.4)
    ax1.text(35, 1.05, "1 dB target (resonant bands)", color="orange",
             fontsize=8, alpha=0.7)
    ax1.axhline(y=2.0, color="red", linestyle="--", alpha=0.4)
    ax1.text(35, 2.05, "2 dB max (non-resonant)", color="red",
             fontsize=8, alpha=0.7)

    for name, f in KH1_BANDS.items():
        ax1.axvline(x=f, color="gray", alpha=0.15)
        ax1.text(f, 4.5, name, ha="center", fontsize=8, color="gray")

    ax1.set_xlabel("Frequency (MHz)", fontsize=12)
    ax1.set_ylabel("Insertion Loss (dB)", fontsize=12)
    ax1.set_title("Portable EFHW Unun — Insertion Loss vs Frequency\n"
                  "(each design terminated in its natural matched load:\n"
                  "21T→2450 Ω, 23T→2940 Ω, 24T→3200 Ω; KH1 bands shaded)",
                  fontsize=12)
    ax1.legend(fontsize=9, loc="upper right")
    ax1.set_xlim(3, 50)
    ax1.set_ylim(0, 5)
    ax1.invert_yaxis()
    ax1.grid(True, which="both", alpha=0.3)
    fig1.tight_layout()
    fig1.savefig("efhw_portable_unun_il.png", dpi=150)
    print(f"\nSaved: efhw_portable_unun_il.png")

    # =========================================================================
    # Plot 2: SWR with comp cap sweep (Variant B)
    # =========================================================================
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    cap_values = [0, 68, 82, 100, 120, 150, 180]
    cap_colors = mpl.colormaps["viridis"](np.linspace(0.1, 0.9, len(cap_values)))

    for c_pf, color in zip(cap_values, cap_colors):
        _, _, swr = unun49_performance(freqs, 23, 3, MIX43_DATA, FT50, 1,
                                        c_comp_pf=c_pf)
        lbl = "no cap" if c_pf == 0 else f"{c_pf} pF"
        lw = 2.5 if c_pf == 100 else 1.6
        ax2.semilogx(freqs, swr, color=color, linewidth=lw, label=lbl)

    ax2.axhline(y=1.5, color="orange", linestyle="--", alpha=0.4)
    ax2.axhline(y=2.0, color="red", linestyle="--", alpha=0.4)
    ax2.text(35, 1.53, "1.5:1", color="orange", fontsize=8)
    ax2.text(35, 2.03, "2.0:1", color="red", fontsize=8)

    for name, f in KH1_BANDS.items():
        ax2.axvline(x=f, color="gray", alpha=0.15)
        ax2.text(f, 3.7, name, ha="center", fontsize=8, color="gray")

    ax2.set_xlabel("Frequency (MHz)", fontsize=12)
    ax2.set_ylabel("SWR at 50 Ω port", fontsize=12)
    ax2.set_title("Primary build (1× FT-50-43, 23T/3T = 58.8:1) — SWR vs Compensation Cap\n"
                  "(ideal 2940 Ω matched load on radiator port)", fontsize=12)
    ax2.legend(fontsize=9, title="C_comp", title_fontsize=10)
    ax2.set_xlim(3, 50)
    ax2.set_ylim(1, 4)
    ax2.grid(True, which="both", alpha=0.3)
    fig2.tight_layout()
    fig2.savefig("efhw_portable_unun_swr.png", dpi=150)
    print(f"Saved: efhw_portable_unun_swr.png")

    # =========================================================================
    # Plot 3: CMC choking impedance comparison
    # =========================================================================
    fig3, ax3 = plt.subplots(figsize=(12, 7))
    cmc_plot = [
        ("1× FT-50-43, 9T",                    9, MIX43_DATA, FT50, 1, "#FF9800", "-"),
        ("1× FT-50-43, 12T",                  12, MIX43_DATA, FT50, 1, "#2196F3", "-"),
        ("2× FT-50-43, 9T",                    9, MIX43_DATA, FT50, 2, "#4CAF50", "-"),
        ("2× FT-50-43, 12T",                  12, MIX43_DATA, FT50, 2, "#9C27B0", "-"),
        ("Reference: 1× FT-50-31 (theory)",   10, MIX31_DATA, FT50, 1, "#666666", "--"),
    ]
    for label, turns, mat, core, num, color, style in cmc_plot:
        _, _, zm = cmc_choking_impedance(freqs, turns, mat, core, num)
        ax3.semilogx(freqs, zm, style, color=color, linewidth=2.2, label=label)

    ax3.axhline(y=1500, color="orange", linestyle="--", alpha=0.4)
    ax3.text(35, 1550, "1.5 kΩ design target", color="orange", fontsize=9)
    ax3.axhline(y=1000, color="gray", linestyle=":", alpha=0.4)
    ax3.text(35, 1030, "1 kΩ practical floor", color="gray", fontsize=9)

    for name, f in KH1_BANDS.items():
        ax3.axvline(x=f, color="gray", alpha=0.15)
        ax3.text(f, 200, name, ha="center", fontsize=8, color="gray")

    ax3.set_xlabel("Frequency (MHz)", fontsize=12)
    ax3.set_ylabel("|Z_CM| (Ω)", fontsize=12)
    ax3.set_title("Common-Mode Choke — |Z| vs Frequency\n"
                  "(FT-50-43 since FT-50-31 not stocked; mix 31 ref shown)",
                  fontsize=13)
    ax3.legend(fontsize=10)
    ax3.set_xlim(3, 50)
    ax3.set_ylim(0, 5000)
    ax3.grid(True, which="both", alpha=0.3)
    fig3.tight_layout()
    fig3.savefig("efhw_portable_cmc_z.png", dpi=150)
    print(f"Saved: efhw_portable_cmc_z.png")

    # =========================================================================
    # Plot 4: Combined system view
    # =========================================================================
    fig4, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True)

    # Top: unun IL for primary build (1× FT-50-43, 23T/3T) with 100 pF
    ax_il = axes[0]
    il, _, swr = unun49_performance(freqs, 23, 3, MIX43_DATA, FT50, 1,
                                     c_comp_pf=100)
    ax_il.semilogx(freqs, il, color="#E91E63", linewidth=2.5, label="Unun IL")
    ax_il.axhline(y=1.0, color="orange", linestyle="--", alpha=0.4)
    ax_il.set_ylabel("Insertion Loss (dB)", fontsize=11)
    ax_il.set_title("Primary Build (1× FT-50-43, 23T/3T = 58.8:1, 100 pF) — System Performance",
                    fontsize=12)
    ax_il.set_ylim(0, 3)
    ax_il.invert_yaxis()
    ax_il.grid(True, which="both", alpha=0.3)
    for name, f in KH1_BANDS.items():
        ax_il.axvline(x=f, color="gray", alpha=0.15)
        ax_il.text(f, 2.7, name, ha="center", fontsize=8, color="gray")
    ax_il.legend(fontsize=10, loc="upper right")

    # Bottom: CMC choking Z
    ax_cmc = axes[1]
    _, _, zm = cmc_choking_impedance(freqs, 12, MIX43_DATA, FT50, 2)
    ax_cmc.semilogx(freqs, zm, color="#9C27B0", linewidth=2.5,
                    label="CMC |Z| (12T bifilar on 2× FT-50-43)")
    ax_cmc.axhline(y=1500, color="orange", linestyle="--", alpha=0.4,
                   label="1.5 kΩ target")
    ax_cmc.set_xlabel("Frequency (MHz)", fontsize=11)
    ax_cmc.set_ylabel("|Z_CM| (Ω)", fontsize=11)
    ax_cmc.set_xlim(3, 50)
    ax_cmc.set_ylim(0, 4000)
    ax_cmc.grid(True, which="both", alpha=0.3)
    for name, f in KH1_BANDS.items():
        ax_cmc.axvline(x=f, color="gray", alpha=0.15)
        ax_cmc.text(f, 100, name, ha="center", fontsize=8, color="gray")
    ax_cmc.legend(fontsize=10, loc="upper right")

    fig4.tight_layout()
    fig4.savefig("efhw_portable_combined.png", dpi=150)
    print(f"Saved: efhw_portable_combined.png")


if __name__ == "__main__":
    main()
