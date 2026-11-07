---
inclusion: always
---

# Structure

- `src/grave_truth/skeleton.py` — ingest, retrieve, answer, reject.
- `src/grave_truth/apps/eob.py` and `lease.py` — load one synthetic fixture each.
- `eob-explainer/` and `lease-checker/` — the two Skeleton Crew application folders. They call the shared library.
- `fixtures/` — synthetic source text only.
- `evals/` — gold cases and the hook runner.
- `scripts/demo_walkthrough.py` — judge transcript for both apps. Run it before claiming a demo works.
- `demos/haunted/` — offline page. Ghosts are uncited claims. A cited answer highlights the source clause.
- `tests/` — pytest, including generated-document checks.
- `.kiro/` — specs, steering, and hooks. Never gitignore this directory.

A change to grounding behavior needs a gold case: cited, not found, reject, or accept. Do not "fix" a miss by writing a number into the answer that the span does not contain.
