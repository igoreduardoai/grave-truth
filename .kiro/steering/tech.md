---
inclusion: always
---

# Tech

- Python 3.11+.
- Library code lives in `src/grave_truth`. The dependency surface is the standard library plus pytest for tests.
- Retrieval is lexical: tokens, a few query aliases, and a subject window in front of each number. There is no hosted model in the answer path, so the demo runs offline.
- Gold cases in `evals/gold_cases.json` are the contract. `python3 evals/run_evals.py` and `python3 -m pytest` must stay green.
- Keep the public types `DocumentAgent`, `GroundedAnswer`, and `Citation`. Apps call `answer` and `reject_ungrounded_claim`.
- MIT license stays. Do not commit `.env` files, keys, or real personal data.
