# Observed validation run

- Date: 2026-11-08T17:42:12+00:00
- Commit: `dca54ec67201dfbb820b35a638ad1566a46f4e28`
- Mode: local
- Observed cost: $0.0 (model API calls: 0)
- App config: `grave-truth`

## Denominators

- Scripted tasks completed: 10 / 10
- Citation checks correct: 7 / 7
- Refusals correct: 3 / 3

Scripted profiles are deterministic browser steps. They are not LLM synthetic users.

## Pytest and gold

- pytest exit 0: passed 53, failed 0
- gold exit 0: 90/90

## Layers

- pytest_and_gold: exercised
- scripted_browser: exercised
- axe_core: exercised
- lighthouse: diagnostic
- persona_llm: skipped

## axe-core

- violations: 0
- incomplete: 2
- Rule findings are not a conformance certificate and are not a harness grade.
- incomplete color-contrast on initial (21 nodes): Elements must meet minimum color contrast ratio thresholds
- incomplete color-contrast on cited-eob (22 nodes): Elements must meet minimum color contrast ratio thresholds

## Lighthouse laboratory diagnostic

- Lighthouse 13.6.0, form factor mobile, throttling simulate, mobile emulation True
- first-contentful-paint: 902.1451
- largest-contentful-paint: 902.1451
- total-blocking-time: 0
- cumulative-layout-shift: 0
- speed-index: 902.1451
- lab category performance: 1
- lab category best-practices: 0.96
- Laboratory figures from this machine. Not a field measurement, not a harness pass/fail gate, and not a quality score for the product.

## Negative controls

- Planted citation failures caught: 1 / 1
- Off-allowlist click probe: caught

## Confirmed defects

No scripted profile failed in this run.

## Limitations and hypotheses

- Limitation: The cited span included the pasted sentence that says the billed amount is $999.00. That sentence is in the document, so the quote is still a slice of the file, and the page did not drop the citation when the sentence said not to cite. Lexical overlap preferred that sentence over 'The billed amount is $240.00.' This is a retrieval limit, not an instruction the harness followed.
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

This report has no aggregate quality score.
