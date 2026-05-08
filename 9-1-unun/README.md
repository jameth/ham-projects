# 9:1 Unun for End-Fed Random Wire Antenna

## Design Goals

- Transform ~450 ohms (end-fed random wire feedpoint) to 50 ohms (coax)
- Broadband operation across 80m-10m (3.5-30 MHz)
- Low insertion loss (<0.5 dB across the operating range)
- Power handling: 100 W SSB
- Use available materials: FT-240-43/31 toroids, epoxy-coated magnet wire,
  SO-239 connectors, project boxes

## Theory of Operation

### Why 9:1?

An end-fed random wire antenna presents a high feedpoint impedance that varies
widely with frequency and wire length. While theoretically the impedance could
be anywhere from a few hundred to several thousand ohms, a 9:1 impedance
transformation provides a reasonable compromise, mapping the ~200-800 ohm
range down to ~22-89 ohms — close enough to 50 ohms for most tuners to handle
on bands where the wire isn't resonant.

The "9:1" refers to the impedance ratio. Since impedance scales as the square
of the voltage ratio, a 9:1 unun is a **3:1 voltage** autotransformer.

### Unun vs Balun

- **Balun** (balanced-to-unbalanced): connects a balanced antenna (dipole) to
  unbalanced feedline (coax)
- **Unun** (unbalanced-to-unbalanced): both sides are unbalanced — a random
  wire against a ground/counterpoise is unbalanced, and coax is unbalanced

This is an unun because neither the antenna wire nor the coax is balanced.

### Autotransformer Principle

A 9:1 unun uses a **trifilar autotransformer** — three identical windings
connected in series. The coax (50-ohm side) taps across the first winding,
while the antenna (450-ohm side) connects across all three windings in series.

```
                    Winding 1       Winding 2       Winding 3
                  ┌───WWWW───┬───WWWW───┬───WWWW───┐
                  │           │           │           │
   Ground ────────┤           │           │           ├──── Antenna (450 Ω)
   (counterpoise) │           │           │           │
                  │           │           │           │
   Coax center ───┘           │           │           │
   (50 Ω)      start W1    end W1     end W2      end W3
                            =start W2  =start W3

   All three windings are on the SAME ferrite core (trifilar wound).
   They share magnetic coupling, so voltage divides equally.
```

Each winding carries 1/3 of the total voltage. The 50-ohm tap sees 1/3 the
voltage and 3x the current of the full winding — that's a 3:1 voltage ratio
and therefore 9:1 impedance ratio.

Because all three wires pass through the core together, the magnetic coupling
between them is very tight, and the transformer works across a wide bandwidth
as long as the magnetizing inductance is adequate.

### Magnetizing Inductance Requirement

For the transformer to work properly, the magnetizing inductance (Lm) must be
high enough that its reactance is much larger than the load impedance at the
lowest operating frequency. The rule of thumb:

    X_Lm > 4 × Z_load  (at the lowest frequency)

For 450 ohms at 3.5 MHz (80m):

    X_Lm > 4 × 450 = 1800 Ω
    Lm > 1800 / (2π × 3.5 MHz) = 81.9 μH

If the magnetizing inductance is too low, the core shunts too much current
and insertion loss increases sharply at the low end.

## Core Selection

### FT-240-43 (Mix 43) — Recommended for Unun Transformers

| Parameter              | Value             |
|------------------------|-------------------|
| Initial permeability   | ~800              |
| AL (low-freq)          | ~575 nH/turn²     |
| Optimal frequency      | 10-250 MHz        |
| Loss characteristic    | Lower loss than mix 31 at HF |

**Mix 43 is the standard choice for broadband HF transformers.** Unlike a
common-mode choke (where loss is desirable to absorb CM energy), a transformer
passes signal power through the core. Lower core loss means less heating and
better efficiency. Mix 43 has adequate permeability for 80m-10m operation with
12+ turns while keeping loss manageable.

