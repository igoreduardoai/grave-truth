# Design

## Boundary

`validation/` is a local runner. The haunted server and `DocumentAgent` stay the product. The runner starts `demos/haunted/server.py` on `127.0.0.1` with port 0, drives it, and stops it. It does not add a ranker and it does not open a public port.

Per-app behavior lives in `validation/apps/<id>.json`. `python3 -m validation run` loads `grave-truth` unless `--app` is passed. `check-config` only validates the file.

## Layers

1. **Pytest and gold.** Subprocess the existing commands and parse the summary the tools print. A missing summary is a failure. There is no stored "expected 90" inside the parser.
2. **Scripted Playwright profiles.** Each profile is a list of actions (`check`, `fill`, `click`, `press`, `expect_*`) in a fresh context. The route hook aborts any URL that is not `localhost` or `127.0.0.1`. These profiles are the pilot. They are not personas.
3. **axe-core.** The pinned npm package is injected with `addScriptTag`. The runner asks for violations and incomplete results, not a pass rate.
4. **Lighthouse.** The pinned CLI runs once against the demo URL with Playwright's Chromium. Mobile simulated throttling is Lighthouse's default. The numbers are copied from its JSON.
5. **Persona loop.** `validation/persona.py` adapts the ux-swarm browser step. The checked-in Grave Truth run uses `ReplayDecider`, which replays `persona_double.steps` and ignores page text. The LLM gate stays closed unless the JSON and the environment both opt in. `LlmDecider` is the only caller of `litellm`, and that import is inside the call.

GhostUser was the other candidate. It was not adapted because a run requires an Anthropic or OpenAI key and its default personas are demographic. One loop is enough.

## Report

`validation/report.py` writes `validation/reports/observed.json` and `OBSERVED.md`. Counts are numerators over denominators. Confirmed defects are failed scripted profiles only. The decision is separate from those counts. UX hypotheses stay empty when the model layer did not run.

A pasted document that states two billed amounts is a conflict. The page shows both original spans and does not select one. The harness expects that conflict verdict. Instructions in the file do not suppress the citation.

## Negative controls

`validation/fixtures/negative_wrong_citation.html` always marks `$999.00` and links to `https://example.com/out`, with a form that posts to `https://example.com/submit`. The citation check fails, and both the link and the submit button are refused. `negative_keyboard.html` has a skip link whose target cannot take focus, so the focus check fails. `negative_recovery.html` shows the empty-input error and never produces a citation. Each of those failures is the catch.

## Decision

The app config names mandatory, diagnostic, optional, and manual checks. Skipped or failed mandatory checks are `not-ready`. Open manual checks, holdout misses, and axe incomplete results are `insufficient-evidence`. `ready` is not issued while those remain. Sponsor rules are manual. There is no score and no prize claim.

## Demo fixes found by the keyboard and axe passes

The skip link pointed at `#result`, and that section could not take focus, so Enter changed the hash and left focus on `body`. The section now has `tabindex="-1"` and a visible focus outline. The examples container had `aria-label` on a generic `div`. It is now `role="group"`. axe-core's contrast check stays incomplete because the body background is a gradient. The eyebrow color `#f0d48a` on the declared background `#120e16` measures 13.17:1, above the 4.5:1 AA threshold for normal text. The rule is still enabled. The incomplete result stays in the report.

## What this design does not do

It does not call a model by default, does not read personal browser state, does not submit forms to other sites, and does not score the product as a single green number. It does not merge or submit the repository.
