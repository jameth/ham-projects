# 49:1 Unun for End-Fed Half-Wave (EFHW) Antenna

## Design Goals

- Transform ~2450 ohms (EFHW feedpoint) to 50 ohms (coax)
- Operate on a fundamental band and its harmonics (e.g., 40m fundamental
  → 20m, 15m, 10m)
- Low insertion loss (<0.5 dB on the design bands)
- Power handling: 100 W SSB
- Use available materials: FT-240-43/31 toroids, epoxy-coated magnet wire,
  SO-239 connectors, project boxes

## Theory of Operation

### Why 49:1?

A half-wave dipole has a feedpoint impedance of ~73 ohms at its center. But
if you feed it at the **end** instead, the voltage is at a maximum and the
current is at a minimum — the impedance is very high, theoretically
approaching infinity for an ideal thin conductor.

In practice, a real end-fed half-wave antenna presents roughly **2000-5000 ohms**
at the feedpoint, depending on wire diameter, height, ground proximity, and
exact resonant frequency. A 49:1 transformation maps this range:

    2450 Ω / 49 = 50 Ω (ideal case)
    2000 Ω / 49 = 40.8 Ω → SWR ≈ 1.2:1
    5000 Ω / 49 = 102 Ω → SWR ≈ 2.0:1

This is a much better match than trying to feed several thousand ohms directly
into a 50-ohm coax.

### EFHW vs Random Wire

| Property           | EFHW (49:1)                        | Random Wire (9:1)            |
|--------------------|------------------------------------|------------------------------|
| Wire length        | Resonant (½λ or multiples)         | Non-resonant (arbitrary)     |
| Tuner required     | Often not needed on design bands   | Almost always needed         |
| Bandwidth          | Narrower (resonant antenna)        | N/A (tuner handles it)       |
| Harmonic operation | Yes — ½λ at 40m = 1λ at 20m, etc. | Works on any band with tuner |
| Feedpoint Z        | ~2000-5000 Ω (predictable)         | ~200-5000 Ω (varies wildly)  |
| Counterpoise       | Short (~0.05λ) or none needed      | Required                     |

The EFHW is a more elegant system when you want specific-band operation
without a tuner. The tradeoff is that the wire length must be carefully cut
to resonance.

### Autotransformer: 7:1 Voltage = 49:1 Impedance

A 49:1 unun is a **7:1 voltage** autotransformer. There are two common
winding approaches:

#### Method 1: Heptafilar (7 wires) — Theoretically Ideal, Impractical

Seven wires wound together, connected in series. This is the "pure"
autotransformer approach but is extremely difficult to wind and manage
on a toroid. **Not recommended.**

#### Method 2: Two-Winding Autotransformer — Standard Approach

Use two windings: a **primary** (small, N turns) and a **total winding**
(large, 7N turns). The primary is wound as part of the total winding.

In practice, this is built as:
- **Winding A:** 3 turns (the 50-ohm tap section)
- **Winding B:** 21 turns total (the full winding, which includes the
  3 turns of A within it — effectively 3 + 18 additional turns)

Wait — let's be precise. For a 7:1 voltage ratio autotransformer:

```
    Total turns: 7N (entire winding from GND to antenna)
    Tap point:   N turns from GND (the 50-ohm connection)

    Voltage ratio: 7N / N = 7:1
    Impedance ratio: 7² = 49:1
```

The standard practical build uses a **bifilar winding** where:
- Wind 2 wires together as a bifilar pair, N turns
- One wire becomes the "bottom" section (GND to 50-ohm tap)
- The other wire connects in series above it (50-ohm tap to midpoint)
- Then a single wire continues for the remaining turns to reach 7N total

**But the most common EFHW transformer approach is simpler:**

#### The Standard EFHW 49:1 Build (2-winding method)

Wind a **primary** of 2 turns and a **secondary** of 14 turns on the same
core. Connect them as an autotransformer with the primary tapped into the
bottom of the secondary.

```
    Primary:   2 turns  (connected from GND to 50 Ω tap)
    Secondary: 14 turns (connected from GND to antenna terminal)

    The primary is wound OVER or THROUGH the same core as the secondary,
    providing tight coupling.

    Voltage ratio: 14 / 2 = 7:1
    Impedance ratio: 7² = 49:1
```