| Turns (trifilar) | Lm (approx) | X_Lm at 3.5 MHz | 80m Margin |
|-------------------|-------------|------------------|------------|
| 10                | 57.5 μH     | 1265 Ω           | Marginal   |
| 12                | 82.8 μH     | 1821 Ω           | Adequate   |
| 14                | 112.7 μH    | 2479 Ω           | Good       |

### FT-240-31 (Mix 31) — Usable, Higher Loss

| Parameter              | Value             |
|------------------------|-------------------|
| Initial permeability   | ~1500             |
| AL (low-freq)          | ~1075 nH/turn²    |
| Optimal frequency      | 1-30 MHz          |
| Loss characteristic    | Higher loss (more lossy material) |

Mix 31's higher permeability means fewer turns are needed for adequate
magnetizing inductance. However, the higher loss factor (μ'') means more
signal power is dissipated as heat in the core. This is fine at QRP levels
but becomes a concern above 50-100 W.

| Turns (trifilar) | Lm (approx) | X_Lm at 3.5 MHz | 80m Margin |
|-------------------|-------------|------------------|------------|
| 8                 | 68.8 μH     | 1513 Ω           | Marginal   |
| 10                | 107.5 μH    | 2365 Ω           | Good       |
| 12                | 154.8 μH    | 3405 Ω           | Excellent  |

**Tradeoff summary:** Mix 31 needs ~2 fewer turns for equivalent low-band
performance, but converts more of your signal to heat. For 100 W SSB, mix 43
is preferred. For QRP (<10 W), either works fine.

## Design Variants

---

### Design A: Trifilar on FT-240-43, 12 Turns (Recommended)

**The standard broadband 9:1 unun build.**

#### Specifications

| Parameter         | Value                              |
|-------------------|------------------------------------|
| Core              | 1x FT-240-43                      |
| Winding           | 12 turns trifilar                  |
| Wire              | 18-16 AWG epoxy-coated magnet wire |
| Lm (approx)       | 82.8 μH                           |
| Connectors        | 1x SO-239 (coax side), binding post or lug (antenna) |
| Enclosure         | Project box                        |
| Power rating      | 100 W SSB / 50 W continuous        |

#### Construction

**Step 1: Prepare the trifilar bundle**

Cut three equal lengths of 18 AWG epoxy-coated magnet wire, each
approximately **85 cm (33")** — 100 cm (40") if you want comfortable
tails. Each wire needs to cover 12 turns around the FT-240 cross-section
(~55 mm per turn) plus 5–8 cm of lead at each end for the series
interconnections and terminal solder joints.

Twist the three wires together loosely — about 1–2 twists per inch.
A hand drill with one end chucked works well: clamp the far end in a
vise, hand-feed, and spin gently. This keeps the wires together and
ensures tight magnetic coupling. Alternatively, lay them flat
side-by-side and secure with tape at each end (ribbon-wound, slightly
better high-band performance but stiffer to wind).

**Why twist/bundle at all?** Not for core flux — every wire through the
core hole links the same core flux regardless of position. The bundle
matters for: (1) minimizing leakage inductance *between* the three
windings (the main reason — controls high-end rolloff), (2) setting
the characteristic impedance of the trifilar "transmission line"
(~50–100 Ω depending on twist tightness), (3) keeping the wires
ordered so you don't accidentally cross one and reverse its polarity.

Tip: Use a marker or nail polish to mark one wire at each end so you can
identify individual wires after winding. Call them W1, W2, W3.

```
    W1: ─────────────── (marked with dot at each end)
    W2: ───────────────
    W3: ───────────────
         twisted together as a bundle
```

**Step 2: Wind the core**

Pass the trifilar bundle through the FT-240-43 toroid **12 times**. Each
pass through the center hole is one turn. Distribute the turns evenly around
the core, covering approximately 270-300 degrees (leave a gap between the
entry and exit leads).

