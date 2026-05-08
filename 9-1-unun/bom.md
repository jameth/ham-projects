# Bill of Materials

## Common Parts (All Designs)

| Item                          | Qty | Notes                                    |
|-------------------------------|-----|------------------------------------------|
| SO-239 female chassis mount   | 1   | Coax side (50 Ω)                        |
| Binding post or lug bolt      | 1   | Antenna wire terminal (450 Ω side)       |
| Binding post or lug bolt      | 1   | Counterpoise / ground terminal           |
| Project box                   | 1   | Weatherproof if outdoor mounting         |
| Mounting hardware              | --  | Screws, nuts, lock washers for terminals |
| Hot glue / RTV silicone       | --  | To secure toroid in enclosure            |
| Ring terminals or solder lugs | 2-3 | For wire-to-terminal connections         |

---

## Design A: Trifilar on FT-240-43, 12 Turns (Recommended)

| Item                        | Qty            | Notes                                    |
|-----------------------------|----------------|------------------------------------------|
| FT-240-43                   | 1              | Amidon / Fair-Rite mix 43 toroid         |
| 18 AWG epoxy magnet wire    | ~250 cm (100") | 3 pieces × ~85 cm (33") each + leads    |

*Per-turn path on FT-240 ≈ 55 mm. 12 turns × 55 mm ≈ 660 mm per wire +
8–10 cm for tails and interconnections ≈ 80–85 cm per wire. Buy 300 cm
(10 ft) for comfortable handling while winding.*

---

## Design B: Trifilar on FT-240-31, 10 Turns

| Item                        | Qty            | Notes                                   |
|-----------------------------|----------------|-----------------------------------------|
| FT-240-31                   | 1              | Amidon / Fair-Rite mix 31 toroid        |
| 18 AWG epoxy magnet wire    | ~210 cm (83")  | 3 pieces × ~70 cm (28") each + leads   |

*10 turns × 55 mm ≈ 550 mm per wire + leads ≈ 70 cm. Buy 225–240 cm for
working margin.*

---

## Design C: Trifilar on Stacked 2x FT-240-43, 10 Turns

| Item                        | Qty            | Notes                                   |
|-----------------------------|----------------|-----------------------------------------|
| FT-240-43                   | 2              | Stacked and taped together              |
| 18 AWG epoxy magnet wire    | ~285 cm (112") | 3 pieces × ~95 cm (37") each + leads   |
| Electrical tape / Kapton    | --             | To bind stacked cores                   |
| Project box (larger)        | 1              | Must accommodate 25.4 mm core stack     |

*Stacked height doubles per-turn path to ~80 mm. 10 turns × 80 mm =
800 mm per wire + leads ≈ 95 cm. Buy 300–325 cm for working margin.*

---

## Additional: Counterpoise Wire

| Item                        | Qty           | Notes                              |
|-----------------------------|---------------|------------------------------------|
| Insulated stranded wire     | 5-10 m        | For single counterpoise radial     |
|                             | OR 4x 4-10 m  | For multiple radials               |
| Ring terminal               | 1 per radial  | To connect to GND lug on enclosure |

## Additional: Test Load

| Item                        | Qty | Notes                                   |
|-----------------------------|-----|-----------------------------------------|
| 390 Ω resistor (2W)        | 1   | Non-inductive, for testing              |
| 56 Ω resistor (2W)         | 1   | Series with 390 Ω = 446 Ω ≈ 450 Ω     |
| SO-239 to PL-259 adapter   | 1   | Or short coax jumper for NanoVNA hookup |
