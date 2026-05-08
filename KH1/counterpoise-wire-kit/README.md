# Counterpoise Wire Kit (Wires A and B)

Two lightweight silicone-insulated wires that form the core of the
KH1 antenna system. Used in Options 1, 2, and (combined as the
radiator) Option 3 of the go-kit.

See `../go-kit/README.md` for kit-level context and decision tree.

## Wires Built Here

| Wire | Length | λ/4 resonance | Rig end | Chain / free end |
|---|---|---|---|---|
| **A** | 13 ft | 17 m | 3 mm spade lug (M3) | in-line banana socket |
| **B** | 16.5 ft | 20 m | 3 mm spade lug (M3) | in-line banana plug |

Both wires terminate identically at the rig end. A's free end has a
banana socket; B's free end has a banana plug. The asymmetric chain
end ensures B can plug into A in Option 3 (and only in that direction)
while either wire can be used independently in Options 1 and 2.

## Roles per Option

| Option | A (13') | B (16.5') |
|---|---|---|
| **1a — single CP** | spade under ground thumbnut | OR spade under ground thumbnut |
| **1b — dual radial** | spade under ground thumbnut | spade stacked under same thumbnut |
| **2 — short EFRW** | spade on ground binding post (CP) | spade on radiator binding post |
| **3 — chained EFRW** | spade on radiator binding post; socket meets B's plug at chain joint | plug into A's socket; spade now at antenna tip |

## Materials

| Item | Spec | Qty |
|---|---|---|
| Stranded silicone-insulated wire | 28 AWG, BNTechgo or equivalent | 13 ft + 16.5 ft = ~30 ft total |
| 3 mm (M3 / #4) spade lug | crimp-style, 22-18 AWG barrel, insulated or bare | 2 |
| In-line banana socket | 4 mm, solder-on or screw-on, low-profile | 1 |
| In-line banana plug | 4 mm, solder-on or screw-on, low-profile | 1 |
| Heat-shrink tubing | 3 mm and 6 mm diameters, contrasting color | as needed |

Buying notes
- Silicone wire: BNTechgo on Amazon sells small spools in many colors. Pick a high-visibility color (orange or hi-vis green) so you can find the wire in grass.
- Spade lugs: get insulated ones if you can, or apply heat-shrink to bare crimps for strain relief.
- Banana hardware: Pomona or Mueller brand for reliable mating. Generic Amazon parts work for low power but can have inconsistent fit. Get one extra of each in case the first crimp goes wrong.

## Build Steps (per wire)

These steps work for both A and B. The only difference between them is the wire length and the choice of banana plug vs socket on the chain end.

### Step 1 — Cut and prep

1. Measure carefully. Cut to **13 ft** for Wire A or **16.5 ft** for Wire B.
2. Strip ½" of insulation from both ends.
3. Tin the stranded ends to keep them tidy during crimp/solder.

### Step 2 — Spade lug at the rig end

1. Slide a 6 mm × 1 cm piece of heat-shrink onto the wire, away from the working end (you'll position it later).
2. Insert the tinned wire end into the spade lug's crimp barrel.
3. Crimp with a wire-terminal crimper.
4. Reflow the crimp with a soldering iron and a small amount of solder for permanent strain relief.
5. Slide the heat-shrink up over the crimp barrel and shrink it. The heat-shrink should cover the bare conductor area, the crimp, and ½" of the insulated wire body.

### Step 3 — Chain-end termination (the difference between A and B)

**For Wire A — banana socket:**
1. Slide a piece of 6 mm heat-shrink onto the chain end.
2. Solder the wire's tinned end into the banana socket's solder cup.
3. Slide and shrink the heat-shrink over the socket's wire entry point and ½" of wire body.

**For Wire B — banana plug:**
1. Slide a piece of 6 mm heat-shrink onto the chain end.
2. Solder the wire's tinned end into the banana plug's solder cup.
3. Slide and shrink the heat-shrink over the plug's wire entry point and ½" of wire body.

If the banana hardware is screw-on rather than solder-on (some Pomona parts), follow that brand's instructions instead, but still apply heat-shrink for strain relief at the wire entry.

### Step 4 — Verify

1. Measure end-to-end resistance with a multimeter: should be < 0.1 Ω (basically a short).
2. Check no shorts between conductor and the heat-shrink jacket.
3. Visually inspect: heat-shrink fully covers all bare conductor and crimp barrels, no exposed copper.
4. For Wire A: insert a known-good banana plug into the socket and tug gently — should hold firmly.
5. For Wire B: insert the plug into a known-good banana socket and tug gently — should hold firmly.

### Step 5 — Wind onto winder

Figure-eight wind onto a Tufteln-style winder or a simple fishing-line spool. Both wires can share one winder if it's wide enough; otherwise use one per wire.

## Deployment Recipes

### Option 1a — Single CP (minimal carry)

1. Power on KH1, set whip slide switch to the band you'll operate (17-15 m or 20 m).
2. Pick A or B based on band:
   - 17 m primary → A (13' = 17 m λ/4, resonant)
   - 20 m primary → B (16.5' = 20 m λ/4, resonant)
   - 30 / 15 m → either works, both are off-resonance and the ATU compensates
3. Loosen the KH1 ground thumbnut.
4. Slip the wire's spade lug under the thumbnut, around the 4-40 stud.
5. Retighten the thumbnut.
6. Walk the wire out, on the ground, away from your body.
7. Tap ATU to tune. Should match within a few seconds.

Deploy time: ~30 seconds.

### Option 1b — Dual radial (slight boost)

1. Steps 1, 3, 4 from Option 1a, but stack **both** A and B spade lugs under the thumbnut.
2. Walk A out one direction, B out another (~90° apart works; opposite directions also fine).
3. Tap ATU.

Both 17 m and 20 m now have a near-resonant counterpoise simultaneously. ~1-1.5 dB improvement over single-wire on each band.

Deploy time: ~45 seconds.

### Option 2 — Short EFRW direct to BNC

This recipe needs the BNC-to-binding-post adapter from `../go-kit/bom.md`.

1. Plug the BNC adapter onto the KH1's BNC jack.
2. Loosen both binding posts on the adapter.
3. Insert Wire B's spade lug through the cross-hole on the radiator-side binding post, retighten.
4. Insert Wire A's spade lug through the cross-hole on the ground-side binding post, retighten.
5. Toss B's free end (the banana plug) over a tree branch, or just hang it from a high point.
6. Walk A out on the ground in the opposite direction.
7. Set whip slide switch to OFF (center position) so RF doesn't go to the whip.
8. Tap ATU. Should match easily on 20 m, with adequate matches on 17/15 m.

Deploy time: ~1-2 minutes.

## Care and Maintenance

- After every outing, inspect heat-shrink for cracks and the crimp areas for fatigue. Re-heat-shrink if needed.
- Don't pull on the wire by the banana plug or socket — pull on the wire body instead.
- If a spade lug pulls out of the crimp, the joint wasn't soldered properly. Cut back, redo the crimp + solder + heat-shrink.
- Silicone insulation degrades under sustained UV. If the kit lives in a window, consider replacing wires every few years.
- Banana plug/socket springs can fatigue after thousands of insertions. For your usage rate (a few outings a week max), they should last decades.

## See Also

- `bom.md` — explicit shopping list and prices
- `../micro-travel-kit/README.md` — Wire C build (twin of A) and the Option 3 chaining recipe
- `../go-kit/README.md` — overall kit philosophy
- `../efhw-portable/README.md` — Option 4 EFHW build (separate sidecar)
