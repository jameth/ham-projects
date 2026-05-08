# Circuit Diagram and Physical Layout

## Circuit diagram

```
                            ┌────────────────────────┐
                            │       49:1 UNUN        │
                            │  (FT-82-43, 21T/3T)    │
                            │                        │
                            │       T2:   21T        │
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
- The unun's full 21-turn winding is the high-Z output to the radiator.
- Comp cap goes across the entire winding (cold end ↔ ANT) per K6ARK
  reference, OR across just the primary section (cold ↔ tap) per the
  bench-grade design. K6ARK's "across full winding" placement is the
  more common QRP convention; we follow that.
- The unun cold end is BOTH the CMC's "cold side" output AND the CP
  binding post. They're the same node electrically.
```

## Physical layout — primary recommendation (K6ARK-style with binding posts)

Keeps the BNC-mounted PCB philosophy but extends it to accommodate
both toroids and adds binding-post outputs for wire swappability.

### Top view

```
                                                 ┌────────┐
                                                 │ ANT BP │
                                                 │  (red) │
   ┌──────┐                                      └────┬───┘
   │      │                                           │
   │      │  ╔══════════════════════════════════╗     │
   │ BNC  │  ║                                  ║     │
   │  F   │═>║   PCB (FR4, ~20mm × 50mm)        ║─────┘
   │      │  ║                                  ║
   │      │  ║   T1: CMC      T2: 49:1 unun     ║─────┐
   └──────┘  ║   (vertical    (vertical to      ║     │
             ║    to PCB)      PCB, opp. side)  ║     │
             ║                                  ║   ┌─┴──────┐
             ║                                  ║   │ CP BP  │
             ╚══════════════════════════════════╝   │ (black)│
                                                    └────────┘
```

Key dimensions (target):
- PCB: 20 mm × 50 mm × 1.6 mm FR4
- T1 (FT-50-43 bifilar): ~13 mm OD × 5 mm height; mounts upright, 5 mm
  from BNC end of PCB
- T2 (FT-82-43 unun): ~21 mm OD × 6.4 mm height; mounts upright,
  centered on the PCB, 25 mm from BNC end
- Cores stand on opposite faces of the PCB to minimize coupling
  (T1 above, T2 below — verify with sim if needed)
- Enclosure: 1" diameter heat-shrink + small Hammond shroud OR a
  3D-printed snap-shell sized to the PCB (~25 × 55 × 18 mm)

### Side view (cross-section)

```
              T1 (CMC, FT-50)                T2 (unun, FT-82)
              ┌──┐                           ┌────┐
              │  │                           │    │
   ╔══════════╪══╪═══════════════════════════╪════╪═══════════╗
   ║ ┌─────┐  └──┘                           └────┘           ║
   ║ │ BNC │   PCB top                                        ║
   ║ │     │                                                  ║
   ║ │     │   PCB bottom (comp cap SMT here)       BPs here  ║
   ║ └─────┘                                                  ║
   ╚══════════════════════════════════════════════════════════╝
                                                              ▲
                                                   wire outputs
```

The two toroids are physically separated by ~15 mm of PCB. Mounting
them on opposite PCB faces ensures the unun's main winding doesn't
share a magnetic path with the CMC's bifilar.

### PCB pads (top view, schematic-level)

```
   ┌────────────────────────────────────────────────────┐
   │   [BNC ctr pad]  [BNC gnd1] [BNC gnd2]             │
   │         │             │          │                 │
   │         │             └──────────┴── shield        │
   │         │                                          │
   │   T1 input pads ──┐                                │
   │   (BNC ctr in)    │                                │
   │                   │   T1 output pads ──┐           │
   │   T1 shield in ───┘  (to T2 tap)       │           │
   │                                        │           │
   │                              T2 tap pad (50Ω in)   │
   │   T1 mounting holes (2 × 0.8 mm)                   │
   │                                                    │
   │                              T2 cold end pad       │
   │                                  │    │            │
   │                              ┌───┘    └─── to CP BP│
   │                              │                     │
   │                          T2 ANT pad ── to ANT BP   │
   │                                                    │
   │   T2 mounting holes (2 × 1.0 mm)                   │
   │                                                    │
   │   [comp cap pads, BOTTOM SIDE — across T2 winding] │
   │                                                    │
   │   [Strain relief holes for wires going to BPs]     │
   └────────────────────────────────────────────────────┘
```

## Physical layout — alternative (Hammond box)

