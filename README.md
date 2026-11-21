# The Passport Page of a Country That Isn't There

[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Vellocatta/the-passport-page-of-a-countr-2-20261121-0318-entry/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Vellocatta/the-passport-page-of-a-countr-2-20261121-0318-entry/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

Entry for the [make.fun bounty](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318): an invented passport spread for a country that does not exist.

`main.py` (Python 3.13, stdlib + PIL) writes one 1024×1024 PNG to `/output/entry.png`. Deterministic: fixed data, no network, no clock, no randomness.

## The country: Kestrelia

An alpine republic, capital Aldor. Holder Mara Vren, born Aldor, passport K7319042, issued 12 MAR 2023, expires 11 MAR 2033. Travel history: Aldovia entry 02 APR 2024, Brenmark exit 19 APR 2024, Tarnovia entry 07 OCT 2025 (matching transit visa), Aldovia exit 23 OCT 2025. The telling detail: a mountain transit permit, valid for the Three Valleys only.

The spread has a data page (portrait, personal data, signature, ICAO MRZ with correct check digits) and a visa page (transit visa, four border-control stamps from neighbouring countries, endorsement box). Five candidate countries were generated and judged in a local pairwise tournament (record in the work dir); Kestrelia won because its stamps are all from neighbours with dates that agree — the other candidates stamped their own capitals or reused the holder's surname as a place name.
