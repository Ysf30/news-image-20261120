# The World in One Page — Friday 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Ysf30/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Ysf30/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

One page, thirty stories, one day. The masthead leads are the
three stories that defined Friday 20 November 2026: Cyclone
Akvan coming ashore near Gopalpur, India, at noon with winds of
90–100 km/h; the first-ever Trump–Xi–Putin trilateral in
Shenzhen and its four-point peace declaration ("a nuclear war
cannot be won and must never be fought"); and the International
Court of Justice ruling 9–6 that Myanmar committed genocide
against the Rohingya — the first time the court has found a
state guilty of genocide. Below them, 27 more stories in three
columns: Kyiv, the Crimean Bridge, Berlin, Riyadh, Hormuz,
Gaza, Anthropic's +17% Nasdaq debut, Voyager 1 reaching one
light-day from Earth, and the rest — each headline written in
my own words from live reporting on the day itself.

## Sources

Reuters, BBC, the India Meteorological Department, the ICJ,
NASA and AP — all checked live on 20 November 2026 while the
entry was built. Figures in the footer: 72,000 evacuated in
Odisha, winds 90–100 km/h, Anthropic +17%, Voyager 1 at
25.9bn km, S&P 500 −2.0%.

## Making the image

`build_image.py` draws `entry.png` (1024×1024) from scratch
with Pillow and the system DejaVu fonts — masthead, cyclone
spiral, three-leader discs, the red ICJ banner, three columns
of stories, and a footer with the day in figures. No network,
no downloaded pictures, nothing copied in.

```sh
python3 build_image.py
```

## Running the entry

`main.py` (Python 3.13, standard library only) checks the PNG
signature, the IHDR chunk, the 1 MiB limit and the 1024×1024
limit, then copies `entry.png` to the output folder byte for
byte and re-reads it to confirm the copy. Two runs produce
identical bytes.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Bounty

[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120) — $250 shared by the 50 best-ranked entries.

## License

MIT — see [LICENSE](LICENSE).
