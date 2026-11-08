# Adjudication loop

## Boundary

`validation/adjudication/` runs a bounded evaluator simulation against a critic simulation, then applies only an allowlisted edit in a workspace copy and retests. It does not call a model unless a future adapter is both opted in and actually invoked. This build does not invoke one.

The official rubric text is stored as data with a source and a retrieval date. Eligibility, deadlines, and sponsor rules stay manual and fail closed. Winner-pattern files under `validation/seeds/` are research notes, not judge preferences and not demand.

## Repairs

The only applied edit is `focusable: true` on `candidate.json` inside the scenario workspace, and only when a failed `skip_target_focusable` check is cited by both simulations. A note-only edit that does not change the check is reverted. Paths outside the workspace, shell commands, holdout files, gold files, and the rubric file are rejected. A `submitted_frozen` candidate is not edited.

## Stop

The loop stops on a clear retest, no improvement, a repeated repair, malformed output, a critique with no evidence, a missing rubric, a frozen submission, an unsafe proposal, or a failed check that agreement cannot waive. The ceiling is 3 rounds and 5 seconds. Observed cost is zero. It does not continue until a simulation awards a perfect rubric score. Rubric criteria stay `unknown`.