```
         ╭───────────╮
        ╱  FT-240-43  ╲
       │   12 turns     │
       │   trifilar     │
        ╲  bundle      ╱
         ╰─────────────╯
        ↑gap↑
     3 wires in    3 wires out
```

**Step 3: Identify and connect the windings**

This is the most critical step. Getting the connections wrong will result in
a dead short, no transformation, or the wrong ratio.

Strip and tin all 6 wire ends (3 starts, 3 ends). Use a multimeter in
continuity mode to trace each wire from start to finish. Label them:

```
    Start side:  W1s  W2s  W3s
    End side:    W1e  W2e  W3e
```

Make the following connections:

```
    SERIES CONNECTIONS (solder these pairs together):
    ─────────────────────────────────────────────────
    W1e ──── W2s    (end of winding 1 to start of winding 2)
    W2e ──── W3s    (end of winding 2 to start of winding 3)

    TERMINAL CONNECTIONS:
    ─────────────────────
    W1s ──── Ground / SO-239 shell / counterpoise lug
    W1e/W2s junction ──── SO-239 center pin (50 Ω tap)
    W3e ──── Antenna terminal (450 Ω)
```

**Schematic:**

```
                        Core
              ┌─────────────────────────┐
              │                         │
    GND ──── W1s ═══W1═══ W1e─┬─W2s ═══W2═══ W2e─┬─W3s ═══W3═══ W3e ──── ANT
              │                │                   │                        (450Ω)
              │                │                   │
              │          50 Ω tap                   │
              │          (SO-239                    │
              │           center)                   │
              │                                     │
              └─────────────────────────────────────┘
                    ═══ = wound on ferrite core (all 3 together)
```

**Step 4: Verify before enclosing**

With a multimeter, verify:
- Continuity from GND → 50 Ω tap (through W1) — should read near 0 Ω
- Continuity from 50 Ω tap → ANT terminal (through W2 + W3) — should read
  near 0 Ω
- Continuity from GND → ANT terminal (through all three) — should read
  near 0 Ω
- **No continuity** between any wire and the core itself

**Step 5: Mount in enclosure**

- Mount the SO-239 on one side of the project box
- Use a bolt-through binding post, wing nut, or stainless steel lug for the
  antenna wire terminal on the opposite side (or top)
- Add a second ground terminal/lug for the counterpoise wire
- Secure the toroid with hot glue or RTV silicone
- Keep leads short to minimize stray inductance

```
    ┌─────────────────────────────────┐
    │                                 │
    │   [ANT post]    [GND lug]      │
    │        │            │           │
    │        │   ╭────╮   │           │
    │        └───│core│───┘           │
    │            ╰──┬─╯               │
    │               │                 │
    │          [SO-239]               │
    │                                 │
    └─────────────────────────────────┘
         coax to shack ↓
```

---

### Design B: Trifilar on FT-240-31, 10 Turns

**Fewer turns, adequate for QRP, slightly higher loss at power.**

#### Specifications

| Parameter         | Value                              |
|-------------------|------------------------------------|
| Core              | 1x FT-240-31                      |
| Winding           | 10 turns trifilar                  |
| Wire              | 18-16 AWG epoxy-coated magnet wire |
| Lm (approx)       | 107.5 μH                          |
| Power rating      | 50 W SSB / 25 W continuous         |

#### Construction

Identical to Design A except:
- Use the FT-240-31 core instead of FT-240-43
- Wind 10 turns instead of 12 (the higher permeability compensates)

#### When to choose this design
- You want to save your FT-240-43 cores for another project
- Operating at QRP power levels (<10 W) where core loss is negligible
- You want the best possible 160m/80m performance (the higher Lm helps)

#### Caution
At 100 W continuous-duty modes (FT8, RTTY), the mix 31 core will run warm
to hot. At 100 W SSB (lower duty cycle), it's manageable but will still be
warmer than mix 43. Touch-test the core after a long transmission — if it's
too hot to touch, reduce power or switch to Design A.

---

### Design C: Trifilar on Stacked 2x FT-240-43, 10 Turns

