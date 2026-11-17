---
inclusion: always
---

# Steering: cite or abstain

- Every number in an answer must occur in a cited span. If it does not, the answer is `not found`.
- Do not guess a number from a nearby clause, a negated sentence, or a currency code the parser does not treat as dollars.
- A proposed claim that names the wrong figure is rejected. The rejection is `not found` in the workflow file. It is not rewritten into a different figure.
- Quote the span, with its document id and character offsets, or abstain. Do not add a sentence to make the answer more helpful.
- The workflow file is deterministic. Do not add a clock, a random id, or a model completion.
- This is a research demo. It is not a medical device and not legal advice. Use synthetic documents only.
