# Grave Truth

A lean skeleton for citation-grounded document agents, built for [Kiroween 2026](https://kiroween.devpost.com/) in the Skeleton Crew spirit: every answer cites a source span or says `not found`. Two demo apps share the same skeleton — a synthetic medical bill / EOB explainer and a synthetic lease clause checker.

This is a research demo. It is not a medical device and not legal advice. Documents in `fixtures/` are synthetic.

## How it works

1. `DocumentAgent.ingest` stores a document and splits it into sentence spans.
2. `retrieve` ranks spans by token overlap with the question.
3. `answer` quotes only those spans. Numbers that do not appear in the spans never enter the answer.
4. `reject_ungrounded_claim` flags a proposed claim when it invents a number (the “ghost”).

Uncited claims do not survive as answers (`GroundedAnswer.ghost`).

## Apps

| App | Module | Fixture |
|---|---|---|
| EOB explainer | `grave_truth.apps.eob` | `fixtures/sample_eob.txt` |
| Lease checker | `grave_truth.apps.lease` | `fixtures/sample_lease.txt` |

```python
from grave_truth.apps import eob

result = eob.explain("What is the patient responsibility?")
print(result.text, result.citations[0].span)
```

## Kiro workflow

The `/.kiro` directory is part of the repo (it is not gitignored):

- `.kiro/specs/grave-truth.md` — product spec
- `.kiro/steering/no-invention.md` — no guessed numbers or citations
- `.kiro/hooks/run-evals.json` — hook that runs `python evals/run_evals.py` (meant to fire on save in the Kiro IDE)

This tree documents the spec-driven workflow even when the code is run outside Kiro.

## Eval results

Gold cases live in `evals/gold_cases.json` (13 cases: cited-correct, not-found, and hallucination rejection).

```bash
pip install -e ".[dev]"
python evals/run_evals.py
pytest
```

Last local run (2026-11-06): `python evals/run_evals.py` → **13/13 passed**; `pytest` → **6 passed**.

## Limits

- Retrieval is lexical, not a hosted model. That keeps the demo offline and inspectable.
- One short synthetic document per app.
- No insurer, clinic, or landlord customers have used this software.

## License

MIT. Built as a new project after 30 October 2026 for Kiroween. Affiliation: Igor Eduardo, Founder in Residence, Antler.
