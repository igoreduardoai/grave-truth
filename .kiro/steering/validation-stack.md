---
inclusion: fileMatch
fileMatchPattern: ["validation/**", "tests/test_validation_stack.py", "THIRD_PARTY_NOTICES.md"]
---

# Validation stack

`validation/` is local test tooling. It is not a third application and it does not change `DocumentAgent`.

- Run it with `sh validation/run.sh` from the repo root.
- Scripted browser profiles are not LLM synthetic users.
- Do not set `llm.opt_in` or `VALIDATION_LLM_OPT_IN` in a committed file. Ambient API keys are not a fallback.
- Do not add a public host to an allowlist. The loader rejects it.
- Do not copy UXAgent. Its GitHub license metadata is null.
- Record a failed scripted profile as a confirmed defect. Keep axe incomplete results, Lighthouse laboratory figures, and retrieval limits out of that list.
- Do not write an aggregate quality score into the report.
- Synthetic fixtures only. No real bill, lease, or personal browser profile.
