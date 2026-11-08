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

`validation/report.py` writes `validation/reports/observed.json` and `OBSERVED.md`. Counts are numerators over denominators. Confirmed defects are failed scripted profiles only. axe incomplete results and the lexical-overlap note on the adversarial paste stay out of that list. UX hypotheses stay empty when the model layer did not run.

The adversarial paste is a limit of lexical retrieval: the sentence that says the billed amount is `$999.00` is text in the file, and the demo quotes a span from the file. The harness records which span won. It does not treat that sentence as an instruction to itself.

## Negative controls

`validation/fixtures/negative_wrong_citation.html` is a separate local page. It always marks `$999.00` and offers a link to `https://example.com/out`. The citation expectation for `$240.00` fails, which is the catch. The safety probe's click on "Leave" is refused before navigation.

## Demo fixes found by the keyboard and axe passes

The skip link pointed at `#result`, and that section could not take focus, so Enter changed the hash and left focus on `body`. The section now has `tabindex="-1"` and a visible focus outline. The examples container had `aria-label` on a generic `div`. It is now `role="group"`. axe-core's contrast check stays incomplete on the gradient background; that is recorded, not converted into a palette change or a pass.

## What this design does not do

It does not call a model by default, does not read personal browser state, does not submit forms to other sites, and does not score the product as a single green number. It does not merge or submit the repository.
