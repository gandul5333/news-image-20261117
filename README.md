# news-image-20261117 — The World in One Day

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/gandul5333/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/gandul5333/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image that sums up Tuesday 17 November 2026's world news, drawn as a
newspaper front page — masthead dated **TUESDAY 17 NOVEMBER 2026** — so a
viewer who missed the day can tell what happened from the image alone.

The five stories, each with its own illustration, headline and one-line
summary:

1. **War in Europe** — Ukraine strike collapses a span of the Kerch Bridge
   to Crimea, the second attack in 24 hours, as Russian missiles hit
   bridges over the Dnipro in Kyiv.
2. **Middle East** — tankers hit by mines near the Strait of Hormuz catch
   fire; a third US carrier arrives in the region.
3. **Diplomacy** — Trump, Xi and Putin confirmed to meet in Shenzhen on
   Thursday, on the sidelines of the APEC summit.
4. **Space** — ULA's Vulcan rocket fails minutes after launch, destroying
   40 Amazon Leo satellites.
5. **Business** — a JPMorgan Chase software bug disrupts online banking
   and Zelle payments. (Footer: five European states plan a Rwanda return
   hub for rejected asylum seekers.)

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to the
output directory as `entry.png` and verifies the copy's sha256 matches the
source. The image is a 1024x1024 PNG (80,648 bytes) drawn by
`draw_image.py` in this repository (Pillow, deterministic — no randomness,
fixed geometry and fonts), so both graded runs write byte-identical bytes.

## Files

- `entry.png` — the image (PNG, 1024x1024, 80,648 bytes)
- `main.py` — the entrypoint
- `draw_image.py` — the script that drew `entry.png`
- `LICENSE` — MIT
- `.makefun/owner.json` — claim file naming the payout wallet
