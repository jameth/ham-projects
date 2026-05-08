# KH1 Community Research — Gemini Deep Research Report

Date: 2026-05-02
Source: Gemini Deep Research (128 minute run)
Output JSON: `/home/jameth/.config/gemini-mcp/output/3ff95041b93ab3f4/deep-research-2026-05-03T02-07-56-244Z.json`

> **Note on accuracy:** This is a synthesis from third-party forum posts,
> blogs, and YouTube transcripts. Verify before building. A few claims
> below conflict with the official manual rev B7 (flagged inline).

## Key Findings

### Paradigm
- KH1 = HF hand-talkie. CW-only by design (Wayne Burdick / N6KR's stated philosophy from FDIM 2024 / Pacificon).
- Internal ATU is highly tolerant; PA can run into ~4:1 SWR safely per N6KR on groups.io. Don't obsess about 1:1.

### Firmware milestones
- **1.27** added `FOnn;` CAT command (1-Hz VFO step) → enables FT8 via SOTACAT, plus added `SW TONES` audio CW UI and variable `QSK DELAY`.
- VFO knob hold-toggle to 1 MHz / 100 kHz steps in BAND/MODE group.

---

## 1. Hardware Modifications

### KHPD1 magnetic paddle mod (most-cited)
- Replace internal spring with two **5 mm × 2 mm neodymium magnets** in opposition.
- Drill existing spring retention holes slightly with **#9 drill bit**.
- Result: crisp Begali / Vibroplex-like break-over feel. Eliminates the "spongy" complaint.

### Battery elimination ("hollow-out") mod — N6MTB
- 3D-print a dummy tray (~14 g) to replace the KXBT2 (~90 g).
- Saves 76 g; tray doubles as storage for backup TinyPaddle and foam.
- Power exclusively via external LiFePO4 or USB-C PD.

### Counterpoise material swap
- Replace stiff factory 13' wire with **28 AWG silicone-insulated wire** (e.g., BNTechgo) terminated with crimped + soldered fork connector.
- Saves ~10 g, eliminates memory-effect tangle.

### Knob and switch upgrades
- Tufteln red aluminum knurled knob caps for tactile feedback.
- 3D-printed power switch guard prevents accidental in-pack power-on.

### Calibration touch-ups (every couple months)
- `MENU:ADJ SWR` (null SWR bridge — needs cover off, trim C80)
- `MENU:ADJ WMTR` (against accurate external wattmeter)
- `MENU:ADJ TIME` and `ADJ RTC` for log timestamp accuracy

---

## 2. 3D-Printed Accessories

| Part | Designer | Notes |
|---|---|---|
| BaseCap + AntennaCap | user "goss" (Thingiverse) | PETG, 0.20 mm layer, scale 101-102% |
| Mini Screwdriver Loading Coil | Adam Kimmerly (Printables) | continuous-tune coil with 26 AWG magnet wire + M4 heat-set insert; gets the whip down to 40 m without AXE1 |
| Kneeboard Field Desk | user "_" (Printables); Tufteln sells commercial version | strap-to-thigh, hands-free cockpit |
| TinyPaddle KH1 stabilizer | community | shroud that braces N6ARA TinyPaddle against the KH1 chassis to protect the 3.5 mm jack from lateral load |
| 1/4-20 tripod adapters | various | KH1 + AX1/AXE1 onto camera tripods |

---

## 3. Upgrades

### Paddles / keys
- N6ARA TinyPaddle (direct PCB plug — needs the stabilizer mod)
- BaMaKeY TP-III, SP4 magnetic, PUTIKEEG "Grasshopper" for stationary use
- K6ARK pressure paddle (zero-travel, immune to dirt/moisture)

### External power
- KH1 accepts 8-15 V at the DC jack; jacks are diode-OR'd with internal battery.
- USB-C **PD trigger cable** (Birdcord 12V, Acroname) is the right path. Cheap 5V→12V boosters fail thermally under TX (~12 W).
- Power banks called out: Anker, INIU, BioLite Charge 80 PD.
- External supply > 12.5 V → automatically charges KXBT2 in background via KHIBC1 even with the radio in operation.

### Audio
- Internal speaker is ~25 × 16 mm, ≈0.5 W peak — easily lost in wind.
- Community favors passive in-ear monitors (IEMs):
  - Sony ICD-UX series
  - Modified Koss "The Plug" with super-glued tri-flange tips

---

## 4. Antennas

### Factory whip (4-foot telescoping)
- Electrically very short: ~0.05 λ on 40 m, ~0.17 λ on 15 m.
- Internal slide switch picks 17-15 m loading or 20 m loading or BYPASS.
- Sub-25-second deployment is the value proposition. Efficiency is bad — pair with effort.

### EFHWs
- KM4ACK 40-10 m EFHW — popular, EDC-friendly.
- K6ARK Mini 49:1 / 9:1 — micro-toroid (FT-50-43) matching networks the size of a BNC connector. WA9STI logged 300+ POTA contacts on KH1 + 40 m EFHW.

### Random wire (the most lauded compact setup)
- **Tufteln "no transformer" setup**: 15' radiator + 7.5' counterpoise straight to BNC via a binding-post adapter. ATU finds matches 40-15 m.
- **K4SWL speaker-wire**: ~71' radiator + 17' counterpoise straight to BNC binding posts. Excellent on 30 m and 20 m.

### Verticals (WB3GCK)
- 12' wire vertical with T106-2 toroid base loading on 20 m; KH1 tunes 15/17 m without the coil.
- 19' vertical (resonant 40/30, random 20-15) + four 12.5' radials → ATU brings SWR < 2:1 easily.

### Mag-loops
- ~24" driven loop of 1/4" copper inside a main loop tuned by 5-200 pF variable cap.
- KH1 works well with loops, but disable internal ATU to prevent cascading tune faults.

---

## 5. Counterpoise / Grounding

### Quarter-wave targets vs. factory wire

| Band | Theoretical λ/4 | Factory CP | Note |
|---|---|---|---|
| 40 m | ~33.0 ft | 33' (with AXE1) | resonant |
| 30 m | ~23.5 ft | 13' or 33' | 33' acts as random-wire ground |
| 20 m | ~16.5 ft | 13' | slight capacitive load, ATU absorbs |
| 17 m | ~13.0 ft | 13' | resonant — high efficiency |
| 15 m | ~11.0 ft | 13' | slight inductive, ATU corrects |

### WD8RIF KH1 Micro Travel Kit (corrected from WD8RIF's own site)

**This is an EFRW antenna setup using the BNC jack, not a counterpoise mod.**
The original Gemini summary mis-described it.

- **33' wire** (AXE1 drag wire) = the **radiator**, deployed as vertical / sloper / inverted-vee from a tree or mast.
- **13' wire** (KHATU1 counterpoise) = the **counterpoise**, laid on the ground.
- Both connect at the KH1 BNC via a binding-post adapter. Whip not used.

**Radiator modifications:**
- Button insulator at the **29' mark** (4' from the far end) — fold-back point.
- Mini-banana **socket at the 33' tip** — accepts a 2' wire with a matching plug, extending radiator to 35'.

