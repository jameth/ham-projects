# Portable 49:1 EFHW + 1:1 CMC Combined Unit

## Design Goals

- Single in-line heat-shrunk bundle containing a 49:1 unun and a 1:1
  common-mode choke (CMC), hanging directly off a BNC male plug,
  feeding a ~66 ft EFHW radiator from the KH1's BNC jack
- Cover all five KH1 ham bands (40/30/20/17/15 m), with peak efficiency
  on 40/20/15 (harmonic-related to the 40 m fundamental) and ATU-tunable
  performance on 30/17 (non-harmonic)
- Power handling: 10 W continuous CW (2× the KH1 maximum, gives margin
  for ATU mismatches and prolonged duty cycles)
- Insertion loss: < 1.5 dB on resonant bands (40/20/15), < 2 dB on
  non-resonant bands (30/17). (Simulation suggests primary build
  delivers 1.3-1.6 dB across all KH1 bands; see simulation output.)
- CM isolation: |Z_CM| > 1.5 kΩ across 7-22 MHz (10T on FT-50-31
  delivers 1.7-2.1 kΩ per simulation)
- Total weight: < 20 g for the in-line build; < 40 g for the Hammond
  box variant
- Form factor (primary): ~3/4" diameter × ~4" long heat-shrunk bundle
  off the BNC plug. Alternative: fits in a Hammond 1551KFLBK
  (50 × 35 × 20 mm) box.
- Connectors: BNC male solder-pot (primary, in-line build) with
  hardwired radiator/CP pigtails. Alternative: BNC female chassis-
  mount with dual binding posts (Hammond variant).
- Use available materials: 2× FT-50-43 cores (mix 43; one for the
  unun at 23T total / 3T tap = 58.8:1 ratio, one for the CMC at 12T
  bifilar — the K6ARK QRP kit recommended recipe), magnet wire, NP0
  axial-leaded ceramic cap

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
[~59:1 unun, FT-50-43 mix 43, 23T autotransformer w/ 3T tap]
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

### Why FT-50-43 for the unun (and when to use FT-82-43)

The K6ARK QRP kit ships with **1× FT-50-43, 3 turns primary + 20 turns
more = 23 turns total** (his recommended "general use" build). The
sim confirms FT-50 lands within 0.08 dB of FT-82-43 at the same turn
count on every KH1 band (FT-50 → 1.40 dB IL, FT-82 → 1.32 dB at 40 m).
Both cores yield ~215 μH of magnetizing inductance at 23 turns; their
Ae/le ratios (0.43 mm vs 0.47 mm) are nearly identical, so the core
constant scales 1:1 once turn counts are matched.

The earlier "FT-82 required" claim in this doc was based on a 14T/2T
FT-50 comparison (Lm = 80 μH, 2.76 dB IL on 40 m). That's not how
K6ARK's kit is wound. With matched turn counts the two cores are
interchangeable at QRP.

**Pick FT-50-43 for this build:** lighter (~1.5 vs ~3.5 g), cheaper
($0.75 vs $1.50), single core type shared with the CMC (simpler BOM),
matches the field-proven K6ARK kit recipe.

**Pick FT-82-43 instead:** if you want thermal headroom beyond 10 W
for an eventual QRO upgrade, or if 24 AWG on the FT-50 window is
fighting you.

For the KH1 (5 W max, CW duty cycle), FT-50-43 is the right call.

### A note on the "49:1" name

The transformation ratio is (N_total / N_tap)². K6ARK's recommended
23T/3T build gives a ratio of (23/3)² = **58.8:1**, not 49:1. The
"49:1 EFHW" label is a community/historical name that's stuck even
though most field-proven designs are closer to 59:1 or 64:1. Real
EFHW feedpoint impedances run 2,800-3,500 Ω in typical installations,
which matches the higher ratios better than a textbook 49:1 (2,450 Ω).

K6ARK's range of "19-24 more turns" gives ratios from 53:1 to 81:1.
**Pick total turns based on which EFHW match impedance you're
targeting**, not based on the project folder name:

| Total turns | Ratio | Matched load | Notes |
|---|---|---|---|
| 21T (3+18 more) | 49:1 | 2,450 Ω | "True" 49:1; textbook EFHW |
| **23T (3+20 more)** | **58.8:1** | **2,940 Ω** | **K6ARK recommended, "general use"** |
| 24T (3+21 more) | 64:1 | 3,200 Ω | K6ARK image count; common alternative |
| 27T (3+24 more) | 81:1 | 4,050 Ω | High end of K6ARK's range; for elevated EFHWs |

The sim shows **all of these give identical IL** (1.40 dB at 40m on
FT-50-43) because when each is terminated in its natural matched load,
the reflected primary impedance is the same — primary inductance and
leakage inductance depend only on N_primary (= 3T), not N_total. The
choice between them is which load they present to the antenna, not
which performs better as a transformer.

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

