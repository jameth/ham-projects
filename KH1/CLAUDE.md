# Elecraft KH1

Research, notes, mods, and accessory projects for the Elecraft KH1
portable HF CW transceiver, with emphasis on the Edgewood package
(handheld pedestrian-mobile configuration).

See parent `../CLAUDE.md` for general ham workspace conventions
(SI units, project structure, Python sim setup). This file scopes
KH1-specific context.

## Radio Overview

- Portable QRP CW transceiver, ~5 W out (lower on internal battery)
- Bands: 40, 30, 20, 17, 15 m (CW); general-coverage RX
- Internal ATU (KHATU1)
- Internal Li-ion battery
- Built-in iambic paddle (KHIP1) and optional log tray on Edgewood
- Whip antenna with loading coil taps per band (AX1-style)

## Edgewood Package Components

Track inventory and configuration here as items are acquired or
modified:

- KH1 transceiver
- KHIP1 internal paddle
- KHLOG1 log tray
- KHATU1 internal ATU
- Whip antenna with band-tap loading coil
- Counterpoise wire(s)
- Earphones / earbuds
- Carry case

## Focus Areas

- **Operating notes** — band/time strategy, POTA/SOTA usage, pedestrian-mobile technique
- **Antenna pairings** — whip + counterpoise tuning, end-fed alternatives, deployment options
- **Mods & addons** — field-serviceable enhancements, 3D-printed accessories, external battery options
- **Firmware/config** — menu settings, memory keyer messages, CONFIG snapshots
- **Measurements** — RX sensitivity, TX output per band/battery state, ATU match range

## Project Structure

Within this folder, follow the parent workspace pattern:

```
KH1/
  <project-or-topic>/
    README.md          # goals, theory, build notes
    bom.md             # parts list (if applicable)
    schematics/        # any circuit work
    measurements/      # VNA sweeps, power readings, photos
    notes.md           # freeform research / observations
```

For pure research topics (no build), a single `README.md` or
`notes.md` is fine.

## Conventions

- Log frequencies in MHz with band context (e.g., "14.061 MHz / 20 m")
- Document battery state when recording TX power measurements
  (internal Li-ion sag affects output significantly)
- Note antenna + counterpoise length when reporting SWR or match
- Keep firmware version recorded in any config/menu notes
  (settings change between releases)
- Photos welcome; place in the relevant project's `measurements/`
  or a topic-local `photos/` folder

## Useful References

- Elecraft KH1 Owner's Manual
- Elecraft KH1 Reference Guide (menu/config)
- KH1 user community: groups.io `Elecraft-KH1`
- POTA: pota.app
- SOTA: sotawatch.sota.org.uk
