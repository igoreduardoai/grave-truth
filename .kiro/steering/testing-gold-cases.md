---
inclusion: fileMatch
fileMatchPattern: ["evals/**/*.py", "evals/**/*.json", "tests/**/*.py"]
---

# Gold cases

Each case is one object in `evals/gold_cases.json`.

- `expect: cited` — `answer` is found, citations are non-empty, and `citation_groups` each occur together inside one span.
- `expect: not_found` — text is exactly `not found` and citations are empty.
- `expect: reject_ungrounded` — `reject_ungrounded_claim` is true.
- `expect: accept_grounded` — the claim's numbers and ids are in the clause that states that subject, so rejection is false.

Use `max_citations: 1` when one clause should win. Use `min_citations` when two clauses must both surface, as with the shared `$1,850.00` rent and deposit.

Add the case before tuning the ranker. A new fixture sentence must stay synthetic.
