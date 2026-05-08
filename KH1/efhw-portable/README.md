# Portable 49:1 EFHW + 1:1 CMC Combined Unit

## Design Goals

- Single small enclosure containing a 49:1 unun and a 1:1 common-mode
  choke (CMC), feeding a ~66 ft EFHW radiator from the KH1's BNC jack
- Cover all five KH1 ham bands (40/30/20/17/15 m), with peak efficiency
  on 40/20/15 (harmonic-related to the 40 m fundamental) and ATU-tunable
  performance on 30/17 (non-harmonic)
- Power handling: 10 W continuous CW (2× the KH1 maximum, gives margin
  for ATU mismatches and prolonged duty cycles)
- Insertion loss: < 1.5 dB on resonant bands (40/20/15), < 2 dB on
  non-resonant bands (30/17). (Simulation suggests Variant B + 100 pF
  cap achieves 1.3-1.6 dB across all KH1 bands; see simulation output.)
- CM isolation: |Z_CM| > 1.5 kΩ across 7-22 MHz (10T on FT-50-31
  delivers 1.7-2.1 kΩ per simulation)
- Total weight: < 50 g
- Form factor: fits in a Hammond 1551KFLBK (50 × 35 × 20 mm) or similar
- Connectors: BNC female input, dual binding posts (or banana jacks)
  for radiator and counterpoise stub
- Use available materials: FT-82-43 core (mix 43, transformer; community
  standard for QRP EFHW), FT-50-43 cores (mix 43, choke; FT-50-31 not
  stocked at retail), magnet wire, NP0 cap

## Why an EFHW for the KH1

Half-wave end-fed antennas are resonant at integer harmonics of their
design frequency. A 40 m EFHW (~66 ft) is naturally resonant on:

- 40 m (λ/2 fundamental)
- 20 m (λ — 2nd harmonic, behaves like λ/2 at the feedpoint)
- 15 m (3λ/2 — 3rd harmonic)

The remaining KH1 bands (30 m and 17 m) are not harmonically related
to 40 m. On those bands, the EFHW presents a mid-Z reactive feedpoint
that the 49:1 transforms to a few-ohm range. The KH1's internal ATU
finishes the match. Total loss on these bands is 1-2 dB more than the
resonant bands but still better than a comparable EFRW or whip system.

## Architecture

```
[BNC F input]
     │
     │  (rig side)
     ▼
[1:1 CMC, FT-50-43 mix 43, 12T bifilar]
     │
     │  (decoupled common-mode reference)
     ▼
[49:1 unun, FT-82-43 mix 43, 21T autotransformer w/ 3T tap]
     │      │
     │      └──── [CP binding post] (cold side, 6-9' counterpoise stub)
     │
     ▼
[Radiator binding post] (hot side, ~65'6" wire)
```

The CMC sits between the BNC and the unun. This decouples the rig
chassis from the antenna's RF reference, so the counterpoise stub on
the unun's cold side becomes the actual CM ground reference rather
than the operator's body or the rig case.

### Why FT-82-43 for the unun (not FT-50)

Single FT-50-43 lacks magnetizing inductance for QRP-grade 40 m
performance (sim shows 2.76 dB IL on 40 m). Stacking two FT-50s helps
but matches the K6ARK community-standard FT-82-43 in capability while
costing a similar amount of weight. FT-82-43 with 21T/3T (the K6ARK
turn count) gives 195 μH magnetizing inductance, essentially identical
to a single FT-240-43 with 14T (the bench-grade reference). The
simulation confirms within 0.01 dB IL match on every KH1 band.

### Why FT-50-43 for the CMC (not FT-50-31)

FT-50-31 (mix 31 in FT-50 size) is **not stocked at retail.** Fair-Rite's
mix 31 hobbyist parts are FT-114-31, FT-140-31, and FT-240-31 only.
Mix 43 is the next-best HF choke material; its loss tangent (μ'') is
lower than mix 31's at 5-15 MHz but still significant. With 12 bifilar
turns on a single FT-50-43, the choke delivers > 1.5 kΩ |Z_CM| across
the entire KH1 band coverage (1.93 kΩ at 7 MHz rising to 3.5 kΩ at 15
MHz). That meets the design target and exceeds the mix-31 reference's
1.67 kΩ at 7 MHz.

## Key Design Decisions

### Mix 43 for both the 49:1 and the CMC

