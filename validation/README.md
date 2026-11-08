# Pre-submission validation

This directory is test tooling for a local app. It is not a third Grave Truth application, and it does not answer questions. The product remains `src/grave_truth` plus the EOB explainer, the lease checker, and the haunted demo.

The harness keeps the existing pytest and gold evals, then opens the haunted demo in a clean Chromium profile and checks scripted journeys. axe-core and Lighthouse run as diagnostics. One persona loop, adapted from [ux-swarm](https://github.com/masonomara/ux-swarm), can call a model only when you opt in. This repository's config leaves that off.

Scripted journeys are not LLM synthetic users. A replay through the adapted loop is an adapter test double, not a synthetic-user study. UX hypotheses are recorded only from a real opted-in model run. None were invented for the checked-in report.

## Quickstart

From the repo root:

```bash
sh validation/run.sh
```

That installs the `validation` extra (Playwright 1.64.1), Chromium, and the pinned npm packages if they are missing, then runs `python3 -m validation run`. The run binds the demo to `127.0.0.1` on a free port. It does not deploy, submit, or call a paid API.

Config check only:

```bash
python3 -m validation check-config
```

Another local app copies `validation/apps/grave-truth.json`, points `server_script` at its own local server, and lists scripted actions. The loader rejects any allowlist host other than `127.0.0.1` or `localhost`.

## What the Grave Truth pilot checks

Synthetic EOB and lease text only. The profiles load or select a fixture, paste a document, ask a question, require the highlighted clause, separate billed `$240.00` from allowed `$180.00`, refuse a swapped claim and a missing penalty, recover from an empty question, and move through the page with the keyboard.

A planted page that highlights `$999.00` must fail the citation check. A link to `https://example.com/out` must not be followed. Page text is data. The replay decider ignores instructions in the page.

The checked-in result is `validation/reports/OBSERVED.md`. The decision is `ready`, `not-ready`, or `insufficient-evidence` from the app config. Grave Truth stays `insufficient-evidence` while sponsor rules are manual and the holdout has misses. A skipped mandatory check is `not-ready`. There is no quality score.

Traces from the latest run stay under `validation/reports/runs/`, which is gitignored. Screenshots of the synthetic pages are in `validation/reports/evidence/`.

## Opt-in model

Both of these are required, and neither is set in the committed config:

- `llm.opt_in` true in the app JSON
- `VALIDATION_LLM_OPT_IN=1` and `VALIDATION_LLM_MODEL` in the environment

Ambient `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, and `AZURE_API_KEY` are not read when opt-in is off. If opt-in is on and `litellm` is not installed, the layer is skipped and no other model is called. Installing `litellm` can send page text to the provider named by the model string and can cost money. Do not point it at a real bill, a real lease, or anyone's personal information.

## Not included

No new third-party package was added for the contradiction rule or the readiness report. The pins above are unchanged.

GhostUser was inspected (MIT, commit `17eaef154011ef93351a127da31cd7216bdd8c8c`) and not used. Its browser agent calls Anthropic or OpenAI only, and its built-in personas are demographic sketches. ux-swarm exposes a Python step loop and custom task personas, which matches this repo and the opt-in rule. UXAgent was not copied: GitHub reports no SPDX license and the root has no `LICENSE` file.

promptfoo, DeepEval, and TinyTroupe are not installed. The product has no model in the answer path, so a model judge is not a second source of truth next to the gold cases. The adversarial paste is a deterministic citation check.

## Licenses

The repo stays MIT. Upstream obligations are in `THIRD_PARTY_NOTICES.md` and `validation/NOTICE`. axe-core is MPL-2.0 and is used unmodified from npm. Playwright and Lighthouse are Apache-2.0 packages, not vendored trees. The ux-swarm license text that covers the adapted step loop is `validation/third_party/ux-swarm/LICENSE`.
