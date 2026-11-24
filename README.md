# news-image-20261124-entry

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dillahhhh/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dillahhhh/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper front page summing up Tuesday 24 November 2026 in a single 1024×1024 image: 13 verified stories across 5 regions, a stats bar, a world map with 12 numbered places, a UTC timeline of the day, and a date-check box that names the big near-misses left out on purpose (COP31's collapse on 22 Nov, the Merkury sinking on 22–23 Nov, the CrowdStrike–Zscaler deal announced 23 Nov). Every fact was checked against its source (Reuters, Associated Press, Wall Street Journal, Zacks, UN News / WHO, OneTurn) before anything was drawn.

## Run it

```sh
python3 render.py   # rebuild entry.png from stories.json (needs Pillow)
python3 main.py     # write /output/entry.png
```

`main.py` uses only the standard library and copies the rendered image, so the graded run is byte-identical every time.

---

<sub>Entered on [make.fun](https://make.fun/?ref=00tr9yqb&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
