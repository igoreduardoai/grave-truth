# Requirements

## Introduction

Grave Truth needs a reusable local check before anyone treats a future editable project as ready to show. The check sits beside the product. It does not replace pytest, the gold cases, or the haunted demo, and it is not a third application.

Official Kiroween rules allow frameworks and libraries and require disclosure of other pre-existing code. The validation stack discloses that boundary in `THIRD_PARTY_NOTICES.md`. The stack does not submit the project and does not change the visibility of the repository.

## Requirements

### Requirement 1: Keep the deterministic contract

**User Story:** As a maintainer, I want pytest and the gold cases to stay the source of truth, so that a browser tool cannot invent a passing answer.

#### Acceptance Criteria

1. WHEN the harness runs THEN it SHALL execute `python3 -m pytest` and `python3 evals/run_evals.py` and record their exit codes and their own summary lines.
2. The harness SHALL NOT replace a gold expectation with a model score.
3. The report SHALL NOT contain an aggregate quality score.

### Requirement 2: Scripted browser journeys

**User Story:** As a maintainer, I want the haunted demo exercised in a clean browser, so that selection, paste, citation, refusal, recovery, and keyboard use are visible.

#### Acceptance Criteria

1. WHEN a scripted profile runs THEN it SHALL use a new browser context with no stored session.
2. The Grave Truth profiles SHALL cover sample EOB, sample lease, pasted text, billed versus allowed, a missing fact, empty input followed by a valid question, and keyboard activation.
3. A scripted profile SHALL be labeled as a scripted profile and SHALL NOT be labeled as an LLM synthetic user.
4. The report SHALL give completed/attempted, citation-correct/applicable, and refusal-correct/applicable counts from the profiles that ran.

### Requirement 3: Accessibility and laboratory diagnostics

**User Story:** As a maintainer, I want axe-core and Lighthouse results from the local page, so that rule findings and load metrics are recorded without becoming a fake grade.

#### Acceptance Criteria

1. WHEN axe-core runs THEN it SHALL run against the initial page and a cited EOB state, and the report SHALL list violations and incomplete results.
2. WHEN Lighthouse runs THEN it SHALL record the tool version, form factor, throttling, and metric values it actually returned.
3. A Lighthouse category figure SHALL be labeled as a laboratory diagnostic and SHALL NOT be a pass/fail gate for the harness.

### Requirement 4: One persona adapter, opt-in model

**User Story:** As a maintainer, I want one exploratory browser loop, so that a future opted-in model run has a place to go, and today's run does not pretend a model was used.

#### Acceptance Criteria

1. The persona loop SHALL be the ux-swarm-adapted loop in `validation/persona.py`, not a second stack.
2. WHEN `llm.opt_in` is false or `VALIDATION_LLM_OPT_IN` is not `1` THEN the harness SHALL make zero model calls, including when an API key variable is present.
3. A replay of configured steps SHALL be reported as an adapter test double and SHALL NOT be called an LLM synthetic user.
4. Page text passed toward a model prompt SHALL be marked as untrusted data.

### Requirement 5: Negative controls and local-only network

**User Story:** As a maintainer, I want the harness to fail on purpose when the page is wrong, so that a green report means the checks ran.

#### Acceptance Criteria

1. WHEN the planted page highlights `$999.00` THEN the citation check SHALL fail and the control SHALL be reported as caught.
2. WHEN a step targets `https://example.com` THEN the browser SHALL stay on a local host.
3. The allowlist loader SHALL reject a config whose allowlist contains a public host.

### Requirement 6: Disclosure

**User Story:** As a future reader, I want licenses and limits in the repo, so that adapted code is not mistaken for new product code.

#### Acceptance Criteria

1. The ux-swarm MIT license text SHALL be stored next to the adapted loop, with the upstream commit.
2. `THIRD_PARTY_NOTICES.md` SHALL separate copied, adapted, and new work.
3. The README quickstart SHALL be one command from the repo root.