Actually, the most widely-used and proven approach is even simpler — a
**single tapped winding**:

### Recommended: Tapped Autotransformer

```
    Total winding: 14 turns of magnet wire on the toroid
    Tap at: 2 turns from the ground end

                     2 turns        12 more turns
    GND ────────── ═══════ ──┬── ═══════════════════════════ ──── ANT
                              │                                   (2450 Ω)
                         50 Ω tap
                        (SO-239 center)

    ═══ = turns on ferrite core (single continuous winding)
```

This is the simplest, most reliable, and most commonly used configuration.
The 50-ohm tap is at 2 turns, the antenna connects to the end at 14 turns.
Ratio: (14/2)² = 49:1.

**Key insight:** Unlike the 9:1 unun (which uses a trifilar winding for tight
coupling), the 49:1 can use a single tapped winding because:
1. The coupling between the 2-turn and 14-turn sections is inherently tight
   since they share the same core
2. The bifilar technique would require 7 wires, which is impractical
3. The single-winding approach is proven in thousands of EFHW builds

### Adding a Compensation Capacitor

EFHW transformers often benefit from a small capacitor (100-150 pF) across
the 50-ohm winding (from the tap to ground). This compensates for leakage
inductance and parasitic effects, improving SWR on the higher bands.

```
    GND ──────┬── ═══ ──┬── ═══════════════════════ ──── ANT
              │          │
              ├── [C] ───┤
              │  100pF    │
              │       50 Ω tap
           SO-239 shell
```

The exact value is determined empirically — start with 100 pF and adjust
by measuring SWR across your target bands. This is one of the key tuning
steps during construction.

### Magnetizing Inductance Requirement

For the 49:1 transformer, the magnetizing inductance requirement is based
on the full (14-turn) winding and the high-impedance load:

    X_Lm > 4 × Z_load (at lowest frequency)

For 2450 ohms at 7 MHz (40m, typical lowest EFHW band):

    X_Lm > 4 × 2450 = 9800 Ω
    Lm > 9800 / (2π × 7 MHz) = 222.8 μH

This is a much more demanding requirement than the 9:1 unun. The 14-turn
winding must provide enough inductance to avoid excessive shunt current
through the core.

## Core Selection

### FT-240-43 (Mix 43) — Recommended

| Turns | Lm (approx) | X_Lm at 7 MHz | 40m Margin |
|-------|-------------|----------------|------------|
| 14    | 112.7 μH    | 4955 Ω         | Marginal (~2× Z_load, want 4×) |
| 16    | 147.2 μH    | 6471 Ω         | Better (~2.6× Z_load) |
| 18    | 186.3 μH    | 8190 Ω         | Good (~3.3× Z_load) |

With a single FT-240-43, 14 turns is the practical minimum for 40m operation.
The margin is tight — the magnetizing reactance is only ~2× the load impedance
rather than the ideal 4×. This means some additional loss on 40m, but it's
manageable because:
1. The actual feedpoint impedance may be lower than 2450 Ω
2. The compensation capacitor helps
3. Many successful EFHW builds use 14 turns on a single FT-240-43

For better 40m performance, stack two cores (Design C below).

### FT-240-31 (Mix 31) — Higher Permeability, Higher Loss

| Turns | Lm (approx) | X_Lm at 7 MHz | 40m Margin |
|-------|-------------|----------------|------------|
| 14    | 210.7 μH    | 9261 Ω         | Good (~3.8× Z_load) |
| 12    | 154.8 μH    | 6805 Ω         | Better than 43 w/ 14T |

Mix 31 provides more inductance per turn, giving better 40m margin. However,
the higher loss dissipates more signal power. At 100 W, core heating is a
real concern in a 49:1 transformer because the current in the 2-turn primary
is high.

**Core dissipation warning:** In a 49:1 transformer at 100 W, the primary
carries ~2 A peak current. The core loss from this current flowing through
the magnetizing impedance can be several watts. Mix 31 will dissipate roughly
2× more power than mix 43 at the same operating point.

## Design Variants

---

### Design A: Single FT-240-43, 14T Tapped at 2T (Recommended)