If you'd rather have a rigid weatherproof case at a small weight cost
(~10 g extra), use Hammond 1551KFLBK (50 × 35 × 20 mm). Same internal
PCB; instead of heat-shrink, the PCB mounts inside the box on standoffs.

```
   ┌──────────────────────────────────┐
   │  ┌────┐                          │
   │  │BNC │   ┌──┐    ┌────┐         │
   │  │    │   │T1│    │ T2 │  [ANT●] │
   │  │    │   │  │    │    │  [CP ●] │
   │  └────┘   └──┘    └────┘         │
   │                                  │
   └──────────────────────────────────┘
   Hammond 1551KFLBK, ABS plastic
   BNC and BPs panel-mounted through drilled holes
   PCB on M3 standoffs
```

Tradeoff: ~10 g heavier, rigid, weatherproof when sealed with a thin
bead of silicone around connectors. Easier to mount on a backpack
strap or tripod. Better choice if the unit will see weather or rough
handling.

## Recommended primary build

Go with the **K6ARK-style heat-shrink** approach as the primary build:

- Closer to the user's K6ARK inspiration
- Lighter (~25 g vs ~35 g for Hammond)
- Smaller form factor
- Easier to source (no Hammond box order)

Add binding posts (or banana jacks at minimum) instead of permanent
soldered wires, so you can swap radiators without re-soldering. The
binding posts mount on a small tab of PCB that protrudes past the
heat-shrink at the antenna end, giving you a clean wire-attachment
point without breaking the heat-shrink seal.

## Winding instructions

### T1: CMC — 12T bifilar on FT-50-43

1. Cut two ~12-inch lengths of 26 AWG enamel magnet wire, contrasting
   colors (e.g., red and blue). Strip and tin both ends of each.
2. Twist the two wires loosely together, ~3-4 twists per inch.
3. Wind 12 turns of the bifilar pair through the FT-50-43 core.
   Each pass through the center counts as one turn.
4. Spread turns evenly around the core — about 30° per turn.
5. Identify the windings: the **start of red** is the BNC center input.
   The **start of blue** is the BNC shield input. The **end of red**
   goes to the unun tap (50 Ω input). The **end of blue** is the unun
   cold end (CP). Use a multimeter for continuity to verify.

### T2: Unun — 21T autotransformer with 3T tap on FT-82-43

This is the K6ARK 21T/3T config:

1. Cut a single ~28-inch length of 22 AWG enamel magnet wire. Strip
   and tin both ends.
2. Wind 21 turns through the FT-82-43 core. Spread evenly (~17° per
   turn).
3. After the **3rd turn from the start**, expose a small tap by
   carefully sanding the enamel off a 3 mm section without breaking
   the wire. This is the 50-Ω tap.
4. The **start** of the winding is the cold end (connects to BNC
   shield via the CMC, AND to the CP binding post).
5. The **3T tap** is the 50-Ω input (connects to the BNC center via
   the CMC's red-end output).
6. The **end of the winding** (after 21T) is the high-Z output (to
   the ANT binding post).
7. Solder a 100 pF NP0 1.5 kV ceramic cap from the **cold end** to
   the **ANT end** (across the full 21-turn winding) — this is the
   compensation cap.

### Verification before final assembly

With a multimeter:
- BNC center to BNC shield: open circuit (CMC's bifilar should not
  short)
- BNC center to T1 red-end output: continuity (~ohms of wire)
- T1 red-end output to T2 3T tap: continuity (your interconnect)
- T2 3T tap to T2 ANT end: continuity through the rest of the
  winding (low ohms)
- T2 ANT to comp cap to T2 cold end: continuity through the cap
  (high impedance at DC; capacitor discharges any test current)

With a NanoVNA:
- 50 Ω port at BNC, 2450 Ω resistive load at ANT/CP terminals
- Sweep 5-25 MHz
- Look for SWR < 2:1 across all KH1 bands (40/30/20/17/15)
- If 15 m SWR is high (> 2.5), try 82 pF or 120 pF comp cap variants
- If 40 m SWR is high, check toroid winding tightness or core orientation

## Strain relief

Both wires (radiator and CP) need strain relief at the unit. Two
options, in increasing rigor:

| Option | Method | Effort |
|---|---|---|
| Easy | Heat-shrink tubing over the wire entry, sleeved through a small PCB hole | minutes |
| Better | Knotted wire end inside the enclosure, plus heat-shrink boot outside | 5-10 min |
| Best | Crimped ferrule + small chassis-mount strain-relief grommet | 15 min, requires more parts |

K6ARK uses option 1 (heat-shrink only). For an integrated unit that
might see more handling, option 2 is worth the extra effort.
