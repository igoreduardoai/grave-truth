---
inclusion: manual
---

# Offline demo

From the repo root, after `python3 -m pip install -e ".[dev]"`:

```bash
python3 -m grave_truth eob "What is the patient responsibility?"
python3 -m grave_truth lease "What is the security deposit?"
python3 -m grave_truth reject eob "The billed amount is $180.00."
python3 eob-explainer/main.py
python3 lease-checker/main.py "How many days written notice are required to terminate?"
```

Read the `Citations:` lines. The span is the answer. `Found: no` means the fixture does not say. `Rejected: yes` means the claim's number is not in the matching clause.

Invoke this note with `#demo-walkthrough` when you want the judge path and not the ranker internals.
