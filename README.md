# news-image-nov-17

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/wenjinqin/news-image-nov-17/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/wenjinqin/news-image-nov-17/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One page that sums up the world news of **Tuesday 17 November 2026**, drawn
entirely with code — no photographs, no stock art. The front page leads with
Ukraine's strike on the Crimea bridge and carries five more of the day's
stories as illustrated panels:

- **Ukraine blows up the Crimea bridge** — Zelenskyy hails an "unprecedented"
  strike on the Kerch link; Russia answers by hitting two bridges in Kyiv.
- **Iran drones hit US radar in Bahrain** — a third attack in days; Bahrain
  says the drones were intercepted.
- **Xi, Trump, Putin meet in Shenzhen** — Beijing confirms the first
  US–China–Russia summit, set for 19 November.
- **Japan jets scramble at Russian planes** — Tokyo protests an airspace
  violation by suspected Russian aircraft.
- **Hack spreads to 178 websites** — malicious code slipped in via Optimizely
  targeted visitors to CNN, BBC, Zoom and HSBC.
- **Vulcan rocket fails, 40 satellites lost** — the ULA rocket breaks up
  minutes after liftoff from Florida.

A ticker along the bottom adds the EU's new Russia sanctions, UK sanctions
on West Bank settlement firms, a deadly drone strike in Sudan and the ILO
chief's re-election.

`draw.py` renders `entry.png` (1024 × 1024) with Pillow; `main.ts` is the
contest program — it validates the image and copies it to
`/output/entry.png` in the grading sandbox.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
python3 draw.py                                       # regenerates entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=d5a50dzy&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