**Higher power handling, lower core temperature.**

#### Specifications

| Parameter         | Value                              |
|-------------------|------------------------------------|
| Core              | 2x FT-240-43 (stacked)            |
| Winding           | 10 turns trifilar                  |
| Wire              | 18-16 AWG epoxy-coated magnet wire |
| Lm (approx)       | 115 μH (doubled Ae)               |
| Power rating      | 200 W SSB / 100 W continuous       |

#### Construction

Same as Design A, but:
- Stack two FT-240-43 cores, tape them together
- Wind 10 turns through both cores as a unit
- The doubled cross-section reduces flux density for any given power level,
  which means lower core heating and higher power handling

#### When to choose this design
- Running 100 W+ continuous-duty digital modes
- Portable/field use where you can't monitor core temperature
- You want the most robust, worry-free build

---

## Counterpoise / Ground

**A 9:1 unun for a random wire REQUIRES a counterpoise.** Without it, RF
current has no return path except through your coax shield (defeating
the purpose) or your station ground (causing RFI).

### Core rule

**The counterpoise length must be different from the antenna length**
— and different from any `n·λ/2` multiple on your operating bands. If
the counterpoise and antenna happen to be the same length, you've
inadvertently built an off-center-fed dipole with an odd feed impedance.

### Counterpoise options

1. **Single radial wire:** 0.05–0.1 wavelength at your lowest operating
   frequency, laid on the ground or slightly elevated. For 80m: ~4–8 m
   (13–26 ft). A **17 ft counterpoise** is the simplest broadband starting
   point that works with every antenna length below.

2. **Multiple radials:** 2–4 radials of different lengths (avoiding
   multiples of each other) give better pattern and lower RX noise.

3. **Tuned counterpoise:** A quarter-wave wire for your primary
   operating band. For 40m: ~10 m (33 ft). For 20m: ~5 m (16.5 ft).

### Pairing table — counterpoise to antenna length

| Antenna length | Suggested counterpoise                |
|----------------|----------------------------------------|
| 29 ft          | 17 ft or 25 ft                        |
| 41 ft          | 17 ft or 25 ft or 33 ft              |
| 58 ft          | 17 ft + 25 ft (two radials)          |
| 84 ft          | 17 ft + 25 ft + 33 ft (three radials)|
| 107 ft         | 33 ft + 50 ft (two radials)          |
| 124 ft         | 33 ft + 50 ft + 65 ft (three radials)|

Rule of thumb: **more radials = better pattern and lower noise floor**,
with diminishing returns after ~4–6. For portable use, a single 17 ft
counterpoise is a reasonable compromise; for a permanent install, lay
down as many as your site allows.

Connect the counterpoise wire(s) to the GND terminal of the unun (same
point as the SO-239 shell / W1s connection).

### Common-mode choke

**Strongly recommended:** Place a common-mode choke (see the `../common-mode-choke/`
project) on the coax immediately after the unun. Even with a good counterpoise,
some common-mode current will flow on the coax shield. The choke isolates the
feedline from the antenna system.

```
    [Random wire] ──── [9:1 Unun] ──── [CM Choke] ═══coax═══ [Radio]
                          │
                    [Counterpoise]
```

## Wire Length Selection

For a "random wire" antenna to work well across multiple bands, the wire
length should **avoid** being a half-wavelength (or multiple) on any
desired band. At `n·λ/2`, end-fed impedance rockets to several thousand
ohms — even a good tuner can't match it and the 9:1 alone can't tame it.

These "magic lengths" keep feedpoint impedance mostly in the
**200–800 Ω** range across HF, which the 9:1 maps to **22–89 Ω** —
well within tuner range on every band marked good.

### Magic random wire lengths

