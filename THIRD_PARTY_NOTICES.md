# Third-party notices

Grave Truth itself is MIT, Copyright (c) 2026 Igor Eduardo. See `LICENSE`.

This file separates copied text, adapted code, new code, and packages that are pinned but not copied. It is not a claim that any upstream project endorses Grave Truth.

Checked against GitHub license metadata and the cloned trees on 2026-11-08.

## Copied

`validation/third_party/ux-swarm/LICENSE`

- Project: ux-swarm, https://github.com/masonomara/ux-swarm
- Commit: `71197bc9d4800a9ecac863e7b5eee1f121e287a5` (tag line: release 1.1.2)
- SPDX from GitHub: MIT
- What was copied: the license file only
- Copyright: Copyright (c) 2026 Mason O'Mara

No other ux-swarm source file is copied into this repository.

## Adapted

`validation/persona.py`

- Upstream file: `src/ux_swarm/agents.py`, function `run_browser_agent`, at the commit above
- License: MIT, same copyright and license file as the copied `LICENSE`
- What was kept: one action per step, an element index, a local screenshot, and the terminal actions `done` and `give_up`
- What was not taken: the litellm client, webdriver masking, a spoofed user agent, public screenshot upload, completion-rate math, and the default persona list

The rest of `validation/` is new code written for this repository: the config loader, allowlist, scripted journeys, axe and Lighthouse runners, report, and tests.

## Pinned packages, not vendored

| Package | Pin | SPDX | How it is used |
|---|---|---|---|
| playwright | Python `1.64.1` | Apache-2.0 | Scripted Chromium journeys and the adapted step loop |
| axe-core | npm `4.14.0` | MPL-2.0 | Injected unmodified into the page under test |
| lighthouse | npm `13.6.0` | Apache-2.0 | Local laboratory diagnostic |

axe-core's MPL-2.0 copyleft applies to axe-core's own files. Those files are not modified here and are not copied into git. They arrive from npm. Playwright and Lighthouse are Apache-2.0; `validation/NOTICE` names them. Their source trees are not committed.

## Inspected and not incorporated

- GhostUser, https://github.com/savkevip/ghostuser, commit `17eaef154011ef93351a127da31cd7216bdd8c8c`, MIT. Not used. The agent calls Anthropic or OpenAI, and the shipped personas are demographic sketches.
- UXAgent, https://github.com/neuhai/UXAgent. GitHub `license` is null (checked 2026-11-08). No code was copied.
- promptfoo, DeepEval, TinyTroupe, browser-use, Stagehand, Skyvern, and UXCascade. Not installed. The product answer path has no model, so those tools are not a second judge beside the gold cases.

## Product boundary

`validation/` is pre-submission test tooling. It is not one of the two Skeleton Crew applications (`eob-explainer/` and `lease-checker/`). Kiroween's published rules allow libraries and require disclosure of other pre-existing code (https://kiroween.devpost.com/rules, "New Projects Only"). The adapted ux-swarm loop is that pre-existing code. This repository has not been submitted. Eligibility is a manual check. Nothing in this file is a statement about prizes or demand.

The contradiction behavior in `src/grave_truth/skeleton.py` is new project code. It does not copy another repository. No additional third-party package was added for it.
