# Elecraft KH1 Operating Cheat Sheet

Field reference for the KH1 (Edgewood configuration), distilled from the
Owner's Manual rev B7 (firmware ≥ 1.27). Format is scan-first: tables and
short lines, no prose.

Conventions in this doc:
- `[N]` = tap switch N (1-4)
- `[N]+` = hold switch N (>0.5 s)
- `VFO` / `AF/MON` = right and left knob, tap or hold
- `MENU:NAME` = menu entry (3-letter shorthand in braces, e.g. {DSP})

---

## Front Panel At-a-Glance

| Control | Tap | Hold |
|---|---|---|
| **VFO knob** | toggle 10 / 100 Hz step | 1 kHz step (until tapped again) |
| **AF/MON knob** | switch to MON (sidetone vol/pitch) | SPOT (zero-beat tone) |
| **[1] SPD-** | keyer WPM down | RCVR display group |
| **[2] SPD+** | keyer WPM up | PFn / XMTR display group |
| **[3] ATU** | run ATU tune cycle | BAND / MODE display group |
| **[4] MSG** | message play menu | MENU |
| **WHIP slide switch** | 17-15 m / OFF / 20 m | (set OFF when using BNC) |
| **ON/OFF slide** | power | — |

In any of the four "display groups," line 1 = tap targets, line 2 = hold targets.
Tap [4] to exit a group; many groups auto-exit after ~10 s.

## Display (Operate mode, line 2)

```
14062.50 C +.42R     <- VFO  mode  RIT/XIT
S5  ♪ n3 🔋  15:30   <- S-meter  AF/sidetone  filter#  batt  time
```

S-meter: 6 dB/unit S0-S9; `+` = S9+10, `†` = S9+20, `‡` = S9+30.
Tuning indicator after mode letter: `^` = signal, `_` = none.
`R` after offset = RIT on; `X` = XIT on; `L` (flashing) = logging on.

Switch to V/I/Temp line via `MENU:DISP MODE` or a PFn assignment.

---

## Quick Operating Recipes

### Power on, get on the air
1. Slide ON.
2. Hold `BAND/MODE` → tap `[1]/[2]` to pick band, exit with `[4]`.
3. Connect antenna + counterpoise. If using whip, slide WHIP switch to band.
4. Tap `[3] ATU` to tune. Watch SWR bar. Re-tune if > 3:1.
5. Spin VFO to frequency. Send.

### Switch antennas (whip ↔ BNC wire)
1. Slide whip switch to **OFF / center** (removes RF from whip post).
2. Plug BNC antenna. Tap `ATU`.
3. To revert, unplug BNC, slide whip switch back to band, tap `ATU`.

ATU keeps separate L/C settings per band, recalled on band change.

### Filter and attenuator
- Hold `[1] RCVR` → tap `[1/2/3]` for FL1 / FL2 / FL3 (~0.3 / 0.5 / 2 kHz).
- Same group, hold `[1/2/3]` for atten 0 / -10 / -30 dB.
- Hold `[4]` in this group to toggle RIT.

### Send a memory message
- Tap `[4] MSG` → tap `[1/2/3]` plays M1/M2/M3; hold same plays with auto-repeat.
- Hold `[4] GRP` toggles to M4-M6.
- Repeat interval set by `MENU:MSG RPT` (default 5 s).

### Record a memory message
- Tap `[4] MSG` → hold `[4] REC` → tap `[1/2/3]` for slot.
- Send with paddle (≤ 40 chars), end with any switch.
- Hold `[1/2/3]` in REC group to clear that slot.

### Use SPOT to zero-beat
- Hold `AF/MON` knob → SPOT tone plays.
- Tune VFO until incoming signal pitch matches SPOT pitch.
- Tap any control to exit.

### RIT (receive-only fine tune)
- Hold `[1] RCVR` → hold `[4]` to enable RIT.
- VFO knob now offsets RX only (TX stays put). `R` shows on display.
- To clear offset: assign `RIT CLEAR` to a PFn (only way), then tap that PFn.

### XIT (TX-only offset for split callers)
- Hold `[2] PFn/XMTR` → hold `[4]` to enable XIT.
- Useful when DX says "UP 2."

