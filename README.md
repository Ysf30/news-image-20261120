# news-image-20261120

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Ysf30/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Ysf30/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

One image summing up Friday 20 November 2026 world news, drawn as a
newspaper front page: Cyclone Akvan bearing down on India, the Trump–Xi–
Putin "Peace Declaration" after the first-ever trilateral talks in
Shenzhen, the ICJ ruling that Myanmar committed genocide against the
Rohingya, and 30+ more real stories from the day, with a day-in-figures
band and a world-news ticker.

## Run

```sh
python3 build_image.py   # renders entry.png (1024x1024, deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

`main.py` (Python 3.13, standard library only) copies the image this
repository holds to `/output/entry.png`, byte for byte, with a sha256
check and a gate check (whole PNG, 1024x1024 at most, under 1 MiB).
Re-running it writes identical bytes every time.
`build_image.py` draws the front page from scratch with Pillow:
masthead, cyclone map of the Bay of Bengal, three flags, figures band,
and three columns of short stories.

## Bounty

[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120) — $250 shared by the 50 best-ranked entries.

## License

MIT — see [LICENSE](LICENSE).
