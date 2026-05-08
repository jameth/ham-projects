# Ham Radio Projects

Open-build workspace for amateur radio antenna and RF circuit
projects, with a focus on QRP portable HF operation and end-fed
antenna systems.

## Projects

| Project | Description | Status |
|---|---|---|
| [`KH1/`](KH1/) | Elecraft KH1 portable QRP CW transceiver — operating notes, four-option antenna go-kit (whip + radials, short EFRW, multi-band magic-length EFRW, custom EFHW), custom 49:1 + 1:1 CMC matching unit, simulation, build sheets. | Active build |
| [`49-1-unun/`](49-1-unun/) | 49:1 unun for end-fed half-wave antennas. Tapped autotransformer on FT-240-43, with compensation capacitor. Leakage inductance model included. Four design variants. | Designed, ready to build |
| [`9-1-unun/`](9-1-unun/) | 9:1 unun for end-fed random wire antennas. Trifilar autotransformer on FT-240-43/31. Three design variants. Performance simulation included. | Designed, ready to build |
| [`common-mode-choke/`](common-mode-choke/) | Common-mode choke for HF antenna feedlines. Four designs using FT-240-31/43 cores with RG316 coax or bifilar magnet wire. Python impedance calculator. | Designed, ready to build |

## Focus Areas

- **Antennas** — design, simulation, and construction of HF antennas (verticals, end-fed, dipoles, loops)
- **Baluns and ununs** — impedance transformation, balanced/unbalanced transitions
- **Common-mode chokes** — suppressing CM currents on feedlines
- **Matching networks** — RF circuits paired with portable QRP rigs
- **Simulation** — Fair-Rite ferrite material modeling, transformer/choke performance, complex permeability with log-log interpolation

## Workspace Conventions

- SI units throughout; impedances in Ω, frequencies in MHz / kHz / Hz
- Design parameters (target frequency, bandwidth, impedance, SWR) at the top of each project README
- Schematics stored alongside simulation files
- BOM files in every build project
- Test results and measurements documented when available
- Python simulation scripts use `MPLBACKEND=Agg` for non-interactive plot generation
- Simulation scripts output both console tables (per ham band) and PNG plots

## Project Structure (per project)

```
<project-name>/
  README.md          # design goals, theory, build notes
  bom.md             # bill of materials
  schematics/        # circuit diagrams, KiCad files
  simulations/       # Python scripts, antenna models
  measurements/      # NanoVNA sweeps, photos
```

## Design Patterns

### Ferrite core selection
- **Mix 31** for common-mode chokes — lossy/resistive impedance absorbs CM energy as heat
- **Mix 43** for transformers (ununs / baluns) — lower loss preserves signal power
- **Stacked cores** double impedance / inductance while preserving broadband behavior better than adding turns (less parasitic capacitance)

### Simulation approach
- Fair-Rite complex permeability data (μ' and μ'') with log-log interpolation
- FT-240 reference: OD = 61 mm, ID = 35.55 mm, H = 12.7 mm, core constant μ₀·Ae/le = 1.339e-9 H
- Transformer models include leakage inductance (coupling k ≈ 0.95)
- Plots span 1-50 MHz with ham band markers

## Tools

- **KiCad** for schematic capture and PCB layout
- **LTspice / QUCS** for circuit simulation
- **NEC2 / MMANA-GAL** for antenna modeling
- **NanoVNA** for VNA measurements
- **Python (numpy, scipy, matplotlib)** for calculations and plotting

## Notes Files

- [`notes.md`](notes.md) — consolidated build-calculation reference
  (per-turn length formulas, wire/coax BOM math, ferrite core selection,
  trifilar bundling theory, magic-length EFRW SWR tables, mobile HF
  operating topics)
- [`KH1/community-research-2026-05.md`](KH1/community-research-2026-05.md) — Gemini Deep Research synthesis on KH1 mods, accessories, antennas, and counterpoise science
- [`KH1/operating-cheat-sheet.md`](KH1/operating-cheat-sheet.md) — KH1 field operating reference (menus, PFn, ATU, logging)
- [`FTX1/FTX-1_Optima_Research_Guide.md`](FTX1/FTX-1_Optima_Research_Guide.md) — Gemini Deep Research synthesis on the Yaesu FTX-1 Optima HF transceiver

## References

- ARRL Antenna Book
- ON4UN's Low-Band DXing
- Sevick's Transmission Line Transformers
- Fair-Rite catalog
- ITU frequency allocation tables
- WD8RIF KH1 Micro Travel Kit: https://wd8rif.com/kh1_micro_travel_kit.htm
- K6ARK Portable Radio: https://k6ark.com/

## A Note on Manuals

The KH1 Owner's Manual and Programmer's Reference are not included in
this repo because they are Elecraft copyrighted material. Download
them directly from Elecraft if you need them:
https://www.elecraft.com/

## License

Documentation, schematics, and simulation results in this repo are
licensed under [Creative Commons Attribution-ShareAlike 4.0
International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

Python simulation scripts are licensed under the MIT License unless
noted otherwise. See `LICENSE` files in subfolders if present.