### Manual ATU peak (RX, no TX)
- `MENU:ATU PARAM` → unlock → tap `[2]` set L, `[3]` set C, `[4]` set Z.
- VFO adjusts the value. Useful on SWL band where TX is blocked.

### SWL listening (6.7-22 MHz)
- Hold `BAND/MODE` → tap up past 15 m to SWL band.
- VFO step is 100 kHz (tap) / 1 MHz (hold) on SWL band.
- Mode = LSB or USB (copies AM). Pick the cleaner sideband.
- Optional: peak signal with `MENU:ATU PARAM` (TX disabled here anyway).

### Scan / mini-pan (hands-free signal hunt)
- Set `MENU:PAN SPAN` (default 10 kHz; smaller = faster + finer).
- Set `MENU:PAN THR` (see "Calibration" below).
- Set `MENU:PAN MODE = ON` and exit. VFO is captured.
- Tap any switch to stop and tune.
- Recommend assigning `PAN MODE` to a PFn for instant on/off.

### Lock the VFO (rough terrain, pedestrian)
- Hold `BAND/MODE` → hold `[4]` to lock (locks VFO and XIT, not RIT).
- Hold `[4]` again to unlock.

### Manual TX TUNE (carrier into ATU/dummy)
- Hold `[2] PFn/XMTR` → hold `[1]` (TUN). Sends carrier.
- Hold `[1]` again to stop.

### TX TEST (CW practice, no RF out)
- Hold `[2] PFn/XMTR` → hold `[3]` (TST). Key plays sidetone, no PA drive.

### Power level toggle (LO ~2 W / HI ~5 W)
- Hold `[2] PFn/XMTR` → hold `[2]` (PWR). Toggles LO/HI.

### Battery / current / temp check
- `MENU:VBAT` → shows internal battery V and accumulated Ah.
- Hold `[0]` in VBAT to reset Ah after a fresh battery swap.
- For live V/I/Temp on line 2, set `MENU:DISP MODE = V/I/Temp` or use a PFn.

