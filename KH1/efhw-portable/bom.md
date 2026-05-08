# BOM — Portable 49:1 + 1:1 CMC Combined Unit

**Primary build:** 1× FT-82-43 (21T/3T) unun + 1× FT-50-43 (12T bifilar) CMC.

This BOM was revised after discovering that **FT-50-31 is not stocked
at retail** by the major hobbyist distributors (kitsandparts.com,
Mouser, DigiKey, Amazon for Fair-Rite). The build is now sourced
entirely from commonly stocked parts.

## Cores

| Item | Qty | Source | Approx. price | Notes |
|---|---|---|---|---|
| FT-82-43 toroid (Fair-Rite mix 43, 21 mm OD) | 1 | kitsandparts.com or Mouser | $1.50 | for 49:1 unun. Standard QRP-portable EFHW core. |
| FT-50-43 toroid (Fair-Rite mix 43, 12.7 mm OD) | 1 | kitsandparts.com | $0.75 | for 1:1 CMC, 12T bifilar |

Buy 2-3 spares of each (~$5 total) for botched windings.

If you ever find FT-50-31 from a specialty supplier (Fair-Rite direct,
RF Parts Co, or KF7P Metalwerks may have small mix-31 toroids), use it
for the CMC instead — same turns count, slightly higher |Z| in the
choke's working range. Not required.

## Wire

| Item | Qty | Source | Notes |
|---|---|---|---|
| 22 or 24 AWG enameled magnet wire | ~5 ft | kitsandparts.com or local | unun secondary: 21T full winding on FT-82 takes ~20 inches; primary tap (3T) takes ~4 inches |
| Bifilar 26 AWG enameled magnet wire pair (contrasting colors) | ~3 ft | same | CMC bifilar 12T on FT-50 takes ~12 inches per wire = ~24 in total bifilar |

The K6ARK build uses 22 AWG for the unun (full power margin to 20 W).
At KH1's 5 W max you can drop to 24 AWG for slightly easier winding,
but 22 AWG is more rugged.

## Components

| Item | Qty | Source | Notes |
|---|---|---|---|
| 100 pF NP0 / C0G ceramic cap, 1.5 kV | 1 | Mouser, DigiKey | compensation cap across unun primary |
| 82 pF and 150 pF NP0 caps (alternates) | 1 each | same | optional values to try if 100 pF doesn't yield best 15 m SWR |
| Heat-shrink tubing assortment | as needed | local | for wire termination and color coding |

## Mechanical

| Item | Qty | Source | Notes |
|---|---|---|---|
| Hammond 1551KFLBK enclosure (50×35×20 mm) | 1 | Mouser, DigiKey | matte black ABS; needs holes for connectors |
| BNC female panel-mount connector | 1 | Amphenol or similar | **isolate from chassis** with insulating shoulder washers |
| Insulating shoulder washer (M5 / 1/4") | 2 | local | for BNC isolation |
| Banana binding posts, red and black | 1 pair | local | radiator and CP outputs |
| OR: dual banana jacks (panel mount) | 1 pair | local | lighter alternative |

## Hardware

| Item | Qty | Notes |
|---|---|---|
| #4 or M3 standoffs (4 mm) | 4 | optional internal mounting |
| Small piece of FR4 perfboard | 1 | optional internal substrate; can be done point-to-point instead |
| Thread-locking compound | tiny | on the BNC mounting nut |

## Antenna Wires

| Item | Qty | Notes |
|---|---|---|
| 26 AWG silicone-insulated stranded wire | 65'6" | EFHW radiator. Trim to actual resonance. |
| 26 or 28 AWG silicone-insulated wire | 9' | counterpoise stub |
| Small ring or knot at far end of radiator | 1 | tossing point |
| Tufteln-style wire winder (3D printed) or fishing-line spool | 1 | tangle-free storage |

## Tools (already on the bench)

- Toroid winding jig (or patience)
- Fine-point soldering iron
- 60/40 leaded solder (or lead-free)
- Wire strippers (22-26 AWG)
- Heat-shrink shrinker
- Drill press for the enclosure
- NanoVNA H or V2 for measurement
- Test loads: 50 Ω and 2450 Ω resistive (or parallel resistor combos)

## Approximate Cost

| Category | Cost |
|---|---|
| Cores (2) | $2-3 |
| Wire | $5 |
| Comp cap | $2 |
| Enclosure | $10 |
| BNC + binding posts | $10 |
| Antenna wire (~75 ft) | $15 |
| **Total** | **~$45** |

Compare: the K6ARK QRP 49:1 EFHW kit retails ~$40 with similar
topology but no integrated CMC. Building it yourself saves $5, gives
you the integrated CMC, and matches your existing bench-grade 49:1
design framework.

## Note: Why not TDK N30?

Sometimes asked as an alternative when Fair-Rite parts are out of stock.
TDK N30 is a **power ferrite** optimized for SMPS frequencies (25 kHz
to ~1 MHz). At HF (3-30 MHz) it's outside its design window. Not a
substitute for either mix 43 or mix 31 in HF antenna work. Stick with
Fair-Rite materials, or accept the FT-114-31 size if you specifically
need mix 31.