**The standard EFHW transformer. Proven in thousands of builds.**

#### Specifications

| Parameter           | Value                              |
|---------------------|------------------------------------|
| Core                | 1x FT-240-43                      |
| Total winding       | 14 turns                           |
| Tap point           | 2 turns from ground                |
| Wire                | 18-16 AWG epoxy-coated magnet wire |
| Compensation cap    | 100-150 pF (adjust empirically)    |
| Lm (approx)         | 112.7 μH (14 turns)              |
| Connectors          | 1x SO-239 (coax), binding post (antenna) |
| Enclosure           | Project box                        |
| Power rating        | 100 W SSB / 30 W continuous        |
| Best bands          | 40m, 20m, 15m, 10m                |

#### Construction

**Step 1: Wind the toroid**

Cut a single length of magnet wire approximately 80 cm (32"). This allows
for 14 turns through the FT-240-43 core plus leads.

Wind 14 turns evenly around the core, covering ~270-300 degrees. Leave a
gap between the start and end leads.

**At the 2-turn mark, create a tap:** After passing the wire through the core
twice, make a small loop or leave extra wire (~5 cm) sticking out from the
winding. This will be your 50-ohm tap point. Then continue winding the
remaining 12 turns.

```
         ╭────────────────────╮
        ╱      FT-240-43       ╲
       │                        │
       │  2T     12T more       │
       │ ═══╤═══════════════    │
        ╲   │tap           ╱
         ╰──┼──────────────╯
        ↑   │              ↑
     start  50Ω tap       end
     (GND)               (ANT)
```

**Step 2: Strip and tin all connection points**

You have three wire points to prepare:
- **Start** (turn 0) — this is ground
- **Tap** (turn 2) — this is the 50-ohm connection
- **End** (turn 14) — this is the antenna terminal

Sand or scrape the epoxy insulation from each point. Tin with solder.

**Step 3: Add the compensation capacitor**

Solder a 100 pF ceramic capacitor (rated for the voltage — 1 kV or higher
recommended) between the tap wire and the start/ground wire. This capacitor
is physically small and solders directly to the wire leads.

```
    GND (turn 0) ──┬────── core ──┬──── core ──── ANT (turn 14)
                    │   2 turns    │   12 turns
                    │              │
                    ├──── [C] ─────┤
                    │   100 pF     │
                    │          50 Ω tap
                 SO-239 shell  SO-239 center
```

**Step 4: Connect to hardware**

- **GND wire** → SO-239 shell / ground lug / counterpoise terminal
- **Tap wire** → SO-239 center pin (through the compensation cap to GND)
- **End wire** → Antenna binding post

**Step 5: Tune the compensation capacitor**

1. Cut your antenna wire to the target half-wave length (see Wire Length
   table below)
2. Connect a NanoVNA to the SO-239
3. Sweep the target band and observe SWR
4. If SWR is too high on the upper bands (15m, 10m), increase capacitance
   (try 120 pF, 150 pF)
5. If SWR is too high on the lower bands (40m), decrease capacitance
   (try 82 pF, 68 pF)
6. Common final values are 100-150 pF for a 40m EFHW

**Step 6: Mount in enclosure**

- Mount SO-239 on one side
- Antenna binding post on top or opposite side
- Optional: ground lug for a short counterpoise wire
- Secure toroid with hot glue or RTV
- Weatherproof if mounting outdoors (silicone seal around connectors)

---

### Design B: Single FT-240-31, 14T Tapped at 2T

**Better magnetizing inductance, higher loss. Good for QRP.**

#### Specifications

| Parameter           | Value                              |
|---------------------|------------------------------------|
| Core                | 1x FT-240-31                      |
| Total winding       | 14 turns                           |
| Tap point           | 2 turns from ground                |
| Wire                | 18-16 AWG epoxy-coated magnet wire |
| Compensation cap    | 100-150 pF                         |
| Lm (approx)         | 210.7 μH (14 turns)              |
| Power rating        | 50 W SSB / 15 W continuous         |

#### Construction

Identical to Design A, substituting the FT-240-31 core.

#### When to choose this design
- QRP operation (<25 W) where core loss is acceptable
- You want the best possible 40m performance from a single core
- You're out of FT-240-43 cores

#### Caution
At 100 W SSB, the FT-240-31 core in a 49:1 transformer will run **hot**.
The combination of high primary current and lossy material can dissipate
5-10 W in the core. For sustained operation at 100 W, use Design A or C.

---

### Design C: Stacked 2x FT-240-43, 14T Tapped at 2T

**Best overall performance. Recommended for 100 W on all bands.**

#### Specifications

| Parameter           | Value                              |
|---------------------|------------------------------------|
| Core                | 2x FT-240-43 (stacked)            |
| Total winding       | 14 turns                           |
| Tap point           | 2 turns from ground                |
| Wire                | 18-16 AWG epoxy-coated magnet wire |
| Compensation cap    | 100-150 pF                         |
| Lm (approx)         | 225.4 μH (doubled Ae)             |
| Power rating        | 200 W SSB / 100 W continuous       |

#### Construction

Same as Design A, but:
- Stack two FT-240-43 cores, tape them together
- Wind 14 turns through both cores
- The doubled cross-section provides ~2× the magnetizing inductance
  and halves the flux density (lower core heating)

#### Advantages
- Magnetizing reactance of ~9900 Ω at 7 MHz — meets the 4× rule
- Core runs cooler at any given power level
- Better efficiency on 40m where the single core is marginal
- Can handle sustained 100 W digital modes

---

### Design D: Single FT-240-43, 21T Tapped at 3T (More Turns)

**Alternative ratio: (21/3)² = 49:1 with more magnetizing inductance.**

#### Specifications

| Parameter           | Value                              |
|---------------------|------------------------------------|
| Core                | 1x FT-240-43                      |
| Total winding       | 21 turns                           |
| Tap point           | 3 turns from ground                |
| Wire                | 20-18 AWG epoxy-coated magnet wire |
| Compensation cap    | 68-120 pF (more turns = more stray C) |
| Lm (approx)         | 253.4 μH (21 turns)              |
| Power rating        | 100 W SSB / 30 W continuous        |

#### Construction

Same approach as Design A but with 21 total turns and the tap at 3.

#### Tradeoffs vs Design A
- **Pro:** 2.25× more magnetizing inductance (253 μH vs 113 μH) — much
  better 40m performance from a single core
- **Pro:** Meets the 4× rule at 7 MHz on a single core
- **Con:** More turns = more inter-turn parasitic capacitance, which can
  create self-resonances that degrade performance on upper bands (10m)
- **Con:** Higher winding resistance (more wire)
- **Con:** More crowded on the core — may need thinner wire (20 AWG)
- **Con:** The compensation capacitor value is more sensitive and harder
  to optimize

This design works well if 40m is your priority and you're less concerned
about 10m performance. The extra parasitic capacitance tends to roll off
impedance above ~25 MHz.

---

## Compensation Capacitor Selection

The compensation capacitor is **critical** for good SWR across multiple bands.
Without it, the leakage inductance and parasitic effects cause the SWR to
climb steeply on the harmonic bands.

### Starting Values

| Design     | Start Value | Typical Final Range |
|------------|-------------|---------------------|
| A (14T/2T) | 100 pF      | 82-150 pF           |
| B (14T/2T) | 100 pF      | 82-150 pF           |
| C (14T/2T) | 100 pF      | 82-150 pF           |
| D (21T/3T) | 82 pF       | 56-120 pF           |

### Capacitor Requirements
- **Voltage rating:** At 100 W into 2450 Ω, peak voltage is:
  V_peak = √(2 × 100 × 2450) ≈ 700 V. At high SWR, it can be much higher.
  **Use 1 kV rated capacitors minimum**, 2 kV preferred.
- **Type:** Ceramic disc (C0G/NP0 preferred for stability) or silver mica.
  Do NOT use electrolytic or standard ceramic (X7R/Y5V).
- **Mounting:** Solder directly across the 2-turn winding leads, keeping
  leads as short as possible.

### Tuning Procedure

1. Build the transformer with a 100 pF cap installed
2. Cut antenna wire to calculated length
3. Connect NanoVNA to SO-239 port
4. Sweep each target band, record SWR minimum frequency
5. If SWR dips are too high in frequency → increase C (add a small cap
   in parallel — 22 pF, 33 pF increments)
6. If SWR dips are too low in frequency → decrease C (remove or replace
   with smaller value)
7. Target: SWR < 2:1 across each operating band

## Wire Lengths for EFHW

The antenna wire must be approximately ½λ at the fundamental frequency.
Due to end effects and velocity factor, the physical length is slightly
shorter than the free-space half wavelength.

    Physical length ≈ (143 / f_MHz) meters  (approximate, adjust by trimming)

### Common EFHW Configurations

| Fundamental | Wire Length | Harmonic Bands        | Notes              |
|-------------|-------------|-----------------------|--------------------|
| 80m (3.5)   | ~40.0 m (131') | 40m, 20m, 15m, 10m | Long, needs space. 80m is demanding on 49:1. |
| 40m (7.0)   | ~20.1 m (66')  | 20m, 15m, 10m      | Most popular EFHW. Sweet spot for size vs bands. |
| 30m (10.1)  | ~14.0 m (46')  | 15m (3rd), 10m (partial) | Fewer harmonics land on ham bands |
| 20m (14.0)  | ~10.1 m (33')  | 10m                 | Compact, great for portable |

**The 40m EFHW (~20 m wire) is the most popular choice** because:
- 20 m of wire is manageable for most yards and portable setups
- 40m, 20m, 15m, and 10m are the most active HF bands
- The even harmonics (20m = 2×, 10m = 4×) present high-Z at the feedpoint
  (good match to the 49:1), while the odd harmonic (15m = 3×) presents a
  different pattern but typically still works with the 49:1

### Trimming Process

1. Start with wire ~5% longer than calculated
2. Check SWR at the fundamental frequency
3. Trim 5-10 cm at a time from the far end
4. Re-check SWR — the dip should move up in frequency
5. Stop when SWR minimum is centered on your target frequency
6. The harmonic bands will generally fall into place once the fundamental
   is tuned

## Counterpoise

EFHW antennas are sometimes described as "no counterpoise needed," but
this is misleading. A short counterpoise improves performance:

- **Minimum:** ~0.05λ at the fundamental (e.g., ~1 m for 40m EFHW)
- **Better:** 2-3 m of wire, laid along the ground or coiled
- **Purpose:** Provides a local ground reference for the transformer and
  reduces common-mode current on the coax shield

Even a 1-meter wire attached to the ground terminal makes a measurable
difference. Without it, your coax shield becomes the counterpoise.

**Always pair with a common-mode choke** on the feedline (see
`../common-mode-choke/` project).

## Complete EFHW System

```
                                        ~20 m wire (40m fundamental)
                                     ╱
    [Radio] ══coax══ [CM Choke] ──── [49:1 Unun] ──────────────────────
                                        │
                                   [~1-3 m counterpoise]
```

## Verification and Testing

### With a NanoVNA

**Test 1: Transformer ratio verification**

Terminate the antenna port with a 2.2 kΩ or 2.7 kΩ non-inductive resistor.
Measure S11 at the SO-239 — it should show approximately 50 Ω (SWR < 1.5:1)
in the HF range.

Finding a 2450 Ω test load: series combination of resistors, e.g.:
- 2.2 kΩ + 270 Ω = 2470 Ω ≈ 2450 Ω
- 4.7 kΩ ∥ 4.7 kΩ = 2350 Ω (close enough)

**Test 2: On-antenna SWR sweep**

1. Connect the full antenna system (wire + counterpoise + CM choke)
2. Sweep each target band
3. Look for SWR dips — they should be near the band centers
4. If all dips are shifted, adjust wire length
5. If only upper bands are off, adjust compensation capacitor

**Test 3: Power test**

Transmit at low power (5-10 W) for 30 seconds, then touch the core.
If cool, increase to 50 W for 30 seconds. If still manageable, you're
good for 100 W SSB. If the core is uncomfortably hot at 50 W, consider
stacking cores (Design C).

## Files in This Project

- `bom.md` — Bill of materials for each design
- `simulations/unun49_performance.py` — Python script to model performance
- `measurements/` — Place NanoVNA exports and photos here after construction
