# BOM — Portable 49:1 + 1:1 CMC Combined Unit

**Primary build:** 1× FT-50-43 unun (3T primary + 20 more = **23T
total**, K6ARK recommended) + 1× FT-50-43 CMC (12T bifilar).

This BOM uses a single core type throughout (FT-50-43). The unun is
K6ARK's recommended "general use" build: 3 turns primary, pull tap,
then 20 more turns continuous. Total 23 turns. Transformation ratio
(23/3)² = **58.8:1**, matched load ~2940 Ω.

The "49:1 EFHW" name is a community label — the actual ratio is
58.8:1, which matches real-world EFHW feedpoint impedances better
than a textbook 49:1. The sim shows FT-50 at 23T lands within 0.08 dB
of FT-82-43 at the same turn count on every KH1 band. See `README.md`
for the full FT-50 vs FT-82 trade-off and the variant table.

FT-50-31 (the ideal CMC material) is **not stocked at retail** by the
major hobbyist distributors (kitsandparts.com, Mouser, DigiKey, Amazon
for Fair-Rite), so the CMC uses mix 43 with more turns to compensate.

## Cores

| Item | Qty | Source | Approx. price | Notes |
|---|---|---|---|---|
| FT-50-43 toroid (Fair-Rite mix 43, 12.7 mm OD) | 2 | kitsandparts.com | $0.75 each | 1× for unun (3T + 20T more = 23T total autotransformer), 1× for 1:1 CMC (12T bifilar) |

Buy 2-3 spares (~$2-3 total) for botched windings. Single part type
simplifies the order.

If you ever find FT-50-31 from a specialty supplier (Fair-Rite direct,
RF Parts Co, or KF7P Metalwerks may have small mix-31 toroids), use it
for the CMC instead — same turns count, slightly higher |Z| in the
choke's working range. Not required.

If you want a thermal-margin upgrade for eventual QRO use (15-25 W),
substitute 1× FT-82-43 ($1.50) for the unun core. See the "Bigger-core
alternative" variant in `README.md`. For KH1's 5 W it's unnecessary.

## Wire

| Item | Qty | Source | Notes |
|---|---|---|---|
| 22 or 24 AWG enameled magnet wire | ~3 ft | kitsandparts.com or local | unun: 23T on FT-50 takes ~15 inches + ~3 inches for the tap loop + leads = ~23 inches |
| Bifilar 26 AWG enameled magnet wire pair (contrasting colors) | ~3 ft | same | CMC bifilar 12T on FT-50 takes ~12 inches per wire = ~24 in total bifilar |

The K6ARK build uses 22 AWG for the unun (full power margin to 20 W),
but on the FT-50 winding window 22 AWG is tight — 23 turns fully fills
the inner circumference. **For KH1 at 5 W, 24 AWG is the better
choice:** easier to wind, less prone to enamel damage on the tight
inner radius, and well within the current-handling margin at QRP.

## Components

| Item | Qty | Source | Notes |
|---|---|---|---|
| 100 pF NP0 / C0G ceramic cap, **axial-leaded**, 1.5 kV | 1 | Mouser, DigiKey | compensation cap across unun winding. Leaded (not SMT) — no PCB in the in-line build. |
| 82 pF and 150 pF NP0 caps (alternates, axial-leaded) | 1 each | same | optional values to try if 100 pF doesn't yield best 15 m SWR |
| Heat-shrink tubing assortment (general) | as needed | local | for wire termination and color coding |

## Mechanical — primary build (K6ARK in-line)

| Item | Qty | Source | Notes |
|---|---|---|---|
| BNC male solder-pot connector | 1 | Amphenol RP-BNC-M, Pomona, similar | The bundle solders directly to this. Pre-tin center pin and shield tab before assembly. |
| Outer heat-shrink, 3/4" or 1" diameter, ~4" long | 1 | Mouser, local | Adhesive-lined preferred (permanent seal). Black or clear. |
| Inner heat-shrink, 1/2" diameter, ~2" long | 1 | local | BNC-to-CMC joint sleeve (construction step 4) |
| Short pigtail wire, 26 AWG silicone stranded | 8" | local | Two 4" pigtails (radiator + CP), in different colors if possible |

## Mechanical — alternative build (Hammond box)

Use these instead of the K6ARK in-line mechanical parts if you're
building the openable / weatherproof variant.

| Item | Qty | Source | Notes |
|---|---|---|---|
| Hammond 1551KFLBK enclosure (50×35×20 mm) | 1 | Mouser, DigiKey | matte black ABS; needs holes for connectors |
| BNC female panel-mount connector | 1 | Amphenol or similar | **isolate from chassis** with insulating shoulder washers |
| Insulating shoulder washer (M5 / 1/4") | 2 | local | for BNC isolation |
| Banana binding posts, red and black | 1 pair | local | radiator and CP outputs |
| OR: dual banana jacks (panel mount) | 1 pair | local | lighter alternative |
| Silicone sealant (clear, neutral-cure) | tiny | local | seal connector holes for weather resistance |

## Hardware — Hammond build only

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
- Heat-gun (or hair dryer set high for thin heat-shrink)
- Drill press (Hammond build only — for enclosure holes)
- NanoVNA H or V2 for measurement
- Test loads: 50 Ω and **2940 Ω** resistive (matched load for 23T/3T,
  ratio 58.8:1). See README "Acceptance Criteria" for resistor combos
  that approximate 2940 Ω. If building a true 49:1 reference (21T/3T)
  for comparison, use 2450 Ω instead.

## Approximate Cost

### Primary build (K6ARK in-line)

| Category | Cost |
|---|---|
| Cores (2× FT-50-43) | $1.50-2 |
| Wire (magnet + silicone pigtail) | $4 |
| Comp cap (axial-leaded NP0) | $1 |
| BNC male solder-pot | $3 |
| Heat-shrink (inner + outer) | $1 |
| Antenna wire (~75 ft) | $15 |
| **Total** | **~$26-28** |

### Alternative build (Hammond box)

| Category | Cost |
|---|---|
| Cores (2× FT-50-43) | $1.50-2 |
| Wire (magnet) | $4 |
| Comp cap (NP0) | $2 |
| Hammond 1551KFLBK enclosure | $10 |
| BNC female + binding posts | $10 |
| Hardware (standoffs, washers, silicone) | $3 |
| Antenna wire (~75 ft) | $15 |
| **Total** | **~$45-47** |

Compare: the K6ARK QRP 49:1 EFHW kit retails ~$40 with the same unun
recipe (1× FT-50-43, 3T + 20 more = 23T total) and the same in-line
heat-shrunk form factor — but no integrated CMC. Building it yourself
in this primary configuration runs ~$13 cheaper than the kit, adds
the 1:1 CMC inside the same bundle, and reuses the bench-grade
simulator for design validation.

## Note: Why not TDK N30?

Sometimes asked as an alternative when Fair-Rite parts are out of stock.
TDK N30 is a **power ferrite** optimized for SMPS frequencies (25 kHz
to ~1 MHz). At HF (3-30 MHz) it's outside its design window. Not a
substitute for either mix 43 or mix 31 in HF antenna work. Stick with
Fair-Rite materials, or accept the FT-114-31 size if you specifically
need mix 31.
