"""Score gold cases against a DocumentAgent. Shared by pytest and the eval runner."""

from __future__ import annotations

import re
from typing import Any

_NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")

_DOC_IDS = {"eob": "sample-eob", "lease": "sample-lease"}


def evaluate_case(case: dict[str, Any], agent: Any) -> tuple[bool, str]:
    expect = case["expect"]
    question = case["question"]
    if expect == "reject_ungrounded":
        rejected = agent.reject_ungrounded_claim(question)
        return rejected is True, f"rejected={rejected}"
    if expect == "accept_grounded":
        rejected = agent.reject_ungrounded_claim(question)
        return rejected is False, f"rejected={rejected}"

    result = agent.answer(question)
    if expect == "not_found":
        ok = (not result.found) and result.text == "not found" and result.citations == []
        return ok, f"found={result.found} text={result.text!r} citations={len(result.citations)}"
    if expect != "cited":
        return False, f"unknown expect {expect}"

    ok = bool(result.found and result.citations)
    for needle in case.get("must_include", []):
        present = needle in result.text or any(needle in citation.span for citation in result.citations)
        ok = ok and present
    for group in case.get("citation_groups", []):
        ok = ok and any(all(needle in citation.span for needle in group) for citation in result.citations)
    if "max_citations" in case:
        ok = ok and len(result.citations) <= case["max_citations"]
    if "min_citations" in case:
        ok = ok and len(result.citations) >= case["min_citations"]
    expected_doc = _DOC_IDS.get(case.get("app", ""))
    if expected_doc:
        ok = ok and all(citation.doc_id == expected_doc for citation in result.citations)
    if result.found:
        for number in _NUMBER.findall(result.text):
            if not any(number in citation.span for citation in result.citations):
                ok = False
        for citation in result.citations:
            if not citation.span or citation.end < citation.start:
                ok = False
    detail = f"text={result.text!r} citations={[c.span for c in result.citations]}"
    return ok, detail
