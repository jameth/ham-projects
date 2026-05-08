# Common Mode Choke for End-Fed HF Antenna

## Design Goals

- Suppress common-mode current on the coax feedline of an end-fed HF antenna
- Target choking impedance: >1000 ohms across 80m-10m (3.5-30 MHz)
- Achieve primarily **resistive** impedance (absorb CM energy, don't reflect it)
- Power handling: up to 100 W SSB
- Use available materials: FT-240-31/43 toroids, RG316 coax, epoxy-coated magnet wire

## Theory of Operation

A common-mode choke works by presenting high impedance to common-mode currents
while having negligible effect on differential-mode (wanted) signals.

**Why common-mode currents are a problem on end-fed antennas:**
End-fed antennas are inherently unbalanced. The coax shield becomes part of the
radiating system, carrying RF current back into the shack. This causes:
- RFI to station electronics
- Distorted radiation pattern
- Noise pickup on receive
- Inaccurate SWR readings

**How the choke works:**
When wire or coax is wound on a ferrite toroid, the core only "sees" the net
magnetic flux. Differential-mode current (equal and opposite in the two
conductors) produces zero net flux — the choke is invisible to it. Common-mode
current (same direction in both conductors) produces net flux and sees the full
impedance of the ferrite-loaded winding.

**Why resistive impedance matters:**
A choke with primarily reactive (inductive) impedance reflects common-mode
energy back toward the antenna, potentially creating a standing wave on the
shield and moving the problem rather than solving it. A choke with resistive
impedance dissipates the common-mode energy as heat, actually eliminating it.
Mix 31 ferrite provides primarily resistive impedance across the HF bands.

## Ferrite Core Selection

### FT-240-31 (Fair-Rite Mix 31) — Recommended for HF

| Parameter              | Value            |
|------------------------|------------------|
| Initial permeability   | ~1500            |
| Optimal frequency      | 1-30 MHz         |
| Impedance character    | Resistive at HF  |
| Core OD                | 61.0 mm (2.40")  |
| Core ID                | 35.55 mm (1.40") |
| Core height            | 12.7 mm (0.50")  |

Mix 31 is the standard choice for HF common-mode chokes. Its lossy
characteristic at HF frequencies means the impedance is dominated by the
resistive component (Rs >> Xs), which is exactly what we want.

### FT-240-43 (Fair-Rite Mix 43) — Better for VHF / Upper HF

| Parameter              | Value             |
|------------------------|-------------------|
| Initial permeability   | ~800              |
| Optimal frequency      | 20-250 MHz        |
| Impedance character    | Reactive at lower HF, resistive above ~15 MHz |
| Core OD                | 61.0 mm (2.40")   |
| Core ID                | 35.55 mm (1.40")  |
| Core height            | 12.7 mm (0.50")   |

Mix 43 peaks at higher frequencies. At 80m/40m it provides less impedance
and what it does provide is largely reactive. Suitable for dedicated 10m/6m
chokes or VHF applications, but not ideal as a broadband HF choke.

## Design Variants

---

### Design A: RG316 Coax on Single FT-240-31

**The recommended general-purpose build.**

#### Specifications

| Parameter         | Value                    |
|-------------------|--------------------------|
| Core              | 1x FT-240-31            |
| Winding           | 12 turns RG316 coax     |
| Connectors        | 2x SO-239 chassis mount |
| Enclosure         | Project box              |
| Power rating      | 100 W SSB / 50 W continuous (FT8, RTTY) |

#### Expected Choking Impedance

| Band | Freq (MHz) | \|Z\| (ohms) | Rs (ohms) | Character   |
|------|-----------|--------------|-----------|-------------|
| 80m  | 3.5       | ~4350        | ~3000     | Mixed       |
| 40m  | 7.0       | ~5900        | ~5250     | Resistive   |
| 30m  | 10.1      | ~6650        | ~6200     | Resistive   |
| 20m  | 14.0      | ~7150        | ~6800     | Resistive   |
| 17m  | 18.1      | ~7350        | ~7100     | Resistive   |
| 15m  | 21.0      | ~7350        | ~7150     | Resistive   |
| 12m  | 24.9      | ~7300        | ~7100     | Resistive   |
| 10m  | 28.0      | ~7200        | ~7050     | Resistive   |

*Theoretical values from the impedance model (see `simulations/choke_impedance.py`).
Real-world values will be 30-50% lower due to inter-turn parasitic capacitance,
which the model does not account for. Verify with a NanoVNA after construction.*

#### Construction

1. **Prepare the core:** Clean the FT-240-31 toroid. Optionally wrap with a
   single layer of cloth electrical tape or Kapton tape to protect the coax
   jacket from the core's sharp edges (though FT-240 cores are generally
   smooth enough for RG316).

2. **Wind the coax:** Pass the RG316 through the center of the toroid 12 times.
   Each pass through the hole counts as one turn. Space the turns evenly around
   the core, covering approximately 270-300 degrees (leave a gap between the
   input and output leads to minimize capacitive coupling).

   ```
        ┌──────────────┐
        │   ╭─toroid─╮  │
   IN ──┤   │ 12 turns│  ├── OUT
        │   ╰────────╯  │
        │  (leave gap)   │
        └──────────────┘
   ```

3. **Terminate:** Solder SO-239 connectors to each end of the coax. Shield to
   the connector body/ground, center conductor to the center pin.

4. **Mount in enclosure:** Secure the SO-239 connectors on opposite ends of the
   project box. Secure the toroid inside with hot glue, RTV silicone, or a
   cable tie through the center.

5. **Label:** Mark the antenna side and radio side. The choke works in either
   direction, but labeling helps with troubleshooting.

#### Tips
- Keep the input and output leads short to minimize stray capacitance
- Don't let the coax cross over itself on the core
- RG316 has a tight bend radius — the FT-240 is large enough that this isn't
  a concern, but don't kink the cable

---

### Design B: Bifilar Magnet Wire on Single FT-240-31

**Best low-band performance, trades impedance match for more choking.**

#### Specifications

| Parameter         | Value                          |
|-------------------|--------------------------------|
| Core              | 1x FT-240-31                  |
| Winding           | 18 turns bifilar magnet wire   |
| Wire gauge        | 18-16 AWG epoxy-coated magnet wire |
| Connectors        | 2x SO-239 chassis mount       |
| Enclosure         | Project box                    |
| Power rating      | Depends on wire gauge; 18 AWG ~150 W SSB |

#### Expected Choking Impedance

| Band | Freq (MHz) | \|Z\| (ohms) | Rs (ohms) | Character   |
|------|-----------|--------------|-----------|-------------|
| 80m  | 3.5       | ~9800        | ~6750     | Mixed       |
| 40m  | 7.0       | ~13300       | ~11800    | Resistive   |
| 30m  | 10.1      | ~15000       | ~14000    | Resistive   |
| 20m  | 14.0      | ~16100       | ~15300    | Resistive   |
| 17m  | 18.1      | ~16500       | ~16000    | Resistive   |
| 15m  | 21.0      | ~16550       | ~16100    | Resistive   |
| 12m  | 24.9      | ~16400       | ~16000    | Resistive   |
| 10m  | 28.0      | ~16200       | ~15850    | Resistive   |

*Theoretical values — (18/12)² = 2.25x Design A. Real-world values will be
lower due to inter-turn capacitance. Bifilar winding has higher parasitic
capacitance than coax, so expect ~40-60% of theoretical. Verify with NanoVNA.*

#### Construction

1. **Prepare the bifilar pair:** Cut two equal lengths of magnet wire
   (~60 cm / 24" each — allows for 18 turns plus lead length). Twist them
   together at approximately 2-3 twists per inch, or lay them flat side by side.
   Twisting provides more consistent impedance between the conductors.

   ```
   Wire A (hot):    ────────────────────
   Wire B (return): ────────────────────
                    twisted together
   ```

2. **Wind the core:** Pass the twisted pair through the FT-240-31 toroid
   18 times. Space evenly, covering ~270-300 degrees. Same gap principle
   as Design A.

3. **Identify wires:** Use a multimeter in continuity mode to identify which
   wire is which at both ends. Label them A and B.

4. **Connect to SO-239 connectors:**
   - Input SO-239: Wire A start → center pin, Wire B start → ground
   - Output SO-239: Wire A end → center pin, Wire B end → ground
   - This ensures the signal follows one wire and returns on the other
     (differential mode), while common-mode current sees the full choke.

   **CRITICAL:** Both wires must be connected the same way at both ends —
   A is always hot, B is always ground. If you reverse one end, you've made
   a short circuit instead of a choke.

5. **Scrape insulation and solder:** Epoxy-coated magnet wire needs the
   insulation removed at the connection points. Use fine sandpaper, a razor
   blade, or a solder pot to tin the ends. Verify continuity before final
   assembly.

6. **Mount in enclosure:** Same as Design A.

#### Tradeoffs vs. Design A
- **Pro:** ~2.25x higher choking impedance at every frequency
- **Pro:** Significantly better on 80m where coax chokes often fall short
- **Con:** Characteristic impedance between the wires is ~80-120 ohms (not 50),
  introducing a mild SWR bump. At the short electrical length of the choke
  (~18 turns on a 2.4" core), the mismatch loss is typically <0.2 dB — negligible
  in practice.
- **Con:** Voltage isolation depends on the magnet wire's insulation rating.
  At high SWR (common on end-fed antennas), voltage between turns can be high.
  Verify your wire's voltage rating for your power level.

---

### Design C: RG316 Coax on Stacked 2x FT-240-31

**Maximum performance with controlled impedance.**

#### Specifications

| Parameter         | Value                     |
|-------------------|---------------------------|
| Core              | 2x FT-240-31 (stacked)   |
| Winding           | 12 turns RG316 coax       |
| Connectors        | 2x SO-239 chassis mount   |
| Enclosure         | Project box (taller)      |
| Power rating      | 100 W SSB / 50 W continuous |

#### Expected Choking Impedance

Stacking two cores approximately **doubles** the choking impedance compared
to a single core (Design A), because the effective permeability path doubles.

| Band | Freq (MHz) | \|Z\| (ohms) | Rs (ohms) | Character   |
|------|-----------|--------------|-----------|-------------|
| 80m  | 3.5       | ~8700        | ~6000     | Mixed       |
| 40m  | 7.0       | ~11800       | ~10500    | Resistive   |
| 30m  | 10.1      | ~13300       | ~12400    | Resistive   |
| 20m  | 14.0      | ~14300       | ~13600    | Resistive   |
| 17m  | 18.1      | ~14700       | ~14200    | Resistive   |
| 15m  | 21.0      | ~14700       | ~14300    | Resistive   |
| 12m  | 24.9      | ~14600       | ~14250    | Resistive   |
| 10m  | 28.0      | ~14400       | ~14100    | Resistive   |

*Theoretical values. Expect 30-50% reduction in practice due to parasitics.
Stacked cores have similar parasitic behavior to Design A (same turn count),
so the real-world ratio between C and A should hold close to 2x.*

#### Construction

1. **Stack the cores:** Place two FT-240-31 toroids on top of each other.
   Secure with a wrap of electrical tape or Kapton tape to hold them together
   as a single unit.

2. **Wind and terminate:** Identical to Design A, but pass the RG316 through
   both stacked cores on each turn. 12 turns through the pair.

3. **Enclosure:** You'll need a slightly larger project box to accommodate
   the doubled core height (25.4 mm / 1.0" stack).

#### Why stack instead of more turns?
- Stacking doubles impedance while keeping turn count (and inter-turn
  capacitance) the same
- More turns increases parasitic capacitance, which can create a self-resonance
  that reduces impedance at higher frequencies
- Stacking preserves the broadband characteristic better than adding turns

#### 9-turn variant on stacked cores

If 12 turns of RG316 on a stacked FT-240 pair is too tight (the window
crowds quickly), **9 turns is a solid alternative**:

- Impedance scales as N², so 9T gives `(9/12)² = 0.5625` — about 56%
  of the 12-turn impedance
- Still comfortably above the 1000 Ω target on every HF band
  (~4900 Ω on 80m, ~8000 Ω on 20m and up)
- **Higher self-resonant frequency** — fewer turns = less inter-turn
  capacitance, so 12m/10m real-world performance often matches or
  exceeds the 12T version once parasitics are accounted for
- Easier to wind with even spacing and a clean gap
- Uses ~25% less RG316

Approximate 9T impedance table (56% of 12T values above):

| Band | \|Z\| (ohms) | Rs (ohms) | Character   |
|------|--------------|-----------|-------------|
| 80m  | ~4900        | ~3375     | Mixed       |
| 40m  | ~6640        | ~5900     | Resistive   |
| 30m  | ~7480        | ~6975     | Resistive   |
| 20m  | ~8040        | ~7650     | Resistive   |
| 17m  | ~8270        | ~7990     | Resistive   |
| 15m  | ~8270        | ~8040     | Resistive   |
| 12m  | ~8210        | ~8015     | Resistive   |
| 10m  | ~8100        | ~7930     | Resistive   |

**Pick 12T if** you prioritize 80m margin or want to match the published
design. **Pick 9T if** you prioritize 10m/12m cleanliness, easier
winding, or less coax to cut.

---

### Design D: RG316 Coax on FT-240-43 (Reference / Not Recommended)

**Included for comparison — use only for upper HF or VHF.**

#### Specifications

| Parameter         | Value                    |
|-------------------|--------------------------|
| Core              | 1x FT-240-43            |
| Winding           | 12 turns RG316 coax     |
| Connectors        | 2x SO-239 chassis mount |
| Enclosure         | Project box              |

#### Expected Choking Impedance

| Band | Freq (MHz) | \|Z\| (ohms) | Rs (ohms) | Character     |
|------|-----------|--------------|-----------|---------------|
| 80m  | 3.5       | ~2750        | ~1300     | Mixed         |
| 40m  | 7.0       | ~4730        | ~3470     | Mixed         |
| 30m  | 10.1      | ~6090        | ~5140     | Mixed         |
| 20m  | 14.0      | ~7430        | ~6770     | Resistive     |
| 17m  | 18.1      | ~8400        | ~7930     | Resistive     |
| 15m  | 21.0      | ~8750        | ~8350     | Resistive     |
| 12m  | 24.9      | ~8950        | ~8620     | Resistive     |
| 10m  | 28.0      | ~9100        | ~8830     | Resistive     |

*Theoretical values.* Note that while the raw numbers look respectable, mix 43
is **mostly reactive below ~14 MHz** — it reflects common-mode energy rather
than absorbing it. On 80m the resistive component is only ~50% of |Z|.
Not ideal as a broadband HF choke.

---

## Verification and Testing

After building any design, measure with a NanoVNA:

1. **Connect the choke in series:** One port to the input SO-239 shield, the
   other to the output SO-239 shield. Leave the center pins unconnected.
   This measures the common-mode impedance.

2. **Sweep 1-30 MHz** and compare against the expected values above.

3. **Look for self-resonance:** A sharp peak followed by a deep dip indicates
   parasitic capacitance creating a resonance. If this falls within your
   operating range, reduce turns or increase turn spacing.

4. **Measure insertion loss:** Connect the choke inline between both ports
   (center-to-center, shield-to-shield). S21 should be very close to 0 dB
   across HF. Any significant loss indicates a winding fault.

## Placement

For an end-fed antenna, place the choke:
- **At the feedpoint** — directly after the matching unit (most effective)
- **At the shack entry** — protects station equipment (complementary to feedpoint choke)
- **Both** — belt and suspenders approach, recommended if common-mode current
  is severe

## Files in This Project

- `bom.md` — Bill of materials for each design
- `simulations/choke_impedance.py` — Python script to calculate and plot impedance curves
- `measurements/` — Place NanoVNA exports and photos here after construction
