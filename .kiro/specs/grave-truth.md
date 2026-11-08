# Spec: Grave Truth

## Intent

A reusable skeleton for citation-grounded document agents, plus two demo apps:

1. Medical bill / EOB explainer (consumer health, synthetic EOB) in `eob-explainer/`.
2. Lease or contract clause checker (synthetic lease) in `lease-checker/`.

The feature specs that drive the implementation are:

- `.kiro/specs/citation-grounding/` — spans, abstention, and rejection of swapped numbers.
- `.kiro/specs/demo-apps/` — the two application folders and the offline CLI.
- `.kiro/specs/haunted-demo/` — the local haunted page, paste-or-pick checking, and the judge walkthrough.
- `.kiro/specs/pre-submission-validation/` — local test tooling (pytest, gold, browser, axe-core, Lighthouse, one opt-in persona loop). Not a third application.

## Requirements

- Ingest plain-text documents and split them into cited spans.
- Retrieve spans by lexical overlap with the question, preferring the clause that contains the subject.
- Compose answers only from retrieved spans.
- Return `not found` when nothing relevant is retrieved.
- Reject ungrounded numeric claims, including a true number pasted onto the wrong subject.
- Ship gold eval cases covering cited-correct, abstain, hallucination rejection, and accepted grounded claims. The floor is well above 10 cases.

## Non-goals

- Live insurer or landlord integrations.
- Clinical or legal advice.
- Reusing code from prior hackathon repositories.
- A hosted model in the answer path.
- Treating `validation/` as a third Skeleton Crew application. It is pre-submission test tooling.