| Length (ft)  | Length (m) | 160m | 80m | 40m | 30m | 20m | 17m | 15m | 12m | 10m |
|--------------|------------|:----:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **29 ft**    | 8.84 m     |  —   |  ✗  |  ✓  |  ✓  |  ✓  |  ✗  |  ✓  |  ✗  |  ✓  |
| **35.5 ft**  | 10.82 m    |  —   |  ✓  |  ✗  |  ✓  |  ✗  |  ✓  |  ✗  |  ✓  |  ✗  |
| **41 ft**    | 12.50 m    |  —   |  ✓  |  ✓  |  ✓  |  ✓  |  ✗  |  ✓  |  ✗  |  ✓  |
| **58 ft**    | 17.68 m    |  —   |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✗  |  ✓  |  ✓  |
| **71 ft**    | 21.64 m    |  —   |  ✗  |  ✗  |  ✓  |  ✗  |  ✓  |  ✗  |  ✓  |  ✓  |
| **84 ft** 🏆 | 25.60 m    |  ~   |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| **107 ft**   | 32.61 m    |  ✓   |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✗  |  ✓  |
| **124 ft**   | 37.80 m    |  ✓   |  ✓  |  ✓  |  ✗  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |

✓ = tuner should handle it (SWR typically < 10:1 at the 9:1 output)
✗ = near `n·λ/2` — impedance spikes, avoid
~ = marginal, may load with a capable tuner

### Top picks

- **84 ft (25.6 m) — the best all-rounder.** Clean on every HF band from
  80m through 10m, marginal on 160m. If your yard fits it, build this one.
- **41 ft (12.5 m) — the compact standard.** Fits most suburban lots.
  Covers 80m–10m with weak spots only on 17m and 12m.
- **58 ft (17.7 m) — the classic LNR length.** 80m–10m with 15m as the
  only weak spot. Good middle-ground choice.
- **107 ft or 124 ft — if you want 160m** and have the real estate.
- **29 ft (8.8 m) — tight spaces.** Skip 80m, good 40m up.

### Reference: λ/2 multiples to avoid

| Band | λ/2 (ft) | Stay away from (ft)     |
|------|----------|-------------------------|
| 80m  | 140.6    | 140, 281                |
| 40m  | 70.3     | 70, 141, 211            |
| 30m  | 48.7     | 49, 97, 146             |
| 20m  | 34.9     | 35, 70, 105, 140        |
| 17m  | 27.2     | 27, 54, 82, 109         |
| 15m  | 23.2     | 23, 46, 70, 93, 116     |
| 12m  | 19.8     | 20, 40, 59, 79, 99, 119 |
| 10m  | 17.3     | 17, 35, 52, 69, 87, 104 |

If your yard dictates the length, pick the longest that fits, then
check it against this table. Lengths within ~6% of any value are
likely to have problems on that band.

*These numbers assume free-space wavelength; real-world performance
shifts 5–10% with wire height, ground conductivity, and nearby objects.*

## Verification and Testing

### With a NanoVNA

1. **Impedance ratio test:** Terminate the antenna port with a 450-ohm
   non-inductive resistor (or a series combination of standard resistors,
   e.g., 390 + 56 = 446 Ω). Measure S11 at the SO-239 port — it should
   show close to 50 ohms (SWR < 1.5:1) across the HF range.

2. **Insertion loss:** With the 450-ohm termination, measure S21 through the
   transformer. Loss should be < 0.5 dB across 80m-10m for Design A.

3. **Magnetizing inductance:** With the antenna port open, measure the
   impedance at the SO-239 port. At low frequencies, this will appear as
   an inductance. It should match the calculated Lm from the design table.

### On the air

- Connect your random wire and counterpoise
- Check SWR with your tuner across bands
- The unun itself doesn't make the SWR 1:1 — it gets the impedance into a
  range your tuner can handle (typically < 10:1 SWR)
- If you have persistent high SWR on a specific band, try adjusting the
  wire length by a meter or two

## Files in This Project

- `bom.md` — Bill of materials for each design
- `simulations/unun_performance.py` — Python script to model performance
- `measurements/` — Place NanoVNA exports and photos here after construction
