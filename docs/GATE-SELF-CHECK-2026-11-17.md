# Gate self-check — 2026-11-17

This is a self-check. It is not the output of `python -m judge_stack`.

The gate package `judge_stack` (private repository `igoreduardoai/hackathon-lab`) is not installed in this repository, and the command was not executed here. The item names below follow that gate’s criteria file as read on 2026-11-17, plus B7 from the task brief. B7 is not an id in the criteria file that was read. The task names B7 as external confirmation.

A checked line in this file is not a `judge_stack` pass.

## Blocking items

| Id | Self-check | Evidence |
|---|---|---|
| B1 storyboard | PASS | `demos/haunted/index.html` hero lists Input, Check, and Result. `gallery/01-hero.png` is a Playwright shot of that screen. `tests/test_hero_screen.py`. |
| B1 five-second person | needs-human | No person is recorded here saying what the screen does. This file does not invent that sentence. |
| B1 video, first 20 seconds | needs-human | There is no video in this repository. |
| B2 final action | PASS | The demo ends in a markdown file. Cited claims carry span offsets. `tests/test_export_artifact.py`, `GET /api/export`. |
| B3 sponsor depth | PASS, with the limit in the matrix | Three capabilities (steering, specs, hook) plus keyless MCP. The measured number is 0 of 17 not-found gold cases cited, against 17 of 17 for a first-sentence quoter. `docs/KIRO-CAPABILITY-MATRIX.md`. This run did not record a Kiro IDE session, so the number is a pytest contrast, not an IDE trace. |
| B4 not the advertised use case | PASS as a written angle only | The hackathon overview retrieved 2026-11-17 (https://kiroween.devpost.com/) asks entrants to use specs, hooks, steering, and MCP. It does not advertise a bill or lease checker that refuses a figure from the wrong sentence and ends in a downloadable letter. No user research is claimed. |
| B4 one named person | needs-human | The README describes the task on the synthetic fixtures and the workaround of scanning the page by eye. It does not name a real person, and this check does not invent one. |
| B5 stable demo URL | needs-human | `GET /health` is static and `?judge=1` runs without an API key (`tests/test_judge_mode.py`). `site/` is a static build (`python3 scripts/build_static.py`) and was not deployed. There is no Vercel or Hugging Face URL. |
| B6 rules read | PASS for the dated quotes | `docs/KIROWEEN-RULES-CHECK.md` quotes the rules page retrieved 2026-11-17, including the Pacific deadline and the America/Chicago conversion of that instant. This does not prove the rules were read before the first commit of the project. |
| B6 anonymous visibility and video | needs-human | `LICENSE` is MIT at the repository root. Repo visibility was not changed. No private-window check and no video check were done. |
| B public text | FAIL on 2026-11-17 | The README license section and `.kiro/steering/product.md` contained the forbidden public substring. That sentence was removed on 2026-11-20. This file does not add a street address. |
| B7 external confirmer | needs-human | No external confirmer is recorded. The video is also needs-human. |

## Advisory items this check did not treat as passing

Screenshots: `gallery/` holds Playwright PNGs and `gallery/axe-report.json`. The gate’s advisory bar is 8 real shots. Count them from the directory. This self-check does not look at pixels.

Lighthouse was not re-run for this increment. Do not reuse an older laboratory figure as a new score.

The scripted adjudication loop was not used as a signal. It remains a simulation.
