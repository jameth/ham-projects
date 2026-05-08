# HAM Radio Build & Operating Notes

Consolidated reference for design decisions, build calculations, and
operating topics that span multiple projects or don't fit inside a
single project's README.

---

## Contents

1. [Build calculations — wire and coax length](#build-calculations)
2. [Ferrite core selection](#ferrite-core-selection)
3. [Trifilar bundling — why we twist](#trifilar-bundling)
4. [Common-mode choke — 12T vs 9T on stacked cores](#cm-choke-12t-vs-9t)
5. [Integrated enclosure — 9:1 unun + CM choke in one box](#integrated-enclosure)
6. [Random wire lengths — magic lengths and SWR](#random-wire-lengths)
7. [Mobile HF operating — battery, grounding, and noise](#mobile-hf-operating)

---

<a name="build-calculations"></a>
## 1. Build calculations — wire and coax length

### Core cross-section path (one turn)

For a wire or coax wrapped around a toroid's cross-section, the per-turn
path is the perimeter of the wound geometry. Treat the wire/coax
centerline, not its surface:

```
Per turn ≈ 2 × ((wall + d_cond) + (height + d_cond))
```

where:
- `wall` = radial thickness = `(OD − ID) / 2`
- `height` = core height (doubles for stacked cores)
- `d_cond` = conductor outer diameter (bare wire + insulation / coating)

### Common conductor sizes

| Conductor | OD |
|---|---|
| 18 AWG bare copper | 1.02 mm |
| 18 AWG epoxy magnet wire | ~1.10 mm |
| 16 AWG magnet wire | ~1.35 mm |
| RG316 coax | ~2.49 mm |
| RG174 coax | ~2.80 mm |
| RG58 coax | ~5.00 mm |

### FT-240 per-turn lengths (reference table)

FT-240 dimensions: OD 61.0 mm, ID 35.55 mm, H 12.7 mm.
Wall = 12.725 mm. Single height = 12.7 mm. Stacked (2×) height = 25.4 mm.

| Build | d_cond | Single FT-240 | Stacked 2× FT-240 |
|---|---|---|---|
| 18 AWG magnet wire | 1.1 mm | ~55 mm/turn | ~80 mm/turn |
| RG316 coax | 2.5 mm | ~60 mm/turn | ~86 mm/turn |
| RG174 coax | 2.8 mm | ~62 mm/turn | ~88 mm/turn |

### FT-140 per-turn lengths (for reference)

FT-140: OD 35.55 mm, ID 22.86 mm, H 12.7 mm. Wall = 6.35 mm.

| Build | d_cond | Single FT-140 | Stacked 2× FT-140 |
|---|---|---|---|
| 18 AWG magnet wire | 1.1 mm | ~41 mm/turn | ~67 mm/turn |
| RG316 coax | 2.5 mm | ~46 mm/turn | ~72 mm/turn |

### Tail length allowance

Always add tails at each end for terminations:
- **Magnet wire to binding posts:** 5–8 cm each end
- **Magnet wire trifilar interconnects:** 5–10 cm each end (W1e↔W2s, W2e↔W3s)
- **RG316 to SO-239:** 8–12 cm each end (need room to strip, dress, solder)

### Worked examples

| Project | Turns | Cores | Conductor | Per turn | Winding | Tails | Per wire |
|---|---|---|---|---|---|---|---|
| 9:1 unun Design A | 12 | 1 × FT-240-43 | 18 AWG trifilar | 55 mm | 660 mm | +200 mm | ~85 cm/wire × 3 |
| 9:1 unun Design B | 10 | 1 × FT-240-31 | 18 AWG trifilar | 55 mm | 550 mm | +200 mm | ~70 cm/wire × 3 |
| 9:1 unun Design C | 10 | 2 × FT-240-43 | 18 AWG trifilar | 80 mm | 800 mm | +200 mm | ~95 cm/wire × 3 |
| CM choke Design A | 12 | 1 × FT-240-31 | RG316 | 60 mm | 720 mm | +200 mm | ~100 cm |
| CM choke Design B | 18 | 1 × FT-240-31 | 18 AWG bifilar | 55 mm | 990 mm | +200 mm | ~115 cm/wire × 2 |
| CM choke Design C (12T) | 12 | 2 × FT-240-31 | RG316 | 86 mm | 1030 mm | +300 mm | ~150 cm |
| CM choke Design C (9T) | 9 | 2 × FT-240-31 | RG316 | 86 mm | 775 mm | +300 mm | ~110 cm |

Always buy 15–25% extra — handling stiff wire/coax is easier with some
slack, and trim errors are common.

---

<a name="ferrite-core-selection"></a>
## 2. Ferrite core selection

### Mix 31 vs Mix 43

| Property | Mix 31 | Mix 43 |
|---|---|---|
| Initial permeability (μi) | ~1500 | ~800 |
| Optimal frequency | 1–30 MHz | 10–250 MHz |
| HF character | Resistive (lossy) | Mixed to resistive |
| Best use | CM chokes, lossy applications | Transformers (ununs, baluns) |

**Rule:** Mix 31 for chokes (you *want* loss — it absorbs CM energy as
heat). Mix 43 for transformers (you *don't want* loss — signal power
must pass through).

Mix 31 in a transformer = heat. Mix 43 in a choke = reflection instead
of absorption of CM current.

### FT-140 vs FT-240

| | FT-140 | FT-240 |
|---|---|---|
| OD / ID / H | 35.55 / 22.86 / 12.7 mm | 61.0 / 35.55 / 12.7 mm |
| Cross-section (Ae) | 81 mm² | 162 mm² |
| Magnetic path (le) | 92 mm | 152 mm |
| Core constant | 1.10 × 10⁻⁹ H | 1.34 × 10⁻⁹ H |
| Per-turn inductance ratio | 0.82 × FT-240 | 1.0 (reference) |
| Power handling (trifilar 12T mix 43) | ~25–30 W SSB | 100 W SSB |
| Window area (inner circumference) | 72 mm | 112 mm |

**Use FT-140 when:**
- QRP (≤20 W)
- Portable / backpack / SOTA / POTA
- Small enclosure required
- Dedicated single-band builds

**Use FT-240 when:**
- 100 W+ SSB or continuous digital modes
- Broadband builds needing spaced turns
- Heavier wire or coax
- General-purpose shack use

**2× stacked FT-140 ≈ single FT-240:**
- Stacking doubles Ae → matches FT-240 cross-section
- le stays at 92 mm (shorter than FT-240's 152 mm)
- Core constant of stacked pair is actually *higher* than single FT-240
- Thermal capacity lower because total ferrite volume is smaller
- Window crowding still an issue (same ID as single FT-140)

### Stacking cores

- Doubles effective `Ae` → doubles inductance per turn (at same `le`)
- Preserves broadband behavior better than adding turns (fewer parasitics)
- Requires taller enclosure
- Secure with Kapton or electrical tape before winding

**Stacking vs more turns:**
- `N²` inductance scaling means more turns looks attractive
- BUT more turns = more inter-turn capacitance = lower self-resonance
- Stacking doubles inductance while keeping turn count (and capacitance) constant
- Stacking is the preferred way to scale up for broadband applications

---

<a name="trifilar-bundling"></a>
## 3. Trifilar bundling — why we twist

For a trifilar autotransformer (9:1 unun), the three wires are
twisted or laid tight side-by-side as a bundle. Not for the reason most
people assume.

### Flux-wise, position doesn't matter

Any wire passing through a toroid's center hole links the same core
flux — the flux is contained inside the core, so wire position on the
surface doesn't change the mutual inductance through the core.

### What the bundle actually does

1. **Minimizes leakage inductance *between* windings**
   - When wires are in intimate contact, any stray flux around one wire
     is immediately inside the neighbors → coupling `k ≈ 0.99+`
   - When wires are spaced apart, stray flux links some wires but not
     others → coupling drops to `k ≈ 0.95–0.98`
   - Leakage inductance shows up as series reactance at the high end
     of the operating range → SWR climb and insertion loss above 20 MHz

2. **Sets characteristic impedance of the trifilar "transmission line"**
   - This is Sevick's insight — the windings form a short length of
     transmission line, not just lumped inductors
   - Tight twist: `Z₀ ≈ 50–80 Ω`
   - Loose twist: `Z₀ ≈ 80–120 Ω`
   - Spaced parallel: `Z₀ ≈ 120–180 Ω`
   - For a 9:1 transforming 50→450 Ω, ideal `Z₀ ≈ 100 Ω` (geometric mean)
   - 1–2 twists per inch = close to ideal

3. **Mechanical discipline during winding**
   - Three loose wires tangle and cross → lose polarity, get shorts
   - A bundle maintains wire order through all 12 turns
   - Every turn sees the same geometry, so coupling is consistent

### Twist tightness tradeoff

| Tighter | Looser |
|---|---|
| ↓ Leakage inductance (good) | ↑ Leakage inductance (bad at top of HF) |
| ↑ Inter-winding capacitance (bad) | ↓ Inter-winding capacitance (good) |
| Lower Z₀ | Higher Z₀ (closer to 100 Ω ideal) |
| Better 80m/low-end | Better 10m/high-end |

**Sweet spot for 9:1: 1–2 twists per inch.** Tight enough to guarantee
coupling and mechanical order, loose enough to keep capacitance from
dominating.

### Flat-wound (ribbon) alternative

Three wires laid flat and parallel, taped into a ribbon, works just as
well — arguably slightly better electrically because `Z₀` lands closer
to the 100 Ω ideal. Stiffer to wind, but forgiving on an FT-240's large
ID. Many production ununs use this method.

### Critical: polarity

All three windings must have the same polarity (dots on the same side).
A bundle maintains this automatically because wires can't cross. Three
loose wires can swap positions mid-winding and flip one winding's
polarity, breaking the transformer. **This is the real hidden reason
bundles exist** — failure-mode prevention, not just a performance
optimization.

### Drill-twist technique

- Chuck one end of all three wires in a hand drill
- Clamp the far end in a vise
- Spin gently, feeding with the free hand
- Target 1–2 twists per inch
- Much more uniform than twisting by hand

---

<a name="cm-choke-12t-vs-9t"></a>
## 4. Common-mode choke — 12T vs 9T on stacked cores

For Design C (RG316 on stacked 2× FT-240-31), 9 turns is a solid
alternative to the published 12 turns.

### Impedance comparison

Impedance scales as N², so 9T gives `(9/12)² = 0.5625` → about **56%**
of the 12-turn impedance.

| Band | 12T \|Z\| | 9T \|Z\| | 12T Rs | 9T Rs |
|---|---|---|---|---|
| 80m | ~8700 | ~4900 | ~6000 | ~3375 |
| 40m | ~11800 | ~6640 | ~10500 | ~5900 |
| 30m | ~13300 | ~7480 | ~12400 | ~6975 |
| 20m | ~14300 | ~8040 | ~13600 | ~7650 |
| 17m | ~14700 | ~8270 | ~14200 | ~7990 |
| 15m | ~14700 | ~8270 | ~14300 | ~8040 |
| 12m | ~14600 | ~8210 | ~14250 | ~8015 |
| 10m | ~14400 | ~8100 | ~14100 | ~7930 |

Both builds stay well above the 1000 Ω design target on every HF band.

### Where 9T wins

1. **Higher self-resonant frequency** — fewer turns = less inter-turn
   capacitance = SRF pushed up, keeping the top of HF (12m/10m) cleaner
2. **Real-world vs theoretical ratio closer to 1** — the parasitic
   haircut in the README shrinks with fewer turns, so measured gap
   vs 12T is smaller than 56%
3. **Easier to wind** — more room to space turns evenly with a clean gap
4. **Less coax** — ~25% shorter winding
5. **Lower stray series inductance**

### Where 12T wins

1. **80m headroom** — 8700 Ω vs 4900 Ω; matters with high-SWR EFHW on 80m
2. **Matches the published design** and simulation script defaults

### Recommendation

- 40m–10m primary → **9T** is the smarter build
- 80m is a priority → stick with **12T** for the low-end margin

---

<a name="integrated-enclosure"></a>
## 5. Integrated enclosure — 9:1 unun + CM choke in one box

Combining the 9:1 unun and CM choke into a single enclosure is the
**preferred build** for a permanent installation — and how most
commercial end-fed matchers are made (LNR Precision, MyAntennas,
Palomar, MFJ 1982).

### Advantages over separate boxes

1. Fewer connections — no inter-box coax jumper to corrode or fail
2. Choke is immediately at the unun output, catching CM current before
   it can establish on the shield
3. One weatherproof enclosure instead of two
4. Cleaner mechanical install at the feedpoint
5. Shorter, controlled interconnects → less stray coupling

### Critical wiring rule

Choke goes **after** the unun (on the 50 Ω side), never before it. The
antenna, counterpoise, and unun live on the high-Z "antenna system"
side. The SO-239 lives on the isolated "feedline" side. The choke is
the isolator between them.

```
   [ANT wire]─┬─[GND/Counterpoise]
              │          │
              │          │         50 Ω tap
   ┌──────────┴──────────┴──── W1 ──── W2 ──── W3 ─┐
   │                                                │
   │        9:1 Unun (FT-240-43, 12T trifilar)     │
   │                                                │
   └──────────┬─────────────────────────────────────┘
              │ (50 Ω, short lead)
              │
   ┌──────────┴───────────────────────────────┐
   │                                           │
   │   CM Choke (FT-240-31, 12T RG316 or     │
   │            bifilar magnet wire)          │
   │                                           │
   └──────────┬───────────────────────────────┘
              │
           [SO-239] ─── coax to radio
```

**Do not** bond the counterpoise terminal to the SO-239 shell inside
the box. That shorts out the choke. They're bonded through the choke
windings at DC, but isolated at RF by 5–8 kΩ — exactly what we want.

### Layout considerations

- **Orient cores perpendicular** to each other (or space by one core
  diameter, ~60 mm for FT-240) to minimize mutual coupling
- **Short, direct jumper** between unun output and choke input
- **Antenna terminal and SO-239 on opposite ends of the box** so input
  and output leads aren't near each other

### Box size

| Configuration | Minimum size |
|---|---|
| Two single FT-240 cores, loose layout | 200 × 120 × 70 mm |
| Two single FT-240 cores, tight layout | 170 × 120 × 60 mm |
| Stacked cores on either side | add ~15 mm height |

Good enclosure options:
- Bud NBB-15247 / NBB-15248 (metal, optional shielding)
- Hammond 1554 series (polycarbonate, weatherproof)
- Generic NEMA 4X plastic enclosure

### Two sensible build variants

**Variant A — coax-wound choke** (cleanest electrically)
- 9:1 unun (FT-240-43, 12T trifilar)
- CM choke: RG316 12T on FT-240-31
- Internal coax jumper between unun tap and choke input
- Shield continuous from choke output to radio

**Variant B — bifilar magnet wire choke** (simpler mechanically)
- 9:1 unun (FT-240-43, 12T trifilar)
- CM choke: 18 AWG bifilar 18T on FT-240-31
- No coax inside the box — unun tap wires directly to bifilar
- Bifilar output wires directly to SO-239
- ~2× choke impedance vs coax version

### Weatherproofing

- IP65+ gasketed enclosure
- **Drain hole** (3 mm angled down) at the bottom — condensation will
  form in any outdoor box and must be able to escape
- Cord grip (PG7/PG9) or compression gland for the antenna wire entry
- Stainless hardware, dielectric grease on SO-239 threads
- Through-bolt the antenna terminal with backup washers — the wire
  will load the enclosure in wind

### Build sequence

1. Build 9:1 unun independently. Terminate with 450 Ω dummy load.
   Sweep S11 on coax side — should show SWR < 1.5:1 across HF.
2. Build CM choke independently. Verify via CM shunt method —
   \|Z\| > 1000 Ω across HF.
3. Mount both in the enclosure with short interconnect.
4. Re-sweep combined unit with 450 Ω load. Should look nearly
   identical to unun alone; choke adds < 0.2 dB insertion loss.

### Gotchas

- Counterpoise wiring: to unun ground, **not** SO-239 shell
- Inter-stage lead routing: don't run the 50 Ω jumper parallel to or
  through the unun windings
- Mechanical support: the antenna wire pulls on the enclosure with
  wind loading; use through-bolts, not screws into thin plastic
- Forgotten drain hole: condensation pools → corrosion

---

<a name="random-wire-lengths"></a>
## 6. Random wire lengths — magic lengths and SWR

For a 9:1 unun feeding a random wire antenna.

### The magic lengths

Lengths chosen to avoid `n·λ/2` resonances on the ham bands. At a
half-wavelength, feedpoint impedance rockets to thousands of ohms,
which no tuner can match. These lengths keep feedpoint impedance
mostly in 200–800 Ω, which the 9:1 maps to 22–89 Ω — well within
tuner range on marked-good bands.

| Length (ft) | Length (m) | 160m | 80m | 40m | 30m | 20m | 17m | 15m | 12m | 10m |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 29 ft | 8.84 | — | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ |
| 35.5 ft | 10.82 | — | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ |
| 41 ft | 12.50 | — | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ |
| 58 ft | 17.68 | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| 71 ft | 21.64 | — | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✓ |
| **84 ft** 🏆 | 25.60 | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 107 ft | 32.61 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| 124 ft | 37.80 | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |

Legend: ✓ tuner-friendly (SWR < 10:1), ✗ near λ/2 multiple, ~ marginal

### SWR ranges — which bands work with a rig's internal tuner (≤ 3:1)

**Caveat:** these are **typical** installation values. Wire height,
counterpoise quality, ground conductivity, and nearby objects shift
results by ±30% or more.

| Length | 160 | 80 | 60 | 40 | 30 | 20 | 17 | 15 | 12 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 29 ft | ✗ | ✗ | ✗ | 🟢 2–3 | 🟡 3–4 | 🟢 2–3 | ✗ | 🟢 2–3 | ✗ | 🟢 2–3 |
| 35.5 ft | ✗ | 🟡 3–4 | ✗ | ✗ | 🟡 3–4 | ✗ | 🟢 2–3 | ✗ | 🟢 2–3 | ✗ |
| 41 ft | ✗ | 🟡 5–7 | ✗ | 🟢 1.5–2.5 | 🟡 3–4 | 🟢 1.5–3 | ✗ | 🟢 2–3 | ✗ | 🟢 2–3 |
| 58 ft | ✗ | 🟡 3–5 | 🟢 2–3 | 🟢 2–3 | 🟢 2–3 | 🟢 2–3 | 🟡 3–4 | ✗ | 🟢 2–3 | 🟢 2–3 |
| 71 ft | ✗ | ✗ | 🟡 3–5 | ✗ | 🟢 2–3 | ✗ | 🟢 2–3 | ✗ | 🟢 2–3 | 🟢 2–3 |
| 84 ft 🏆 | ~ | 🟢 2–3 | 🟡 3–4 | 🟢 1.5–2.5 | 🟢 2–3 | 🟡 3–4 | 🟢 2–3 | 🟡 3–4 | 🟢 2–3 | 🟡 3–4 |
| 107 ft | 🟡 3–6 | 🟢 2–3 | 🟢 2–3 | 🟢 2–3 | 🟢 2–3 | 🟡 3–4 | 🟢 2–3 | 🟡 3–4 | ✗ | 🟡 3–4 |
| 124 ft | 🟡 3–5 | 🟢 1.5–2.5 | ✗ | 🟢 2–3 | ✗ | 🟢 2–3 | 🟡 3–4 | 🟢 2–3 | 🟢 2–3 | 🟢 2–3 |

Legend: 🟢 ≤ 3:1 (internal tuner handles), 🟡 3–5:1 (external needed),
✗ near λ/2 (no tuner saves you)

### Internal-tuner-friendly count per length

| Length | 🟢 bands | Count |
|---|---|---|
| 29 ft | 40, 20, 15, 10 | 4 |
| 35.5 ft | 17, 12 | 2 |
| 41 ft | 40, 20, 15, 10 | 4 |
| 58 ft | 60, 40, 30, 20, 12, 10 | **6** |
| 71 ft | 30, 17, 12, 10 | 4 |
| 84 ft | 80, 40, 30, 17, 12 | 5 |
| 107 ft | 80, 60, 40, 30, 17 | 5 |
| 124 ft | 80, 40, 20, 15, 12, 10 | **6** |

### Picks by use case

- **Best all-around with external tuner:** 84 ft
- **Best compact with internal tuner:** 58 ft (6 bands, no 80m)
- **Best long wire with internal tuner:** 124 ft (6 bands including 80m)
- **Best compact suburban:** 41 ft (4 bands, 80m–10m coverage)
- **Tight yard:** 29 ft (4 bands, 40m+)
- **160m capable:** 107 ft or 124 ft

### Counterpoise pairing

Counterpoise length must be **different** from antenna length and from
any `n·λ/2` multiple.

| Antenna | Counterpoise |
|---|---|
| 29 ft | 17 ft or 25 ft |
| 41 ft | 17 ft or 25 ft or 33 ft |
| 58 ft | 17 ft + 25 ft (two radials) |
| 84 ft | 17 ft + 25 ft + 33 ft (three radials) |
| 107 ft | 33 ft + 50 ft (two radials) |
| 124 ft | 33 ft + 50 ft + 65 ft (three radials) |

A single 17 ft counterpoise works as a minimum for all of the above.
More radials = better pattern and lower RX noise floor.

### λ/2 reference (for checking custom lengths)

| Band | λ/2 (ft) | Stay away from |
|---|---|---|
| 80m | 140.6 | 140, 281 |
| 40m | 70.3 | 70, 141, 211 |
| 30m | 48.7 | 49, 97, 146 |
| 20m | 34.9 | 35, 70, 105, 140 |
| 17m | 27.2 | 27, 54, 82, 109 |
| 15m | 23.2 | 23, 46, 70, 93, 116 |
| 12m | 19.8 | 20, 40, 59, 79, 99, 119 |
| 10m | 17.3 | 17, 35, 52, 69, 87, 104 |

Keep wire length at least 6% away from these values on your desired bands.

### Internal tuner SWR limits (reference)

- Most Icom/Yaesu/Kenwood internal tuners: ~3:1
- Icom IC-7300, IC-705, IC-7610, 7851, IC-7100: ~3:1
- Yaesu FT-991A, FT-891: ~3:1
- Kenwood TS-590: ~3:1
- Older rigs (no internal tuner): rig handles ~2:1 at full power
- External autotuners (LDG, MFJ, Icom AH-4/705): 10:1+

---

<a name="mobile-hf-operating"></a>
## 7. Mobile HF operating — battery, grounding, and noise

### Noise floor: isolated battery vs vehicle electrical

**Isolated external battery** (no connection to vehicle 12V):
- Typically **lower noise floor** than connecting to vehicle electrical
- Eliminates conducted noise path from alternator, ECU, injectors,
  DC-DC converters, CAN bus, fuel pump PWM
- Antenna still picks up radiated noise from the vehicle regardless
- Usually 1–3 S-units quieter on low bands than a 12V-integrated install

**Vehicle-integrated power:**
- Direct conducted path for vehicle electrical noise
- Modern vehicles (smart alternators, LED drivers, infotainment) are
  electrically filthy
- Filtering helps but never fully cures it
- Benefits: continuous runtime, full-voltage supply, "permanent install"

**Hybrid approach (best of both):**
- Isolated battery for power
- Short fat bond strap (¼" braid) from radio chassis to a clean
  chassis bolt on the vehicle body
- Bonds radio to RF ground (mag mount counterpoise) without
  conducting noise from the 12V system
- Usually eliminates hot-mic / RF-bite issues

### Mag-mount counterpoise

- Couples capacitively to vehicle roof — not DC ground, but works for
  RF at HF
- Better at 20m and up; marginal on 80m/40m where counterpoise quality
  matters more
- A floating radio chassis can let CM currents ride on the coax, mic,
  and DC cables → symptoms include hot mic, display glitches, erratic
  keying

### Charging options — isolated battery from vehicle

**Option 1: VSR / ACR (Voltage-Sensitive Relay)**
- Closes at ~13.3 V (engine running), opens at ~12.8 V (off)
- ~$40–100, simple, reliable
- No multi-stage charging — aux sees raw alternator voltage
- Doesn't work well with smart alternators (modern 2015+ vehicles
  drop alternator to 12.3 V at cruise)
- Good for AGM / flooded lead-acid, older vehicles

**Option 2: DC-DC charger**
- Boosts input to proper aux battery voltage regardless of source
- Multi-stage profile for LiFePO4 / AGM / flooded
- Works with smart alternators
- Brands: Victron Orion-Tr Smart, Redarc BCDC, CTEK D250SE
- $150–400
- IS a switching converter — can add HF noise; quality units (Victron,
  Redarc) are well-filtered
- Shuts off via ignition sense when engine off

**Option 3: Shore power charger**
- AC wall charger at home between trips
- Zero vehicle integration, zero added noise
- NOCO Genius, CTEK MXS 5.0 — $60–100

**Option 4: Solar**
- 50–100 W panel + MPPT controller
- Quiet on HF if controller is good (Victron SmartSolar recommended)
- Cheap no-name MPPT controllers can be terrible for RF
- Best for extended field ops (POTA/SOTA)

### On-demand charging while driving

Wire a dashboard switch to either a relay coil or the remote-enable
input of a DC-DC charger:

```
Starter (+) ──[fuse]── DC-DC IN ──── DC-DC OUT ──[fuse]── Aux (+)
                         │
                         └── ENABLE ──[dashboard switch]── ignition-hot
```

- Switch ON + engine running = charging
- Switch OFF = aux fully isolated, quiet operation
- Use Anderson Powerpoles so aux battery can still be pulled for
  home charging

Recommended switch: **lit rocker on the dash** so charge state is
always visible at a glance.

### Recommended build for on-demand mobile

- Victron Orion-Tr Smart 12/12-18 or 12/12-30
- 8 AWG battery cable (6 AWG for long runs / > 40 A)
- ANL fuses at **both ends** of the charging line (fire-safety critical)
- Anderson Powerpole 50A disconnect near the aux battery
- Lit rocker switch on dash for remote enable

### Wiring safety notes

- Fuses within 6" of each battery's positive terminal
- Run positive and negative cables together, away from ignition wiring
- Dedicated ground wire back to starter negative or clean chassis bolt
- Don't rely on incidental chassis grounds
- Keep charging cables away from the coax run (tidy, not RF-critical)

### Quick noise diagnostic

Before committing to a build:

1. Note noise floor with engine off, accessories off
2. Key to accessory (no engine)
3. Start engine, accessories off
4. Add loads (lights, fan, infotainment)

Steps 3–4 show how much of your current noise would increase with
vehicle integration. If step 3 is already a wall of hash, a DC-DC won't
help — the problem is radiated, not conducted, and isolation is your
only defense.

### Why stop/start and EV/hybrid vehicles need special care

- ECU monitors starter battery state of charge — adding a second load
  can confuse charge management
- High-voltage systems can be noisy on HF
- DC-DC chargers handle this more gracefully than VSRs
- Never tap factory starter on these platforms without understanding
  the charge strategy

---

## Quick-reference calculations

### Impedance scaling with turns

`Z_new = Z_old × (N_new / N_old)²`

Example: 12T → 9T = `(9/12)² = 0.5625` → 56% of original impedance

### Magnetizing inductance rule

For a transformer to work broadband:
`X_Lm > 4 × Z_load at lowest operating frequency`

For 450 Ω at 3.5 MHz:
`X_Lm > 1800 Ω → Lm > 82 μH`

### Coupling coefficient target

- Trifilar autotransformer: `k ≈ 0.95+` required for broadband operation
- Tight bundling or flat-lay ribbon: `k ≈ 0.99+`
- Spaced parallel wires: `k ≈ 0.95–0.98` (leakage starts to hurt)

### Internal tuner SWR threshold

Most rigs: **3:1**. Above 3:1, internal tuner either refuses to engage,
takes a long time to find a match, or can't hold one under load.
