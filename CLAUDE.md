# HAM Radio Projects

Workspace for amateur radio projects and research, with a strong focus on
building RF components for end-fed HF antenna systems.

## Focus Areas

- **Antennas** — design, simulation, and construction of HF/VHF/UHF antennas (dipoles, verticals, Yagis, loops, end-fed, etc.)
- **Baluns & Ununs** — impedance transformation and balanced/unbalanced line transitions
- **Common Mode Chokes** — suppressing common mode currents on feedlines
- **RF Circuits** — filters, amplifiers, matching networks, and other radio-related electronics
- **Simulation & Modeling** — antenna modeling (NEC, MMANA, EZNEC), circuit simulation (LTspice, QUCS, etc.)

## Current Projects

| Project | Description | Status |
|---------|-------------|--------|
| `common-mode-choke/` | CM choke for end-fed HF antenna feedline. 4 designs using FT-240-31/43 cores with RG316 coax or bifilar magnet wire. Includes Python impedance calculator. | Designed, ready to build |
| `9-1-unun/` | 9:1 unun for end-fed random wire antenna. Trifilar autotransformer on FT-240-43/31. 3 design variants. Includes performance simulation. | Designed, ready to build |
| `49-1-unun/` | 49:1 unun (EFHW transformer) for end-fed half-wave antenna. Tapped autotransformer with compensation capacitor. 4 design variants. Includes leakage inductance model. | Designed, ready to build |

## Cross-Project Notes

- `notes.md` — consolidated reference for build calculations
  (per-turn length formulas, wire/coax BOM math), ferrite core
  selection (mix 31 vs 43, FT-140 vs FT-240, stacking), trifilar
  bundling theory, CM choke 12T-vs-9T tradeoff, integrated unun+choke
  enclosure design, random wire magic lengths with SWR tables for
  internal-tuner compatibility, and mobile HF operating topics
  (battery isolation, chargers, grounding).

## Available Materials

- RG316 coax cable
- Epoxy-coated magnet wire
- FT-240-31 toroids (mix 31, μi ≈ 1500, best for chokes / lossy applications)
- FT-240-43 toroids (mix 43, μi ≈ 800, best for transformers / low-loss applications)
- Female SO-239 chassis mount connectors
- Project boxes

## Conventions

- Use SI units throughout; document impedances in ohms, frequencies in MHz/kHz/Hz
- Include design parameters (target frequency, bandwidth, impedance, SWR) at the top of each project
- Schematics should be stored alongside any simulation files
- Keep bill-of-materials (BOM) files with each build project
- Document test results and measurements when available
- Python simulation scripts use `MPLBACKEND=Agg` for non-interactive plot generation
- Simulation scripts output both console tables (per ham band) and PNG plots

## Project Structure

```
ham/
  <project-name>/
    README.md          # design goals, theory, build notes
    bom.md             # bill of materials
    schematics/        # circuit diagrams, KiCad files
    simulations/       # antenna models, SPICE files, Python scripts
    measurements/      # VNA sweeps, SWR plots, photos
```

## Design Patterns Established

### Ferrite Core Selection
- **Mix 31** for common-mode chokes — lossy/resistive impedance absorbs CM energy
- **Mix 43** for transformers (ununs/baluns) — lower loss preserves signal power
- **Stacking cores** doubles impedance/inductance while preserving broadband behavior better than adding turns (less parasitic capacitance)

### Simulation Approach
- Fair-Rite complex permeability data (μ' and μ'') with log-log interpolation
- FT-240 core geometry: OD=61mm, ID=35.55mm, H=12.7mm
- Core constant: μ₀·Ae/le = 1.3391e-09 H
- For transformers: include leakage inductance model (coupling k ≈ 0.95) — critical for realistic high-frequency behavior
- Plot impedance/loss/SWR across 1-50 MHz with ham band markers

## Tools & Software

Common tools that may be referenced:

- **KiCad** — schematic capture and PCB layout
- **LTspice / QUCS** — circuit simulation
- **NEC2 / MMANA-GAL / EZNEC** — antenna modeling
- **NanoVNA** — vector network analyzer for measurements
- **Python** (numpy, scipy, matplotlib) — calculations, data analysis, plotting

## Useful References

- ARRL Antenna Book
- ON4UN's Low-Band DXing
- Sevick's Transmission Line Transformers
- Fair-Rite catalog (complex permeability curves for mix 31, 43, 61, etc.)
- ITU frequency allocation tables
