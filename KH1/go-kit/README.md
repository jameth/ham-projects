# KH1 Go Kit

Field-deployable kit centered on the Elecraft KH1 (Edgewood package),
inspired by the WD8RIF KH1 Micro Travel Kit and extended with a
20-meter-optimized stationary kit and a peak-efficiency EFHW build.

Reference: https://wd8rif.com/kh1_micro_travel_kit.htm

## Kit Philosophy

Modular three-tier wire kit plus an optional EFHW sidecar. Two short
wires cover most of the deployment scenarios; a third short wire
upgrades the kit to all-band magic-length operation; the EFHW lives
in its own pouch as an optional "max signal" add-on.

- **Core wires (always carried):** A (13') + B (16.5')
- **Option 3 add-on:** C (13' dedicated CP)
- **Option 4 sidecar:** 65'6" radiator + 9' stub + custom 49:1+CMC unit

Total kit weight target under 250 g (excluding rig). Realized weight
is ~50 g for the core wire kit + ~5 g for the Option 3 add-on +
~58 g for the EFHW sidecar = ~110 g total when bringing everything.

## The Three Wires

### Wire A: 13' silicone

| Spec | Value |
|---|---|
| Length | 13 ft (= λ/4 on 17 m) |
| Wire | 28 AWG silicone-insulated, BNTechgo or similar |
| Rig end | #4 spade lug (matches stock KH1 counterpoise) |
| Free end | banana socket (accepts B's plug for chaining) |
| Used by | Option 1 (single CP), Option 2 (CP), Option 3 (first segment of 29.5' radiator) |

### Wire B: 16.5' silicone

| Spec | Value |
|---|---|
| Length | 16.5 ft (= λ/4 on 20 m) |
| Wire | 28 AWG silicone-insulated |
| Rig end | #4 spade lug (matches stock KH1 counterpoise) |
| Free end | banana plug (mates into A's socket for chaining) |
| Used by | Option 1 (single CP, dual radial paired with A), Option 2 (radiator), Option 3 (second segment of radiator) |

### Wire C: 13' silicone (Option 3 add-on)

| Spec | Value |
|---|---|
| Length | 13 ft |
| Wire | 28 AWG silicone-insulated |
| Rig end | #4 spade lug (matches stock KH1 counterpoise) |
| Free end | knot or small eyelet (no chaining needed) |
| Used by | Option 3 (dedicated CP, since A is being used in the radiator chain) |

## Four Antenna Options

### Option 1 — Quick (Stock Whip + 1 or 2 Counterpoise Wires)

Hand-held, table-top, or pedestrian-mobile. Whip slide switch picks
the matching network position; the counterpoise(s) attach to the
rig's ground stud.

**Mode 1a — minimal (1 wire):**
- Whip + spade-lugged A (13') OR B (16.5') under the ground thumbnut
- Bands: 30/20/17/15 m (no 40 m without AXE1 or DIY loading coil)
- Best on whichever resonant band matches the wire chosen:
  - A (13') = optimal on 17 m
  - B (16.5') = optimal on 20 m
- Deploy time: < 30 sec
- Weight added: ~4 g (single wire)

**Mode 1b — dual radial (slight boost):**
- Whip + both A and B clipped to the ground stud, fanned ~90° apart
- Resonant on **both** 17 m (via A) and 20 m (via B)
- ~1-1.5 dB improvement vs single radial on each band
- Pattern leans slightly toward the bisector of the two wires
- Deploy time: ~45 sec
- Weight added: ~7 g (both wires)

Note: this is a deliberate trade away from the 4×16.5' radial setup.
You give up the 3 dB peak gain that 4 same-length radials produce on
one band, but you gain dual-band (17 m + 20 m) resonance coverage
with half the wire.

Build sheet: `../counterpoise-wire-kit/`

### Option 2 — Compact 20 m (Short EFRW, Direct BNC)

Tight cover, urban, hotel rooms, dense brush, anywhere you can't
sling a long wire. Optimized for 20 m primary.

| Spec | Value |
|---|---|
| Radiator | Wire B (16.5'), spade lug on BNC binding post |
| Counterpoise | Wire A (13'), spade lug on ground binding post |
| Connection | BNC-to-binding-post adapter, no transformer |
| Bands | 20 m primary; 17/15 m good; 30 m marginal |
| Why no 9:1? | At ~λ/4 on 20 m, the wire is low-Z; a 9:1 transforms wrong direction. KH1 ATU handles direct connection. |
| Weight added | 0 g (both wires already in core kit) |

The 16.5' wire deployed vertically, as a sloper, or as an inverted-vee
acts as a near-resonant λ/4 vertical with a single counterpoise radial.
Very efficient for the size.

Build sheet: `../short-efrw-kit/`

### Option 3 — Multi-Band Magic Length (Chained Wires, Direct BNC)

Tree-supported deployment covering all five KH1 bands with a single
chained-wire radiator. No transformer.

| Spec | Value |
|---|---|
| Radiator | A (13') + B (16.5') chained = **29.5'** total |
| Connection at chain joint | A's free banana socket × B's banana plug |
| Counterpoise | Wire C (13'), spade lug on ground binding post |
| Connection at rig | A's spade lug on BNC binding post |
| Bands | All 5 KH1 bands; 29.5' is non-resonant on every band (essentially same as 29' magic length) |
| No fold-back needed | 29.5' is already off λ/2 everywhere; simpler than WD8RIF's 29/33/35 three-position scheme |
| Weight added | ~5 g (wire C only; A and B already in core kit) |

29.5' band-by-band electrical position:

| Band | Electrical | Behavior |
|---|---|---|
| 40 m | 0.22 λ | short cap, ATU likes it |
| 30 m | 0.31 λ | mid-Z |
| 20 m | 0.44 λ | well off both λ/4 and λ/2 |
| 17 m | 1.09 × λ/2 | just past peak, mid-Z |
| 15 m | 0.63 λ | between λ/2 and 3λ/4, mid-Z |

Build sheet: `../micro-travel-kit/`

### Option 4 — Maximum Efficiency (65'6" EFHW + 49:1 + CMC)

Stationary deployment where peak signal matters. Highest efficiency
configuration in the kit. Lives in its own sidecar pouch and is
brought as an **optional** add when the trip warrants it.

| Spec | Value |
|---|---|
| Radiator | 65'6" 26 AWG silicone wire, trimmed to actual 7.05 MHz null with NanoVNA |
| Counterpoise | 9 ft stub at the unun cold side |
| Matching unit | Custom integrated 49:1 unun (FT-82-43, 21T/3T, K6ARK config) + 1:1 CMC (FT-50-43, 12T bifilar) |
| Comp cap | 100 pF NP0 1.5 kV across the unun's 21T winding |
| Connection | BNC at the unun, dual binding posts for radiator and CP |
| Bands | All 5 KH1 bands; resonant on 40/20/15 (3 of 5); ATU-tunable on 30/17 |
| Sim performance | < 1.5 dB IL on resonant bands; > 1.5 kΩ |Z_CM| across all KH1 bands |
| Weight | ~58 g total (matching unit ~35 g + wires ~23 g) |

This is the "build it" project of the kit. See `../efhw-portable/`
for design, simulation, BOM, build instructions, and acceptance tests.

## Decision Tree

```
Start
  │
  ├─ Hand-held / table-top, fast deploy?
  │     ├─ Minimal carry → Option 1a (whip + 1 wire)
  │     └─ Want a boost  → Option 1b (whip + 2 wires)
  │
  ├─ Tight space, 20 m primary?
  │     → Option 2 (16.5' EFRW direct)
  │
  ├─ Tree or mast available?
  │     ├─ Light kit, all bands → Option 3 (29.5' chained EFRW direct)
  │     └─ Brought the EFHW sidecar, want max signal → Option 4
  │
  └─ 40 m specifically required?
        → Option 3 or Option 4 (Option 1/2 lack 40 m without AXE1)
```

## Connection Mechanics

The wire termination scheme is consistent and field-proof:

- **#4 spade lug at the rig end** of every wire — matches the factory
  KH1 counterpoise. Universal connection: slips under the ground
  thumbnut (Option 1) or under a 5-way binding post on the BNC adapter
  (Options 2, 3).
- **Asymmetric chaining termination** on A and B: A has a banana socket,
  B has a banana plug. They mate in only one direction, preventing
  reversed connections in the field.
- **Wire C** has just a spade lug + knot, since it doesn't need to chain.

For Option 1 dual-radial mode, both spade lugs stack under the ground
thumbnut. Loosen the thumbnut, slip both forks around the 4-40 stud,
retighten. Pre-stack at home if you're committing to dual-radial mode
for the trip.

Tradeoff vs alligator clips: spade lugs need the thumbnut loosened
(~15 sec deploy) but are lighter (~0.5 g vs ~3 g per termination),
more reliable (no spring fatigue), match factory consistency, and
fit any 5-way binding post.

## Complete Kit Contents and Weights

### Core kit (always carried)

| Item | Qty | Weight |
|---|---|---|
| Wire A (13' silicone, spade lug + banana socket) | 1 | ~3 g |
| Wire B (16.5' silicone, spade lug + banana plug) | 1 | ~4 g |
| BNC-to-binding-post adapter | 1 | ~5 g |
| Tufteln-style winder for A and B | 1 | ~10 g |
| **Core subtotal** | | **~22 g** |

### Option 3 add-on (carried for tree-supported activations)

| Item | Qty | Weight |
|---|---|---|
| Wire C (13' silicone, spade lug + knot) | 1 | ~3 g |
| Small winder | 1 | ~5 g |
| **Add-on subtotal** | | **~8 g** |

### Option 4 EFHW sidecar (optional bring)

| Item | Qty | Weight |
|---|---|---|
| 65'6" EFHW radiator (26 AWG silicone) | 1 | ~20 g |
| 9' EFHW CP stub | 1 | ~3 g |
| Custom 49:1 + CMC matching unit | 1 | ~35 g |
| Larger winder for radiator | 1 | ~15 g |
| Sidecar pouch | 1 | ~20 g |
| **Sidecar subtotal** | | **~93 g** |

### Carry pouches and misc

| Item | Qty | Weight |
|---|---|---|
| Main carry pouch (Maxpedition or similar) | 1 | ~30 g |
| **Total kit (core + Opt 3 + sidecar + pouch)** | | **~155 g** |

Well under the 250 g target. Trips that don't need the EFHW save ~93 g.

## Optional Variants (Pending Field Testing)

### 20 m-Optimized 4-Radial Variant

For operators whose 20 m time dominates (>70% of operating). Trades
some 17 m efficiency for a substantial 20 m boost via 4× same-length
resonant radials.

**Kit changes vs the standard 3-wire kit:**

| Component | Standard kit | 20 m-optimized variant |
|---|---|---|
| Wire A | 13' (17 m λ/4) | 16.5' (20 m λ/4) |
| Wire B | 16.5' | 16.5' |
| Wire C | 13' | 16.5' |
| Wire D (new) | not present | 16.5' (additional 4th radial) |
| Wire E (extension) | not present | 2' wire with banana hardware (enables 35' chain in Option 3 to dodge 20 m λ/2 dead zone) |

All four short wires become identical 16.5' lengths. The 2' extension
wire is optional but restores Option 3 multi-band capability on 20 m
(without it, the chained 33' radiator sits on 20 m λ/2 and the ATU
can't match).

**New capability (Option 1c — quad-radial whip):**

Stack all four 16.5' spade lugs under the ground thumbnut. Fan the
radials at 90° intervals on the ground. The whip + 4× resonant
radials approaches true ground-plane behavior on 20 m.

Theoretical gain on 20 m: **+3 dB over single radial**, or
**+6 dB over no radial** (factory whip alone). Roughly 1.5 S-units
of audible improvement.

**Trade-offs vs standard kit:**

| Band | Standard kit (mixed lengths) | 20 m-optimized (all 16.5') |
|---|---|---|
| 20 m | up to +5 dB | **up to +8 dB** (Option 1c quad-radial) |
| 17 m | up to +5 dB (resonant CP) | +3 dB (no resonant wire) |
| 15 m | +3 dB | +2.5 dB |
| 30 m | +1 dB | +1.5 dB |
| 40 m | unchanged (needs Option 3 or 4) | unchanged |

Net: ~+3 dB on 20 m (best case, Option 1c), ~-2 dB on 17 m, marginal
elsewhere. Good trade if 20 m is dominant; bad trade if you split
time across bands.

### Test Plan Before Committing

Validate the +3 dB theoretical gain with on-air measurement before
restructuring the kit.

**Test procedure:**

1. Same QTH (open field or activation site), same operating session
2. Same hour, same band (20 m)
3. KH1 set to identical power, sidetone, filter settings
4. Send a CQ identifier on a clear frequency 5-10 times with each
   configuration; let RBN spot you
5. Compare RBN-skimmer-reported SNR averages across configurations

**Configurations to test:**

| # | Configuration | Hypothesis |
|---|---|---|
| 1 | Whip + 1× 16.5' radial | baseline (current Option 1a) |
| 2 | Whip + 2× 16.5' radials | should show +1.5 dB over #1 |
| 3 | Whip + 4× 16.5' radials | should show +3 dB over #1 (the variant's payoff) |
| 4 | Whip alone, no radial | reference floor |
| 5 | Option 2 (1× 16.5' rad + 1× 13' CP on BNC) | reference for wire-vs-whip comparison |

**Decision criteria:**

- If #3 shows ≥ +2 dB over #1: commit to the variant
- If #3 shows < +2 dB over #1 (ground losses, body capacitance dominating, or measurement noise): stay with standard 3-wire kit
- Document results in `../measurements/` (TBD subfolder)

The body capacitance question is the most likely complication: when
hand-held pedestrian-mobile, the operator's body provides much of the
ground reference, so the marginal benefit of additional radials may
shrink. Stationary table-top tests should show closer to theoretical
gain.

## Deployment Recipes

See `deployment-guide.md` for step-by-step field setup of each option.

## Project Subfolders

- `../efhw-portable/` — Option 4 build (active, design + sim done)
- `../counterpoise-wire-kit/` — Wires A + B build sheet (Options 1, 2)
- `../micro-travel-kit/` — Wire C build sheet + Option 3 chaining notes

## References

- WD8RIF KH1 Micro Travel Kit: https://wd8rif.com/kh1_micro_travel_kit.htm
- KH1 Owner's Manual rev B7 (in parent folder)
- KH1 Programmer's Reference rev B2 (in parent folder)
- `../community-research-2026-05.md` — Gemini deep research synthesis
- `../operating-cheat-sheet.md` — field operating reference
