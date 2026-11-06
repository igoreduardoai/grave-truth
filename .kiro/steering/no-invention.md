---
inclusion: always
---

# Steering: no invented facts

- Every answer must cite a source span from an ingested document or say `not found`.
- Never invent numbers, dollar amounts, dates, names, or clauses that are not in the retrieved spans.
- A number in a different clause does not support a claim. `$1,850.00` as rent does not make `$1,850.00` the security deposit, and the allowed amount does not make the billed amount.
- Same numeric value with different formatting (`$1,850.00` and `1850`) can match. A different value cannot. `20%` is not `20` and is not `80%`.
- If a proposed claim includes a number or an id such as `CLM-20481` that the supporting clause does not contain, reject it.
- Do not add facts to make an answer helpful. Abstain.
- This repository is a research demo. It is not a medical device and not legal advice.
- Use only synthetic documents in demos and evals. No real PHI, no real leases, no secrets.
