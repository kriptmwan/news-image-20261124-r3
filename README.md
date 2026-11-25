# The World in One Day — Tuesday, 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/kriptmwan/news-image-20261124-r3/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/kriptmwan/news-image-20261124-r3/reward.svg)](https://make.fun/bounty/news-image-20261124)

A dense newspaper front page that sums up Tuesday, 24 November 2026 in one
image: the Huawei guilty verdict leads, with the Riyadh tower strike, the
KOSPI reclaiming 5,000, and Senegal's restored AFCON title as drawn panels,
plus 18 dated one-line stories across Europe, the Middle East, the Americas
and Asia. Claims are labelled as claims.

## Run it

```sh
python3 render.py        # draws entry.png (1024x1024, deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the Python standard library and copies `entry.png` to
the output directory, so both grader runs write the same bytes. `render.py`
draws the image with Pillow at build time.

## Competition

[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124)
on make.fun — a vision-AI judge compares the images two at a time and the 50
best win rates share $100.
