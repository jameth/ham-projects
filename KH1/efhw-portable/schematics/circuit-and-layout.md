# Circuit Diagram and Physical Layout

## Circuit diagram

```
                            ┌────────────────────────┐
                            │         UNUN           │
                            │  (FT-50-43, 23T total: │
                            │   3T primary + 20T more,│
                            │   ratio 58.8:1)         │
                            │       T2:   23T        │
                            │           ┌────►───────┼──── ANT (radiator BP)
                            │     full  │            │
                            │   winding │  comp.cap  │
                            │           │ ┌──┐ 100p  │
   BNC  ┌──── 1:1 CMC ──────┼─►─tap@3T──┼─┤  ├─►ant  │
   in   │  (FT-50-43)       │           │ └──┘       │
   ●───►│  12T bifilar      │           │            │
        │                   │           │            │
        │                   │           ▼            │
        ●───────────────────┼──── COLD ─────────────►┼──── CP  (counterpoise BP)
   shield                   │     end                │
                            └────────────────────────┘

Notes:
- The CMC is wound as a current-mode (bifilar) choke. Both BNC center
  conductor and BNC shield pass through the toroid as one bifilar pair.
- The unun's tap (3T from cold end) is the 50-Ω input.
- The unun's full 23-turn winding is the high-Z output to the radiator.
  Transformation ratio is (23/3)² = 58.8:1; matched load is ~2940 Ω.
- Comp cap goes across the entire winding (cold end ↔ ANT) per K6ARK
  reference, OR across just the primary section (cold ↔ tap) per the
  bench-grade design. K6ARK's "across full winding" placement is the
  more common QRP convention; we follow that.
- The unun cold end is BOTH the CMC's "cold side" output AND the CP
  binding post. They're the same node electrically.
```

## Physical layout — primary build (K6ARK-style in-line, heat-shrunk)

No PCB, no enclosure box. The whole assembly is a heat-shrunk bundle
that hangs directly off a BNC male connector, exactly like the K6ARK
QRP EFHW kit. The only difference from the K6ARK kit is the added
CMC toroid in series between the BNC and the unun.

### The bundle

```
   BNC male                                              radiator
   plug          T1 (CMC)           T2 (unun)            pigtail
   ┌──┐         ┌────────┐         ┌────────┐         ──────────►
   │  │═════════│   CMC  │═════════│  unun  │═════════
   │██│  short  │ 12T    │  short  │  23T   │         ──────────►
   │  │ jumpers │ bifilar│ jumpers │  3T tap│         counterpoise
   └──┘         └────────┘         └────────┘         pigtail
    │              │                  │
    │              └── inner HS ──────┘
    │
    └─────── outer heat-shrink, 3/4"-1" × ~3-4" ───────►
```

### Key dimensions

