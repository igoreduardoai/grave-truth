# Observed validation run

- Date: 2026-11-08T18:28:52+00:00
- Commit: `34e94d04e5af963b05099900bcb31e314bc3ebc0`
- Mode: local
- Observed cost: $0.0 (model API calls: 0)
- App config: `grave-truth`
- Repo: https://github.com/igoreduardoai/grave-truth

## Decision

- **insufficient-evidence**
- held-out intended behavior was not met on every case
- manual checks are not approved: sponsor_new_work, eligibility, human_review
- unresolved evidence: holdout intended 5/7: holdout-negation-only, holdout-usd-prefix; axe color-contrast incomplete remains; eyebrow versus #120e16 measured 13.17:1; the rule was not disabled; sponsor and new-work rules were not automatically verified
- Manual items are not treated as passed.
- This is not a prize estimate and not a quality score.

## Denominators

- Scripted tasks completed: 10 / 10
- Citation checks correct: 7 / 7
- Refusals correct: 3 / 3

Scripted profiles are deterministic browser steps. They are not LLM synthetic users.

## Pytest and gold

- pytest exit 0: passed 71, failed 0
- gold exit 0: 90/90

## Layers

- pytest_and_gold: exercised
- scripted_browser: exercised
- negative_controls: exercised
- browser_guards: exercised
- axe_core: exercised
- lighthouse: diagnostic
- holdout: exercised
- stability: exercised
- persona_llm: skipped
- adjudication_loop: exercised

## Adjudication loop

- Scripted fixtures. Live evaluator/critic was not validated.
- repair_demo: improved_and_clear (expected improved_and_clear)
- no_improvement: no_improvement (expected no_improvement)
- malformed: malformed_judge_output (expected malformed_judge_output)
- unsupported: unsupported_critique (expected unsupported_critique)
- missing_rubric: missing_rubric (expected missing_rubric)
- protected: protected_submission (expected protected_submission)
- unsafe: unsafe_repair (expected unsafe_repair)
- failed_blocks_ready: failed_checks_block_ready (expected failed_checks_block_ready)

## axe-core

- violations: 0
- incomplete: 2
- Rule findings are not a conformance certificate and are not a harness grade.
- incomplete color-contrast on initial (21 nodes): Elements must meet minimum color contrast ratio thresholds
- incomplete color-contrast on cited-eob (22 nodes): Elements must meet minimum color contrast ratio thresholds

## Lighthouse laboratory diagnostic

- Lighthouse 13.6.0, form factor mobile, throttling simulate, mobile emulation True
- first-contentful-paint: 901.5072
- largest-contentful-paint: 901.5072
- total-blocking-time: 0
- cumulative-layout-shift: 0
- speed-index: 901.5072
- lab category performance: 1
- lab category best-practices: 0.96
- Laboratory figures from this machine. Not a field measurement, not a harness pass/fail gate, and not a quality score for the product.

## Negative controls

- Planted citation failures caught: 3 / 3
- Off-allowlist click probe: caught

## Holdout

- Intended behavior met: 5 / 7
- Miss holdout-negation-only: intended not_found; observed The billed amount is not $240.00.
- Miss holdout-usd-prefix: intended not_found; observed The billed amount is USD 240.

## Confirmed defects

No scripted profile failed in this run.

## Limitations and hypotheses

- No extra limitations were recorded by the profiles.
- No UX hypotheses. The LLM persona runner was not exercised, so none were invented.

## Persona

- LLM runner: skipped. LLM persona runner was not exercised. Opt-in is off.
- Adapter test double: exercised (adapter test double, not an LLM synthetic user).

## Versions

- python: 3.12.3
- playwright: 1.64.1
- axe_core: 4.14.0
- lighthouse: 13.6.0
- chromium_executable: /home/ubuntu/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome
- ux_swarm_adapted_from: 71197bc9d4800a9ecac863e7b5eee1f121e287a5
- ghostuser_evaluated_not_used: 17eaef154011ef93351a127da31cd7216bdd8c8c

This report has no aggregate quality score and does not claim a prize.