Ideally the CMC would use mix 31 (higher μ'' loss tangent above 3 MHz
absorbs CM energy as heat). However, FT-50-31 is not stocked at retail
distributors. Mix 43 still has significant loss at 7-30 MHz (peak μ''
near 7-15 MHz) and works well as a choke when wound with enough turns.
The simulation shows 12T bifilar on a single FT-50-43 hits the same
1.5+ kΩ |Z_CM| target that 10T on FT-50-31 would have provided.

For the 49:1 transformer, mix 43 is the right choice anyway — lower
loss = better signal transmission to the load.

### Compensation capacitor

A small parallel cap (100-150 pF NP0 / C0G, 1.5 kV) across the unun's
primary cancels the leakage inductance at higher frequencies. Without
it, SWR tends to climb on the 3rd harmonic (15 m for a 40 m EFHW).
Exact value should be tuned via simulation and / or NanoVNA sweep.
Starting value: 100 pF (matches K6ARK and the bench design).

## Design Variants

| Variant | Unun core | Unun turns | CMC core | CMC turns | Sim 40 m IL | Sim CMC |Z| @ 7 MHz | Weight |
|---|---|---|---|---|---|---|---|
| **Primary** (recommended) | **1× FT-82-43** | **21T / 3T tap** (K6ARK) | **1× FT-50-43** | **12T bifilar** | **1.32 dB** | **1.93 kΩ** | **~30 g** |
| Heavier-CMC | 1× FT-82-43 | 21T / 3T tap | 2× FT-50-43 stacked | 12T bifilar | 1.32 dB | 3.85 kΩ | ~35 g |
| Lighter | 1× FT-82-43 | 14T / 2T tap | 1× FT-50-43 | 9T bifilar | 2.57 dB | 1.09 kΩ | ~25 g |

**Primary is the recommended build.** The 21T/3T config on FT-82-43 is
the K6ARK community standard, and the simulation shows it delivers
performance within 0.01 dB of the bench-grade FT-240-43 design across
every KH1 band. 12T bifilar on a single FT-50-43 gives more than 1.5 kΩ
of |Z_CM| on every band, exceeding the 1.67 kΩ that mix 31 would have
provided at 7 MHz.

Pick the heavier-CMC variant if you've had RFI issues in past builds.
Pick the lighter variant only if weight is critical and you can accept
~1 dB more IL on 40 m.

## Acceptance Criteria

To be tested with NanoVNA H/V2 after the build is complete.

| Test | Method | Pass |
|---|---|---|
| 50 → 2450 Ω SWR | 50 Ω at BNC, 2450 Ω resistive at radiator BP | < 1.5:1 from 7-21.5 MHz |
| Insertion loss | S21 with matched terminations | < 1 dB at 7/14/21 MHz, < 2 dB at 10/18 MHz |
| CM isolation | open-circuit one wire of bifilar pair, measure |Z| from common to single wire | > 1.5 kΩ at all KH1 band centers |
| Thermal | 5 W carrier into matched system for 5 min | core temp rise < 20 °C |
| KH1 power output | confirm 5 W into matched system on each band via MENU:VBAT | within 0.5 dB of bare-coax baseline |

## Field Test Plan

After completion, measure on-air performance against the WD8RIF EFRW
setup (same wire support, same QTH, same band, same hour) using the
Reverse Beacon Network for objective signal-strength comparison.

- 10 CQ calls on each band with each antenna
- Record max SNR per skimmer per call
- Compare median SNR per band
- Expected result: EFHW should outperform EFRW on the resonant bands
  (40/20/15) by 2-4 dB; comparable on 30/17

## Project Files

- `bom.md` — bill of materials with sourcing notes
- `schematics/` — circuit diagrams and winding diagrams
- `simulations/efhw_portable_performance.py` — Python sim, extends
  the parent project's 49:1 simulator with FT-50 geometry and adds
  CMC analysis
- `measurements/` — NanoVNA sweeps, on-air comparison data, photos

## References

- Parent project: `../../49-1-unun/` (FT-240-43 bench design)
- Parent project: `../../common-mode-choke/` (FT-240-31 / FT-240-43 chokes)
- Cross-project notes: `../../notes.md`
- K6ARK Mini 49:1 EFHW (community reference design for QRP portable)
- KM4ACK 40-10 m EFHW (community design with extensive field data)
