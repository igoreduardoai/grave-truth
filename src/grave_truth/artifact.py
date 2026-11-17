"""Deterministic workflow files built only from DocumentAgent citations.

A cited claim is copied with the span offsets that slice the document.
A claim the checker rejects is marked not found and is not asserted.
No clock and no model call, so the same fixture always yields the same file.
"""

from __future__ import annotations

from grave_truth.apps import eob, lease
from grave_truth.skeleton import DocumentAgent

EOB_CLAIMS = (
    "The patient responsibility is $42.15.",
    "The pharmacy charge is $18.40.",
    "The billed amount is $180.00.",
    "The out-of-network penalty is $50.00.",
)
LEASE_CLAIMS = (
    "The security deposit is $1,850.00 and is not rent.",
    "The late fee is $75.00.",
    "The late fee is $1,850.00.",
    "The written notice period is 14 days.",
)

_APPS = {
    "eob": {
        "kind": "dispute-letter",
        "filename": "grave-truth-dispute-letter.md",
        "title": "Synthetic dispute letter",
        "claims": EOB_CLAIMS,
        "loader": eob.load_agent,
        "fixture": eob.FIXTURE,
        "doc_id": "sample-eob",
    },
    "lease": {
        "kind": "clause-issues",
        "filename": "grave-truth-clause-issues.md",
        "title": "Synthetic clause issues",
        "claims": LEASE_CLAIMS,
        "loader": lease.load_agent,
        "fixture": lease.FIXTURE,
        "doc_id": "sample-lease",
    },
}


def build_artifact(app: str) -> dict:
    """Return the JSON document, including the markdown body, for one sample app."""
    spec = _APPS.get(app)
    if spec is None:
        raise ValueError("app must be eob or lease")
    document = spec["fixture"].read_text(encoding="utf-8")
    agent = spec["loader"]()
    items = [_judge(agent, claim) for claim in spec["claims"]]
    markdown = _markdown(spec["title"], spec["doc_id"], items)
    return {
        "kind": spec["kind"],
        "filename": spec["filename"],
        "app": app,
        "document_id": spec["doc_id"],
        "document": document,
        "live_model": "unimplemented",
        "items": items,
        "markdown": markdown,
    }


def _judge(agent: DocumentAgent, claim: str) -> dict:
    if not agent.reject_ungrounded_claim(claim):
        result = agent.answer(claim)
        if result.found and result.citations and not result.conflict:
            return {
                "claim": claim,
                "verdict": "cited",
                "citations": [
                    {
                        "doc_id": citation.doc_id,
                        "start": citation.start,
                        "end": citation.end,
                        "span": citation.span,
                    }
                    for citation in result.citations
                ],
            }
    return {"claim": claim, "verdict": "not_found", "citations": []}


def _markdown(title: str, document_id: str, items: list[dict]) -> str:
    lines = [
        f"# {title}",
        "",
        "Prepared by the offline checker in this repository. A live model was not called. "
        "This is a research demo. It is not a medical device and not legal advice.",
        "",
        f"Document: {document_id}",
        "",
        "A cited claim is stated only with the source span below it. "
        "A claim marked not found is not asserted.",
        "",
    ]
    for index, item in enumerate(items, start=1):
        lines.append(f"## {index}. {item['claim']}")
        lines.append("")
        if item["verdict"] == "cited":
            lines.append("Status: cited")
            for citation in item["citations"]:
                lines.append(
                    f'Source: {citation["doc_id"]} [{citation["start"]}:{citation["end"]}] {citation["span"]}'
                )
        else:
            lines.append("Status: not found")
            lines.append("Source: not found")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
