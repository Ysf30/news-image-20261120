# The World Today — Friday 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Ysf30/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Ysf30/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A single front page that sums up Friday 20 November 2026. The
leads are Cyclone Akvan coming ashore on India's east coast, the
first-ever Trump–Xi–Putin trilateral in Shenzhen and its joint
Peace Declaration, and the International Court of Justice ruling
that Myanmar committed genocide against the Rohingya. Around
them: Ukraine and Europe's Berlin talks, the Gaza ground push a
year into the ceasefire, Anthropic's record $107bn IPO debut,
Voyager 1 reaching one light-day away, and New Zealand's 317–6
against India — 31 stories in all, each headlined in my own
words from live reporting on the day itself.

## How the image is made

`build_image.py` draws the page from scratch with Pillow
(DejaVu fonts, no network, no downloaded pictures): masthead,
a hand-drawn Bay of Bengal cyclone chart, the three-leader
panel, the ICJ strip, a day-in-figures strip, four columns of
short stories, a ticker and a sources footer. Running it
re-renders `entry.png` at 1024×1024.

```sh
python3 build_image.py
```

## How the entry runs

`main.py` (Python 3.13, standard library only) copies the
stored `entry.png` to `/output/entry.png` byte for byte,
after checking the PNG magic, the IHDR chunk, the 1 MiB
limit and the 1024×1024 limit, and re-reading the output
to confirm the copy. Two runs write identical bytes.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Bounty

[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120) — $250 shared by the 50 best-ranked entries.

## License

MIT — see [LICENSE](LICENSE).