- Bundle length: ~3-4 inches (BNC body to wire exit)
- Bundle diameter: ~3/4" (19 mm)
- Total weight: ~15-18 g
- Both toroids axis-aligned with the bundle (donut holes facing along
  the bundle direction, not sideways — see gotcha #1 below)

### Construction sequence

1. **Wind both toroids first.** Don't terminate anything to the BNC
   yet. Continuity-check each winding on the bench (CMC red-to-red,
   blue-to-blue, red-to-blue open; unun start-to-end continuous,
   tap shows ~14% of full-winding resistance). Catch winding errors
   before they're soldered into a bundle.

2. **Pre-tin the BNC** center pin and shield tab/cup. Flux on, solder
   on, let cool. The pre-tinning is what makes step 3 survivable
   when you only have ~5 mm of magnet wire to play with.

3. **Solder CMC start leads to the BNC:**
   - CMC red start → BNC center pin
   - CMC blue start → BNC shield tab/cup
   - Keep leads ~5-8 mm so the CMC sits close to the BNC body but
     you can still position it.

4. **Slide inner heat-shrink** (1/2" × ~1.5") **over the bundle from
   the wire end.** Park it past T1 for now. You'll slide it back over
   the BNC-to-CMC junction in step 9 for joint protection.

5. **Solder the inter-toroid jumpers:**
   - CMC red end → unun 3T tap (50 Ω input)
   - CMC blue end → unun cold end (start of unun winding)
   - Target **10-15 mm** jumper length (eyeball as ~1/2 inch). Shorter
     than ~8 mm risks magnetic coupling between the two toroids
     (fringe-flux interaction); longer than ~20 mm adds enough stray
     inductance to start shifting the 15 m comp-cap tuning. See
     gotcha #2 below.

6. **Solder the compensation cap** across the unun cold end and ANT
   end. Use an **axial-leaded NP0/C0G ceramic cap** (100 pF, 1.5 kV)
   since there's no PCB for an SMT part. Bridge it across the toroid
   body and insulate the cap leads with a tiny piece of heat-shrink.

7. **Solder the output pigtails:**
   - Unun ANT end → ~4" of 26 AWG silicone stranded wire (radiator)
   - Unun cold end → ~4" of 26 AWG silicone stranded wire (CP)
   - Use stranded silicone, not magnet wire. The pigtails need flex
     tolerance where they exit the bundle.

8. **Tie strain-relief knots** in both output pigtails *inside* what
   will become the bundle interior, about 1" back from where they'll
   exit the outer heat-shrink. The knot transfers wire-pull stress
   to the heat-shrink instead of the solder joints.

9. **Slide outer heat-shrink** (3/4" or 1" × 3-4") over the bundle
   from the wire end. Overlap ~5 mm onto the BNC body at one end,
   leave ~10 mm of clearance past the pigtail exits at the other.

10. **Shrink, BNC-end first.** Heat gun on low, work toward the
    wire end. The outer HS locks everything in place permanently.

### Inter-joint topology (point-to-point construction)

Without a PCB, several wires converge on each solder joint:

| Joint | Wires that meet here |
|---|---|
| BNC center pin | CMC red start |
| BNC shield | CMC blue start |
| 50 Ω input node | CMC red end + unun 3T tap |
| Cold-end node | CMC blue end + unun start + comp cap (-) + CP pigtail |
| ANT-end node | unun end (after 23T) + comp cap (+) + radiator pigtail |

The cold-end node has **four wires converging**. Twist all four
together first, then solder once. Soldering them one at a time gives
a cold solder joint that will fail under flex.

### Gotchas specific to two-toroid in-line builds

These don't apply to a single-toroid K6ARK kit but matter when you
add the CMC in series:

1. **Toroid axis orientation.** Both toroids must have their magnetic
   axis parallel to the bundle axis — donut holes facing along the
   bundle direction. In that orientation each toroid's magnetic field
   is circumferential to itself and doesn't couple to the other. If
   you position one with its axis perpendicular (lying on its side),
   mutual coupling can reach 5-10% and detune the unun. Quick check:
   both toroids should look like the windings pass *through* the
   bundle direction, not around it.

2. **Inter-toroid jumper length: target 10-15 mm.** Two competing
   concerns set this window:
   - **Too short (<8 mm)**: the two toroids' fringe fields couple.
     With axis-aligned cores, coupling at 1 OD center-to-center
     separation (~13 mm CTC, ~8 mm jumper) is k ≈ 0.005-0.01.
     Below that, k climbs past 0.02-0.05 and starts to detune the
     49:1 ratio and weaken the CMC's choking action. At QRP this
     shows up as a 0.2-0.5 SWR-unit shift on 15 m.
   - **Too long (>20 mm)**: the jumpers' stray inductance (~1-1.5
     nH/mm) starts to interact with the 100 pF comp cap. A 25 mm
     jumper adds ~3 Ω of series reactance at 21 MHz — a ~4%
     perturbation of the comp-cap tuning. Tolerable but measurable.

   Sweet spot is ~12 mm. The jumpers should be unbalanced single
   wires (not bifilar) — this is normal point-to-point construction.

3. **Four-wire cold-end joint.** Twist before soldering. The CP
   pigtail, CMC blue-end, unun start, and comp-cap cold lead all
   share this node.

4. **No PCB means no mounting points.** Toroids float, held only
   by the windings and jumpers. They will shift slightly during
   shrinking. Set the parallel-axis orientation deliberately in
   step 9 before heat-shrinking, so any drift stays along the
   bundle axis rather than rotating into a perpendicular orientation.

5. **BNC strain path is direct.** Every yank on the antenna wire
   pulls on the BNC solder joints through the entire bundle. The
   strain-relief knots in step 8 are non-optional.

## Physical layout — alternative (Hammond box for weather/handling)

If the unit will see permanent outdoor mounting, wet POTA activations,
or rough handling that the heat-shrink bundle can't survive, use the
Hammond 1551KFLBK (50 × 35 × 20 mm). Trade ~10-15 g of weight for a
rigid, openable, serviceable shell.

```
   ┌──────────────────────────────────┐
   │  ┌────┐                          │
   │  │BNC │   ┌──┐    ┌────┐         │
   │  │ F  │   │T1│    │ T2 │  [ANT●] │
   │  │    │   │  │    │    │  [CP ●] │
   │  └────┘   └──┘    └────┘         │
   │                                  │
   └──────────────────────────────────┘
   Hammond 1551KFLBK, ABS plastic
   BNC and BPs panel-mounted through drilled holes
   Toroids point-to-point or on a small piece of perfboard
```

Construction is similar to the in-line build but with:

- **Panel-mounted BNC female** (chassis-mount) with insulating
  shoulder washers — center conductor isolated from the metalwork
  if any (the Hammond ABS body is non-conductive but adding washers
  keeps the convention consistent)
- **Binding posts panel-mounted** at the wire-exit end — radiator and
  CP become field-swappable
- **Toroids** mounted point-to-point inside the box, or on a 20×30 mm
  scrap of perfboard for stability. Hot-glue or silicone after testing.
- **Seal the BNC and BP holes** with a thin bead of silicone for
  weather resistance after final assembly

Use this variant when:

- The unit will live outdoors permanently (deck-mounted EFHW for a
  base station)
- You operate in wet conditions and don't want a heat-shrunk bundle
  hanging in the rain
- You want field-swappable radiators via binding posts
- You expect to open the unit later for repair, modification, or
  comp-cap retuning

## Recommended primary build

For the KH1 Edgewood pedestrian-mobile use case, **go with the in-line
K6ARK-style bundle** above. It matches the rig's portable mission,
weighs ~15-18 g, costs ~$28, and hangs directly off a BNC adapter on
the rig.

Pick the Hammond box only if the unit needs to be openable or
weatherproof. For a primary KH1 antenna that lives in a pocket and
deploys to a tree branch, hardwired heat-shrink is the right call.

Radiator and CP termination:

- **Hardwired pigtails** (K6ARK standard, recommended): radiator and
  CP wires are crimped/spliced to permanent ~4" pigtails that exit
  the bundle. Lower weight, lower failure rate, how the kit ships.
- **Binding posts** add ~3 g, ~$5, and a small flap of perfboard or
  terminal carrier outside the heat-shrink. Worth it only if you
  genuinely swap radiator lengths between operations.

For 5 W KH1 work with a fixed ~65 ft EFHW radiator, hardwired is the
right call.

## Winding instructions

### T1: CMC — 12T bifilar on FT-50-43

1. Cut two ~12-inch lengths of 26 AWG enamel magnet wire, contrasting
   colors (e.g., red and blue). Strip and tin both ends of each.
2. Pair the two wires. Either **lightly twist** at ~2-3 TPI (better
   mechanical stability while winding the small FT-50 ID) OR **lay them
   parallel side-by-side** per the K6ARK kit recipe. Electrically
   these are equivalent at HF: |Z_CM| differs by <10% across 7-21 MHz
   because self-resonance sits ~90-120 MHz in either case, well above
   our working bands. Pick whichever you find easier to feed through
   the 7 mm core ID. The twisted variant tends to stay together;
   parallel-laid is slightly easier to wind flat against the core but
   needs more attention to keep the wires from splaying apart.
3. Wind 12 turns of the bifilar pair through the FT-50-43 core.
   Each pass through the center counts as one turn.
4. Spread turns evenly around the core — about 30° per turn.
5. Identify the windings: the **start of red** is the BNC center input.
   The **start of blue** is the BNC shield input. The **end of red**
   goes to the unun tap (50 Ω input). The **end of blue** is the unun
   cold end (CP). Use a multimeter for continuity to verify.

### T2: Unun — 23T autotransformer with 3T tap on FT-50-43

This is the K6ARK QRP kit "recommended general use" recipe: 3 turns
primary, pull tap, then 20 more turns continuous. Total 23 turns.
Transformation ratio (23/3)² = **58.8:1** (matched load ~2940 Ω).

1. Cut a single ~23-inch length of 24 AWG enamel magnet wire (or 22
   AWG if you prefer the extra ruggedness and don't mind tighter
   winding on the FT-50 ID). Strip and tin both ends.
2. **Wind the first 3 turns** through the FT-50-43 core (primary).
   Keep these turns snug to one section of the core (~40-60° of the
   circumference) — don't spread them yet.
3. **Pull a ~3/4" tap loop** after turn 3, before starting turn 4.
   Twist the loop once near its base to keep it from unwinding. This
   is the 50 Ω input tap.
4. **Wind 20 more turns** continuous from turn 3 (don't break the
   wire). Spread these 20 turns evenly around the remaining ~300° of
   the core circumference. Total winding is now **23 turns**.
5. Scrape the enamel off just the tip of the tap loop and tin it.
6. The **start** of the winding (before turn 1) is the cold end
   (connects to BNC shield via the CMC, AND to the CP pigtail).
7. The **3T tap** is the 50 Ω input (connects to the BNC center via
   the CMC's red-end output).
8. The **end of the winding** (after the 20-more turns, turn 23) is
   the high-Z output (to the ANT pigtail).
9. Solder a 100 pF NP0 1.5 kV ceramic cap from the **cold end** to
   the **ANT end** (across the full 23-turn winding) — this is the
   compensation cap. The 100 pF value is correct because leakage
   inductance depends only on the 3T primary (constant across 21/23/24T
   variants).

**Alternative turn counts** (per K6ARK's range of 19-24 more turns):

| Pattern | Total turns | Ratio | Matched load | Use when |
|---|---|---|---|---|
| 3T + 18 more | 21T | 49:1 | 2450 Ω | True 49:1 reference; older docs |
| **3T + 20 more** | **23T** | **58.8:1** | **2940 Ω** | **K6ARK recommended (default)** |
| 3T + 21 more | 24T | 64:1 | 3200 Ω | K6ARK image-count alternative |
| 3T + 24 more | 27T | 81:1 | 4050 Ω | Elevated EFHW with high feedpoint Z |

The sim shows all of these give identical 40 m IL (1.40 dB) when
matched to their own natural load. The choice is about which EFHW
feedpoint impedance you're targeting, not about transformer
performance.

### Verification before final assembly

With a multimeter:
- BNC center to BNC shield: open circuit (CMC's bifilar should not
  short)
- BNC center to T1 red-end output: continuity (~ohms of wire)
- T1 red-end output to T2 3T tap: continuity (your interconnect)
- T2 3T tap to T2 ANT end (turn 23): continuity through the remaining
  20 turns of the winding (low ohms)
- T2 ANT to comp cap to T2 cold end: continuity through the cap
  (high impedance at DC; capacitor discharges any test current)
- T2 cold end (turn 0) to T2 tap (turn 3): continuity through 3
  turns of wire (very low ohms)
- T2 tap (turn 3) to T2 ANT end (turn 23): should be ~6.7× the
  resistance of cold-to-tap (since 20T vs 3T of the same wire)

With a NanoVNA:
- 50 Ω port at BNC, **2940 Ω resistive load** at ANT/CP terminals
  (matched load for 23T/3T = 58.8:1). See README "Acceptance Criteria"
  for how to build this load from common resistor values.
- Sweep 5-25 MHz
- Look for SWR < 2:1 across all KH1 bands (40/30/20/17/15)
- If 15 m SWR is high (> 2.5), try 82 pF or 120 pF comp cap variants
- If 40 m SWR is high, check toroid winding tightness or core orientation
- Note: if you test with a 2450 Ω load (true 49:1 reference) instead
  of 2940 Ω, baseline SWR will be ~1.2:1 even with a perfect 23T/3T
  transformer due to the load mismatch. Use the correct load value.

## Strain relief

For the in-line build, strain relief is built into the assembly
sequence rather than added as a separate step:

| Location | Method |
|---|---|
| BNC-to-CMC joint | Inner heat-shrink (1/2") sleeves over the BNC body and the CMC leads (construction step 4) |
| Pigtail exits | Knot tied in each pigtail inside the bundle (step 8), captured under the outer heat-shrink (step 9) |
| Radiator far end | Loop or ring terminal in the wire — never pull on the pigtail directly when retrieving the antenna |

These are not optional. The in-line build has no PCB to absorb pull
forces, so the heat-shrink + internal-knot system is what protects
the BNC solder joints. Inspect the pigtail-knot region after every
50-100 deployments — if the heat-shrink shows wear at the wire exit,
add a second short outer sleeve over that section before it fails.

For the Hammond box variant: knot inside the box, plus heat-shrink
over the wire entry on the outside. Easier to inspect, and the
binding-post version sidesteps the issue entirely (the pigtail is
the radiator wire itself, replaceable when worn).
