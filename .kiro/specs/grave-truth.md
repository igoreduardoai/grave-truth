# Spec: Grave Truth

## Intent
A reusable skeleton for citation-grounded document agents, plus two demo apps:
1. Medical bill / EOB explainer (consumer health, synthetic EOB).
2. Lease or contract clause checker (synthetic lease).

## Requirements
- Ingest plain-text documents and split them into cited spans.
- Retrieve spans by lexical overlap with the question.
- Compose answers only from retrieved spans.
- Return `not found` when nothing relevant is retrieved.
- Reject ungrounded numeric claims.
- Ship at least 10 gold eval cases covering cited-correct, abstain, and hallucination rejection.

## Non-goals
- Live insurer or landlord integrations.
- Clinical or legal advice.
- Reusing code from prior hackathon repositories.
