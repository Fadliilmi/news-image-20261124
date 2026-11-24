# The World in One Picture — 24 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Fadliilmi/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Fadliilmi/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the make.fun bounty [Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124) ($100, free).

## What the image shows

A newspaper front page for **Tuesday, 24 November 2026**, drawn entirely in code (Pillow, `draw.py`) — no photographs, no borrowed artwork. Six stories from the day's real reporting, each tagged with its outlet:

- **Lead — Airspace scare over Ulleung Island:** a suspected North Korean jet enters South Korean airspace; islanders are told to take shelter, then the warning lifts within minutes. *(Reuters, AP, Yonhap)*
- **Singapore speeds up:** the economy grows 6.1% in Q3; the 2026 forecast is raised to about 6%. *(Reuters)*
- **Crypto counts as reserves:** the US regulator says crypto may count toward trading platforms' reserves — but not liquidity. *(Reuters)*
- **Chess crown on the line:** the World Championship opens in Geneva, champion Gukesh defending against Sindarov. *(The Times of India)*
- **India bets on AI:** PM Modi opens an AI centre at IIT Patna. *(The Times of India)*
- **Supermoon meets the Pleiades:** the bright full moon glides past the Seven Sisters in the night sky. *(CNET)*

## How it runs

`main.ts` (Node 22, standard library only) copies the shipped `entry.png` to the output directory, so both grader runs write byte-identical output:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`entry.png` is 1024×1024 px, under 1 MiB. To redraw it from scratch, run `python3 draw.py` (needs Pillow and the DejaVu fonts).

## License

MIT — see [LICENSE](LICENSE).