| Variant | Unun core | Unun turns | Ratio | CMC core | CMC turns | Sim 40 m IL | Sim CMC |Z| @ 7 MHz | Weight |
|---|---|---|---|---|---|---|---|---|
| **Primary** (recommended) | **1× FT-50-43** | **3T + 20 more = 23T total** (K6ARK recommended) | **58.8:1** | **1× FT-50-43** | **12T bifilar** | **1.40 dB** | **1.93 kΩ** | **~28 g** |
| Bigger-core alternative | 1× FT-82-43 | 3T + 20 more = 23T | 58.8:1 | 1× FT-50-43 | 12T bifilar | 1.32 dB | 1.93 kΩ | ~30 g |
| Higher-ratio alt | 1× FT-50-43 | 3T + 21 more = 24T (K6ARK image count) | 64:1 | 1× FT-50-43 | 12T bifilar | 1.40 dB | 1.93 kΩ | ~28 g |
| True 49:1 | 1× FT-50-43 | 3T + 18 more = 21T | 49:1 | 1× FT-50-43 | 12T bifilar | 1.40 dB | 1.93 kΩ | ~28 g |
| Heavier-CMC | 1× FT-50-43 | 23T total | 58.8:1 | 2× FT-50-43 stacked | 12T bifilar | 1.40 dB | 3.85 kΩ | ~30 g |
| Lighter | 1× FT-50-43 | 2T + 12 more = 14T | 49:1 | 1× FT-50-43 | 9T bifilar | 2.76 dB | 1.09 kΩ | ~23 g |

**Primary is the recommended build.** 1× FT-50-43 wound 3T + 20 more
(23 turns total) is K6ARK's recommended "general use" recipe; the sim
shows 1.40 dB IL on 40 m, within 0.08 dB of the larger FT-82-43 at the
same turn count and within 0.10 dB of the bench-grade FT-240-43
reference. 12T bifilar on a single FT-50-43 gives more than 1.5 kΩ of
|Z_CM| on every band, exceeding the 1.67 kΩ that mix 31 would have
provided at 7 MHz.

**The 49:1 / 59:1 / 64:1 variants all simulate at the same 1.40 dB
IL.** That's not a coincidence: when each is matched to its natural
load (2450 / 2940 / 3200 Ω respectively), the reflected primary
impedance is identical because it depends only on the 3T primary.
Pick the variant whose load impedance best matches your EFHW
installation, not based on IL.

Pick the **bigger-core alternative** if you want thermal headroom for
a future QRO upgrade (15-25 W) or if the FT-50 winding window feels
too tight for 22 AWG.

Pick the **heavier-CMC variant** if you've had RFI issues in past
builds and want margin.

Pick the **lighter variant** only if weight is critical and you can
accept ~1.4 dB more IL on 40 m.

### Tested and rejected: 2× FT-50-43 stacked unun at 23T/3T

Stacking two FT-50-43 cores for the **unun** (keeping the K6ARK 23T/3T
recipe and the 100 pF comp cap) is *worse* than a single core, not
better. The sim output:

| Band | 1× FT-50, 23T/3T | 2× FT-50 stacked, 23T/3T |
|---|---|---|
| 40 m | 1.40 dB | 1.03 dB |
| 30 m | 1.30 dB | 1.23 dB |
| 20 m | 1.28 dB | 1.70 dB |
| 17 m | 1.40 dB | **2.43 dB** |
| 15 m | 1.60 dB | **3.16 dB** |

Why: stacking doubles Lm from ~215 μH to ~430 μH, but the 100 pF
compensation cap was tuned for the ~215 μH design point. The cap
now resonates at the wrong frequencies, and SWR climbs to 4-5:1
above 17 m.

If you do want stacked cores for thermal margin, you must retune the
comp cap (probably down to ~50-68 pF) **or** reduce turn count to bring
Lm back into the ~215 μH range. Don't stack the unun cores without
re-running the sim for your specific cap value.

(This is unun-only. The CMC stacks fine — its impedance isn't shaped
by a tuned cap, so doubling Lm just doubles |Z_CM|.)

## Acceptance Criteria

To be tested with NanoVNA H/V2 after the build is complete.

| Test | Method | Pass |
|---|---|---|
| 50 → 2940 Ω SWR | 50 Ω at BNC, **2940 Ω resistive** at radiator BP (matched load for 23T/3T = 58.8:1) | < 1.5:1 from 7-21.5 MHz |
| Insertion loss | S21 with matched terminations (50 Ω in, 2940 Ω out) | < 1 dB at 7/14/21 MHz, < 2 dB at 10/18 MHz |
| CM isolation | open-circuit one wire of bifilar pair, measure |Z| from common to single wire | > 1.5 kΩ at all KH1 band centers |
| Thermal | 5 W carrier into matched system for 5 min | core temp rise < 20 °C |
| KH1 power output | confirm 5 W into matched system on each band via MENU:VBAT | within 0.5 dB of bare-coax baseline |

**Test load construction:** 2940 Ω from parallel combinations of carbon
or metal-film resistors (1 W rating each so total dissipation handles
5 W). Two options:
- 4× 1 kΩ in parallel (= 250 Ω), then in series with 2× 1 kΩ resistors
  in parallel (= 500 Ω)... actually simpler: **2× 5.6 kΩ in parallel
  ≈ 2.8 kΩ**, or **3× 8.2 kΩ in parallel ≈ 2.73 kΩ**, or **1× 3 kΩ
  carbon-film 1%** directly. Any of these ±5% lands close enough to
  2940 Ω for the test.
- If you only have a 2,450 Ω load (true 49:1 reference), you'll see
  baseline SWR ~1.2:1 even with a perfect 23T/3T transformer because
  the load is mismatched. Either build the right load or test against
  a real EFHW.

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
