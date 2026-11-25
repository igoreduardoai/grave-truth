# Requirements

### Requirement 1: Separate gates

1. WHEN a deterministic check fails THEN a simulation that says the work is ready SHALL NOT mark it ready.
2. WHEN a rubric criterion has no mapped measurement THEN its status SHALL stay `unknown`.
3. Winner-pattern priors SHALL NOT override the rubric or a failed check.

### Requirement 2: Bounded repair

1. WHEN the skip-target check fails and both simulations cite that check THEN the loop MAY set `focusable` true on the workspace candidate and SHALL retest.
2. WHEN a repair does not change the failed checks THEN the loop SHALL revert it and stop.
3. WHEN a proposal contains a command, a parent-directory path, or a protected filename THEN the loop SHALL reject it and SHALL NOT change holdout, gold, or rubric files.
4. WHEN the candidate is `submitted_frozen` THEN the loop SHALL NOT edit it.
5. The loop SHALL stop by 3 rounds or 5 seconds.

### Requirement 3: Honest labels

1. Scripted reviewers SHALL be labeled `simulation` and SHALL NOT be described as live judges.
2. IF live opt-in is absent OR no free adapter is authorized THEN the live loop SHALL be reported as not validated, and provider keys SHALL NOT be read.
