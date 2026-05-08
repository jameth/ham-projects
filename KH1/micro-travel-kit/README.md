# Micro Travel Kit (Wire C + Option 3 Chaining Notes)

The Option 3 add-on. Provides a third wire (C, dedicated counterpoise)
and the deployment recipe for the chained 29.5' magic-length EFRW that
covers all 5 KH1 bands with no transformer.

Inspired directly by Eric WD8RIF's "KH1 Micro Travel Kit" but adapted
to share wires with the rest of the go-kit rather than carrying a
single dedicated 33' wire with fold-back insulator and 2' extension.

Reference: https://wd8rif.com/kh1_micro_travel_kit.htm

See `../go-kit/README.md` for kit-level context.

## What's in This Kit

| Item | Purpose |
|---|---|
| Wire C — 13 ft | dedicated counterpoise for Option 3 (since A is being used as the radiator's first segment) |
| Small winder | tangle-free storage for Wire C |

That's it. Wires A and B (in the `../counterpoise-wire-kit/`) provide the
two radiator segments that chain to make 29.5'.

## Wire C Specs

| Spec | Value |
|---|---|
| Length | 13 ft (matches Wire A) |
| Wire | 28 AWG silicone-insulated stranded, hi-vis color |
| Rig end | 3 mm spade lug (M3 / #4) |
| Free end | small soldered eyelet |

The eyelet at the free end has three purposes:

1. **Wire-end finishing** — keeps stranded copper from fraying after repeated deployments
2. **Anchor / find point** — accept a tent stake to peg the CP end down, or accept a hi-vis ribbon for visibility
3. **Optional elevation point** — hook over a low twig or rock to lift the CP end ~6" off the ground for slight efficiency improvement

## Build Steps

Wire C is essentially identical to Wire A except for the free-end termination. Follow the build steps in `../counterpoise-wire-kit/README.md` Step 1 and Step 2 (cut, prep, spade lug at the rig end). Then:

### Step 3 — Eyelet at the free end

1. Slide a 6 mm × 1.5 cm piece of heat-shrink onto the wire.
2. Strip 1" of insulation at the free end.
3. Fold the bare stranded conductor back over itself to form a small loop ~5 mm in diameter.
4. Pinch the fold tight against the wire body.
5. Solder the entire fold to lock the loop closed and bond it to the wire body.
6. Slide the heat-shrink up over the soldered fold, leaving the small loop exposed at the very tip.
7. Shrink. The result: a small soldered eyelet at the wire tip, with heat-shrink strain relief.

Alternative: crimp a small #4 ring terminal onto the bare end instead. Same function, slightly cleaner appearance, costs ~$0.10 each.

### Step 4 — Verify and wind

1. Tug-test the eyelet — should not pull off the wire.
2. Check no shorts in the heat-shrink area.
3. Wind onto the small winder for storage.

## Option 3 Deployment Recipe (the Chained 29.5' EFRW)

This is where the kit comes together. You need:

- BNC-to-binding-post adapter (in `../go-kit/`)
- Wire A (13', from `../counterpoise-wire-kit/`)
- Wire B (16.5', from `../counterpoise-wire-kit/`)
- Wire C (13', this kit)
- A tree branch, mast, or other support point ~25-30 ft up

### Setup sequence

1. **Mount the adapter.** Plug the BNC-to-binding-post adapter onto the KH1's BNC jack. Loosen both binding posts.

2. **Connect the radiator chain at the rig.** Insert Wire A's spade lug through the cross-hole on the radiator-side binding post. Retighten.

3. **Connect the counterpoise.** Insert Wire C's spade lug through the cross-hole on the ground-side binding post. Retighten.

4. **Walk Wire A out.** Roughly 13 ft toward your throw point. Wire A's free banana socket dangles in the air at the 13' point.

5. **Chain Wire B onto Wire A.** Plug Wire B's banana plug into Wire A's banana socket. The chain joint is now mid-air at the 13' point along the wire run.

6. **Toss Wire B's free end** (the antenna tip, currently the spade lug) over the tree branch using a throw bag or weighted line. The total radiator length from the rig to the tip is now 29.5' (13' of A + 16.5' of B).

7. **Deploy Wire C** in roughly the opposite direction from the radiator, lying on the ground. Optionally peg down the eyelet end with a tent stake.

8. **Set the whip slide switch to OFF (center position)** so RF doesn't try to feed the unused whip.

9. **Tap ATU.** Should find a match within 1-4 seconds on any KH1 band.

Deploy time: 3-5 minutes including the throw.

### Why we chain instead of using WD8RIF's fold-back design

Eric WD8RIF's original kit uses a single 33' wire with a button insulator at 29' (fold-back point) and a banana socket at the 33' tip (for a 2' extension to reach 35'). Three selectable lengths from one wire.

Our approach uses two wires (A: 13' and B: 16.5') chained to make a single 29.5' length. Tradeoffs:

| Aspect | WD8RIF (one 33' wire) | Our setup (chained 13' + 16.5') |
|---|---|---|
| Extra hardware | button insulator + 2' extension wire + banana hardware on one wire | banana socket on A + plug on B (parts already in core kit) |
| Length flexibility | three options (29 / 33 / 35) via fold or extend | one length (29.5') |
| Why three lengths matter | 33' lands on 20 m λ/2; need 29' or 35' to fix 20 m | 29.5' is already off λ/2 on every KH1 band |
| Wire count | 1 (radiator) + 1 (CP) = 2 | 2 (A + B chained as radiator) + 1 (C as CP) = 3 |
| Total wire length | 33' + 13' = 46 ft + 2' ext | 13' + 16.5' + 13' = 42.5 ft |
| Total weight | ~10 g | ~10 g (slightly less wire, similar weight) |
| Wire reuse | dedicated single radiator | A and B serve Options 1 and 2 also |

Our approach pays for itself the moment we use Wire A as a counterpoise (Option 1 or 2) or Wire B as a 20 m radiator (Option 2). One pair of wires serves three options.

The WD8RIF design is brilliant for a dedicated single-purpose kit. Ours is brilliant for a multi-purpose kit. Different optimization targets, both valid.

### 29.5' Band Behavior

Verified clean across every KH1 band:

| Band | 29.5' is electrically | Behavior |
|---|---|---|
| 40 m | 0.22 λ (short, capacitive) | tunable; ATU works moderately hard |
| 30 m | 0.31 λ (mid-Z, past λ/4) | tunable cleanly |
| 20 m | 0.44 λ (well off λ/2 = 33.8') | tunable cleanly |
| 17 m | 1.09 × λ/2 (just past peak) | tunable cleanly, mid-Z inductive |
| 15 m | 0.63 λ (between λ/2 and 3λ/4) | tunable cleanly |

No fold-back required. The 29' magic length is the standard "always-tunable" EFRW length, and 29.5' is electrically identical (within 2%).

## Care Notes

- After every outing, check the chain joint for wear on A's socket and B's plug. A loose-fitting plug means worn springs in the socket. Replace either component if signal becomes intermittent.
- Wire C's eyelet sees mechanical stress when staked down; inspect for the soldered fold breaking apart and resolder if needed.
- Chain joint connection is the most likely failure point in this option. Keep a spare in-line banana plug+socket pair in the kit pouch as field repair material.

## See Also

- `bom.md` — Wire C parts list
- `../counterpoise-wire-kit/README.md` — Wires A and B (the radiator segments for Option 3)
- `../go-kit/README.md` — overall kit philosophy and decision tree
- WD8RIF KH1 Micro Travel Kit: https://wd8rif.com/kh1_micro_travel_kit.htm — the inspiration