**Three selectable radiator lengths (29' / 33' / 35'), and the fold-back / extension exist specifically to fix 20 m.**

- **33'** is fine on 40 m (λ/4), 30 m (mid-Z), 17 m (mid-Z), 15 m (3λ/4).
- **33' is bad on 20 m only** — it lands almost exactly on λ/2 (~34 ft with VF), feedpoint impedance climbs into the thousands of ohms reactive, KH1 ATU can't match.
- **29'** is a standard EFRW "magic length" — fixes 20 m by sliding off the λ/2 peak.
- **35'** is close to the standard 35.5' magic length — also fixes 20 m by sliding past λ/2.

Default deployment is 33'. The fold-back or 2' extension is a 20 m workaround
chosen by whichever is more convenient at the operating site. Standard EFRW
magic-length tables list 29 / 35.5 / 41 / 58 / 71 / 84 ft as recommended and
flag 32 ft (and adjacent values like 33) as **avoid** for exactly this 20 m λ/2
reason.

**Storage:** both wires figure-eighted onto a single Tufteln wire winder.

Source: https://wd8rif.com/kh1_micro_travel_kit.htm

### Pedestrian-mobile ground plane
- Operator's body capacitance is part of the ground plane. Holding the rig stabilizes SWR.
- Diminishing returns from multiple fanned counterpoises in pedestrian use; one well-aimed 13' or 33' drag wire is the consensus.

---

## 6. Cases

| Case | Source | Notes |
|---|---|---|
| ES20 (factory) | Elecraft | soft case; rumored to stress BNC if zipped wrong way — pack rig backwards |
| Modified Pelican M40 | **Tufteln** sells | M40 polymer is heat-stretched to fit factory whip; rugged + waterproof pocket kit |
| Pelican M50 | Pelican | swallows whole ecosystem incl. AXE1, 8.10 × 5.50 × 2.90" |
| Pelican 1050 / 1060 | Pelican (K4SWL verified) | 1050 deeper/narrower, 1060 standard |
| Nanuk Nano 320 / 330 | Nanuk | excellent latches, bulkier |

For weather: log tray cover handles light rain; for serious wet, use a clear waterproof map pouch or a bothy bag.

---

## 7. Operating Technique

- **Hold non-dominant hand**, paddle and pen with dominant hand, log into KHLOG1.
- Internal logging: ~50,000 character capacity (per official manual; the
  research report claims 32 KB EEPROM — **flag this discrepancy**).
- Workflow: enable LOGGING, send and receive, post-activation export via
  KH1 Utility Command Tester → "Send to PC" → run **ELECRAFT2FLE** by
  Christophe ON6ZQ to convert raw text to FLE / ADIF for POTA/SOTA upload.
- Memory keyer slot recipes: `CQ SOTA <CALL> K`. Open filter (FL3) when
  hunting; choke to FL1 (~300 Hz) in pileups.

### Battery duty cycle
- RX 50-70 mA, TX ~1.0 A → typical 1-2 hour POTA at 30% TX easily covered by internal 2.6 Ah.

---

## 8. Known Problems

1. **3D-printed cover warping** in extreme heat (Swiss Alps reports). Elecraft replaces under warranty.
2. **EFHW SWR/tune faults** — usually deployment error (no CMC, wrong CP length), not radio fault.
3. **Spongy paddle** — fix is the magnet mod above.
4. **Battery JST jack stress** — pull only on the plastic tab while bracing the PCB jack with thumb.
5. **Relay chatter** — set `QSK DELAY` to add a tiny hold time, prevents per-character relay drop.

---

## 9. Ecosystem

### SOTAmāt + SOTACAT (off-grid FT8 self-spotting)
- KH1 has no audio input → can't do conventional FT8.
- SOTACAT dongle plugs into KEY/DATA jack, sends `FOnn;` commands at 6.25 Hz steps while keyed down to synthesize FT8 FSK in firmware.
- Result: silent, internet-free SOTA self-spot.

### AX-line compatibility
- AX1, AX2, AX3, AXE1 (40 m extender) all mechanically + electrically compatible with KH1 BNC and threaded post.

---

## 10. Top 10 Community-Recommended Additions/Mods

1. **Magnetic paddle mod** — drill + 5×2 mm neodymium magnets in KHPD1.
2. **SOTACAT** dongle for FT8 self-spotting.
3. **Tufteln modified Pelican M40** for crushproof carry.
4. **28 AWG silicone counterpoise** swap.
5. **3D-printed power switch guard.**
6. **K6ARK / Tufteln random wires** (15-29 ft, no transformer) for stationary work.
7. **WD8RIF 33' wire fold-back** for 20 m use of AXE1 wire.
8. **N6ARA TinyPaddle + 3D-printed jack stabilizer** for ultra-stiff key feel.
9. **Dummy battery tray** + USB-C PD trigger for weight-critical SOTA.
10. **ELECRAFT2FLE** workflow (internal logger → ADIF).

---

## Open Questions / Sparse Data

- **VNA sweeps** isolating internal whip-loading-network insertion loss (per band) — anecdotal only.
- **Long-term (3+ year) durability** of 3D-printed enclosure threaded inserts — radio is too new.
- **USB-C PD RFI ingress** spectral measurements into the KH1's -130 dBm MDS RX — community reports are subjective; no published spectra.

---

## Discrepancies vs. Official Manual rev B7

| Topic | Research report says | Manual rev B7 says | Resolution |
|---|---|---|---|
| Logging memory | "32-kilobyte EEPROM logging memory" | "Up to 50,000 characters captured" | Manual is authoritative (50K chars). The 1 KB EEPROM in the manual is for **configuration**, separate from log storage. |
| Whip length | "4-foot whip" | "45 inches (114 cm)" — listed in specs | 45" is the documented length; "4 ft" is a colloquial round-up. |
| SWR safety | "tolerates up to 4:1" | "PA device very resilient ... drops to LO if reflected power excessive" | Manual doesn't quote a number. 4:1 is community lore from N6KR groups.io posts. |

---

## Source URLs (raw)

The Gemini result returned grounding redirect URLs rather than the original sources. Notable named sources to find directly:

- groups.io `Elecraft-KH1` archive
- elecraft.com KH1 documentation page
- wb3gck.com (WB3GCK blog — vertical experiments)
- wd8rif.com (WD8RIF blog — 33' wire mod)
- huyettm.net (WA9STI / M. Huyett blog)
- ke2yk.com
- tufteln.com (commercial accessories)
- printables.com / thingiverse.com (STLs)
- sotamat.com / SOTACAT (sotamat.com/sotacat/)
- kb6nu.com (FDIM/Pacificon coverage of N6KR's KH1 talks)
- K4SWL (Thomas Witherspoon — qrper.com / YouTube)
- ON6ZQ ELECRAFT2FLE software