### Built-in logging
- Set `MENU:LOGGING = ON`. `L` flashes by mode letter.
- TX'd CW logged uppercase with timestamp + band + mode.
- Tap `[4] MSG` then send free-text via paddle to log lowercase notes
  (other station's call, QTH, etc.) without keying RF — uses TX TEST internally.
- `MENU:LOGGING = VIEW` to scroll log on display via VFO knob.
- `MENU:LOGGING = ERASE` to wipe.
- Capacity ~50 K characters. Set `ADJ TIME` and `ADJ DATE` first.

---

## Keyer Quick Tips

| Setting | Where | Recommended |
|---|---|---|
| Speed (8-50 WPM) | tap `[1]/[2]` SPD-/+ | start 16-20 WPM for QRP/PM |
| Iambic mode | `MENU:KEY IAMB` | A (default) unless trained on B |
| Paddle orientation | `MENU:KEY JACK` | Pdl Norm (right-handed) or Pdl Rev (left-handed) |
| Keying weight | `MENU:KEY WGHT` | 1.25 default; 1.10-1.15 for lighter feel |
| QSK delay | `MENU:QSK DELAY` | 0.00 s for full break-in; 0.10-0.20 s on noisy bands |
| Sidetone pitch | tap AF/MON, then VFO | match your most-comfortable RX pitch (600 Hz default) |
| Sidetone volume | tap AF/MON, then AF | low enough not to fatigue with earbuds |

If you change sidetone pitch, re-run `MENU:ADJ BFO` for FL1 + FL2 so the
filter passband stays centered on incoming signals at the new pitch.

---

## Recommended PFn Assignments

Three programmable shortcuts. Assigned via `MENU:PF1 FUNC` / `PF2 FUNC` / `PF3 FUNC`.
After assignment, access by holding `[2] PFn/XMTR`, then tapping `[1/2/3]`.

### Default recommendation (general field use)

| Slot | Menu entry | Why |
|---|---|---|
| **PF1** | `DSP MODE` ({DSP}) | one tap toggles line 2 between Operate (S-meter, time) and V/I/Temp (battery, draw, PA temp). The single most-used shortcut. |
| **PF2** | `ATU MODE` ({ATM}) | flip Auto ↔ Bypass instantly when swapping antennas, or to skip retune when SWR is already known good. |
| **PF3** | `RIT CLEAR` ({CLR}) | only usable via PFn. Zero out RIT/XIT after a pile-up without rebooting menus. |

### Variant — heavy logger (POTA/SOTA)

| Slot | Menu entry | Why |
|---|---|---|
| PF1 | `DSP MODE` | as above |
| PF2 | `LOGGING` | toggles ON ↔ VIEW for in-the-field log review |
| PF3 | `RIT CLEAR` | as above |

### Variant — band hunter

| Slot | Menu entry | Why |
|---|---|---|
| PF1 | `DSP MODE` | as above |
| PF2 | `PAN MODE` | one-touch scan/mini-pan |
| PF3 | `TEXT DEC` | quick decode toggle when chasing weak CW |

### Variant — paddle / WPM tweaker

| Slot | Menu entry | Why |
|---|---|---|
| PF1 | `KEY WGHT` | adjust dot/space ratio on the fly |
| PF2 | `QSK DELAY` | bump up delay on noisy bands |
| PF3 | `RIT CLEAR` | as above |

To clear an assignment: open `PFn FUNC` and scroll the value to `PFn Unset`.

---

## Recommended Menu Settings

Defaults are sensible. Below are the ones worth changing on day one.

| Menu | Default | Suggested | Reason |
|---|---|---|---|
| `ADJ TIME` | — | UTC, current | logging needs accurate clock |
| `ADJ DATE` | — | current | logging |
| `ADJ RTC` | +00 s/day | adjust after 1-3 days drift check | better long-term clock accuracy |
| `DISP MODE` | Operate | Operate (toggle via PF1) | leave default; toggle as needed |
| `KEY JACK` | Pdl Norm | Pdl Norm or Pdl Rev | match dominant hand. Set RS232 only for firmware updates / CAT |
| `KEY IAMB` | Mode A | Mode A | Mode B only if trained on it |
| `KEY WGHT` | 1.25 | 1.10-1.20 | many ops prefer slightly lighter dots |
| `QSK DELAY` | 0.00 | 0.00 | full break-in unless noisy |
| `MSG RPT` | 5 sec | 5-7 sec for CQing | shorter for contests |
| `LOGGING` | OFF | ON for activations | leave OFF otherwise to keep EEPROM clean |
| `TEXT DEC` | OFF | TX ONLY (if logging) or OFF | TX-only is required when LOGGING=ON to capture sent text |
| `PAN MODE` | OFF | OFF | enable on demand via PFn |
| `PAN SPAN` | 10 kHz | 5 kHz for SOTA hunts | tighter span = faster scan |
| `PAN THR` | -00 | calibrate (see below) | sets decode + scan sensitivity |
| `ATU MODE` | Auto (if installed) | Auto | Bypass only for resonant antennas |
| `VFO FAST` | 100 Hz | 100 Hz | 200 Hz is faster but coarser |
| `SW TONES` | OFF | OFF (sighted) / 15 WPM (eyes-free / blind ops) | enables audio CW menu feedback |
| `PF1 FUNC` | unset | `DSP MODE` | see above |
| `PF2 FUNC` | unset | `ATU MODE` | see above |
| `PF3 FUNC` | unset | `RIT CLEAR` | see above |

### Calibrating PAN THR (do once)
1. Disconnect antenna.
2. Open `MENU:PAN THR`, increase value until display reads `AFCMP` 1 (was 0).
3. That's the lowest threshold; any higher trades sensitivity for QRM rejection.

### Per-band BPF peak (optional, improves RX)
- `MENU:ADJ BPF` stores one DAC value per 100 kHz segment from 6.7-22 MHz.
- Factory-aligned at: 7.05, 7.15, 7.25, 10.0, 14.0, 18.0, 21.0 MHz, plus the
  duplicates noted in the manual.
- For SWL band, peak each 100 kHz segment you actually use (those values
  ship as approximate defaults).

---

## ATU Notes

- Tap `[3] ATU` runs full L/C search until 1:1 or all combinations tried.
  No second-tap "try harder" feature exists.
- SWR bar: 1 solid block ≈ 1:1, 2 blocks ≈ 2:1; half-block = ~0.5 SWR unit.
- KH1 ATU has fewer L/C steps than KX2/KX3, so SWR may settle at < 3:1
  rather than 1:1. PA tolerates higher SWR but auto-drops to LO power if
  reflected power is excessive.
- Whip + 13 ft counterpoise (supplied) → designed for 20/17/15 m.
  Works on 30 m at higher SWR / lower power. Not for 40 m on the whip.
- For 40 m, plan on a BNC-fed wire (random wire + 9:1 unun, EFHW, or
  resonant dipole).
- ATU L/C settings are saved per band and recalled on band change.
- `MENU:ATU MODE = Bypass` for resonant antennas (saves wear on the relays).

---

## Power and Battery

| Spec | Value |
|---|---|
| External supply | 8-15 V, center pin +, 2.1 mm × 5.5 mm barrel |
| Internal battery | KXBT2, 11 V Li-ion, 2.6 Ah |
| Higher-V source wins | internal and external jacks are diode-OR'd |
| RX current (no signal) | 40-80 mA |
| TX current (5 W) | 0.5-1.0 A |
| Internal speaker peak | 0.5 W |
| Charge in progress | RED LED (off) / ORANGE (on) / GREEN when done |

Tips
- ~5 W needs ≥ 11 V supply. KXBT2 sits at 11 V most of its discharge curve.
- After charging a fresh KXBT2 to >12 V, let it drop to ~11 V before
  recalibrating `ADJ PWR`.
- Reset Ah meter (`VBAT` → hold `[0]`) after every battery swap.

---

## Common Error / Status Display Items

| Display | Meaning |
|---|---|
| `UTILITY?` on power-up | failed firmware self-test → forced firmware load |
| `LOADING` | firmware update in progress |
| `MENU` icon (key symbol) | menu entry locked, hold `[4]` to unlock |
| `r` after mode letter | message repeat pause |
| `^` / `_` after mode letter | text decode signal-present / no-signal indicator |
| `L` flashing | logging on |
| `SWL` in offset field | RIT/XIT disabled on SWL band |

---

## Audio CW User Interface (eyes-free)

For low-light or vision-impaired use:
- `MENU:SW TONES` set to a code speed (10-30 WPM) enables it.
- Or hold `MENU` at power-on twice to toggle on (sends "15 WPM").
- Switch presses, band change, coarse VFO steps, and many menu values
  are sent in CW. Sub-functions return to normal display; functional
  groups stay up and emit a periodic low-high tone (tap `[4]` to exit).
- Hold `BAND/MODE` to hear current kHz and 100s of Hz digits.
- Menu entries with audio CW feedback: ADJ BPF, ATU MODE, EE INIT,
  FIRMWARE, KEY IAMB, KEY JACK, KEY WGHT, LOGGING, MSG RPT,
  QSK DELAY, SERIAL NR, SW TONES, VFO FAST.

---

## Field Operating Habits (KH1 specific)

- **Always deploy the counterpoise.** Without one the ATU will still match,
  but radiated signal can be 20-30 dB weaker.
- **Drape the counterpoise toward the favored direction.** Several dB of
  apparent gain is common.
- **Slope behind you = reflector.** Pick spots with rising terrain on the
  back side when possible.
- **Slow down to 16-20 WPM** when running QRP and pedestrian-mobile.
  Receivers will copy you better and you'll make fewer mistakes.
- **Watering holes:** 7030 / 10116 / 14060 / 18086 / 21060 (CW QRP),
  18157.5 (HF Pack), 14055 (County Hunters Net).
- **Lock the VFO** before stuffing the rig in a pocket.
- **Cover the front panel with the log tray** in light precipitation.

---

## Field Reset Procedures

- **Operational EE INIT** (`MENU:EE INIT = OPERATIONAL`, then power-cycle):
  resets menu settings to defaults, preserves factory calibration.
  Try this first if behavior is weird.
- **Full EE INIT** (`= FULL`): wipes calibration. Last resort. Save
  config to PC via KH1 Utility first.
- **Forced firmware reload**: hold `[2]` while powering on → `UTILITY?`
  → run KH1 Utility.
