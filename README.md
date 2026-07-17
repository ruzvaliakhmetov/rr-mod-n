# RR mod N

An experimental font that calculates modulo using OpenType substitutions.

The current version calculates **modulo 7**. Type an integer and enable Stylistic Set 1 (`ss01`) to replace it with the remainder:

- `15` → `1`
- `123` → `4`
- `999999999` → `5`

Numbers of up to nine digits are supported.

## How it works

The font processes digits from left to right and stores the current remainder in one of seven zero-width state glyphs. Each following digit updates the state according to:

    new state = (current state × 10 + digit) mod 7

The final state is then replaced with a visible digit. The entire calculation is performed by the OpenType shaping engine.

## Files

- `RR_mod7.glyphs` — font source
- `mod7generator.py` — Glyphs script that generates the OpenType feature code