---
inclusion: auto
name: add-gold-case
description: Use when adding or editing gold eval cases, fixtures, the grader, or hallucination checks for Grave Truth.
---

# Adding a gold case

1. Pick the app, `eob` or `lease`, and one expectation: cited, not found, reject_ungrounded, or accept_grounded.
2. Phrase the question with words that appear in the fixture when the case should cite. For not-found, use a topic the fixture never mentions.
3. For a rejection, put the real subject next to a number that belongs to a different subject, or use a value that is absent.
4. For an acceptance, every number and id in the claim must sit in that subject's clause.
5. Run `python3 evals/run_evals.py` and `python3 -m pytest`. Do not weaken an existing case to make a new one pass.
