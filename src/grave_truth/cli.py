"""Offline demo CLI. Prints an answer and its citations, or a rejection."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from grave_truth.apps import eob, lease
from grave_truth.skeleton import DocumentAgent, GroundedAnswer


_DEMO_QUESTIONS = {
    "eob": "What is the patient responsibility?",
    "lease": "What is the monthly rent?",
}

USAGE = """\
Usage:
  python -m grave_truth eob [question]
  python -m grave_truth lease [question]
  python -m grave_truth file <path> [question]
  python -m grave_truth reject {eob|lease|file} <path-or-claim> [claim]

Prints the grounded answer and citation spans. Nothing is sent over the network.
Synthetic fixtures are the default documents. This is a research demo, not a
medical device and not legal advice.
"""


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    json_mode = False
    if "--json" in args:
        json_mode = True
        args.remove("--json")
    if not args or args[0] in {"-h", "--help"}:
        print(USAGE, end="")
        return 0 if args else 2

    if args[0] == "reject":
        return _reject(args[1:], json_mode)
    if args[0] in {"eob", "lease", "file"}:
        return _answer(args, json_mode)
    print(USAGE)
    return 2


def _answer(args: list[str], json_mode: bool) -> int:
    try:
        app, question, agent = _load(args)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    result = agent.answer(question)
    if json_mode:
        print(json.dumps(_answer_payload(app, question, result), indent=2))
    else:
        print(render_answer(app, question, result))
    return 0


def _reject(args: list[str], json_mode: bool) -> int:
    if not args:
        print(USAGE)
        return 2
    try:
        app, claim, agent = _load(args)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    rejected = agent.reject_ungrounded_claim(claim)
    if json_mode:
        print(json.dumps({"app": app, "claim": claim, "rejected": rejected}, indent=2))
    else:
        print(render_rejection(app, claim, rejected))
    return 0


def _load(args: list[str]) -> tuple[str, str, DocumentAgent]:
    kind = args[0]
    rest = args[1:]
    if kind == "file":
        if not rest:
            raise ValueError("file mode needs a path and a question or claim")
        path = Path(rest[0])
        question = " ".join(rest[1:]).strip()
        if not question:
            raise ValueError("file mode needs a question or claim after the path")
        if not path.is_file():
            raise ValueError(f"document not found: {path}")
        agent = DocumentAgent()
        agent.ingest(path.stem, path.read_text(encoding="utf-8"))
        return path.stem, question, agent
    if kind not in _DEMO_QUESTIONS:
        raise ValueError(f"unknown app {kind}")
    question = " ".join(rest).strip() or _DEMO_QUESTIONS[kind]
    agent = eob.load_agent() if kind == "eob" else lease.load_agent()
    return kind, question, agent


def render_answer(app: str, question: str, result: GroundedAnswer) -> str:
    lines = [
        f"App: {app}",
        f"Question: {question}",
        f"Found: {'yes' if result.found else 'no'}",
        f"Conflict: {'yes' if result.conflict else 'no'}",
        f"Ghost: {'yes' if result.ghost else 'no'}",
        f"Answer: {result.text}",
        "Citations:",
    ]
    if not result.citations:
        lines.append("- none")
    else:
        for citation in result.citations:
            lines.append(
                f"- {citation.doc_id} [{citation.start}:{citation.end}] {citation.span}"
            )
    return "\n".join(lines)


def render_rejection(app: str, claim: str, rejected: bool) -> str:
    return "\n".join(
        [
            f"App: {app}",
            f"Claim: {claim}",
            f"Rejected: {'yes' if rejected else 'no'}",
        ]
    )


def _answer_payload(app: str, question: str, result: GroundedAnswer) -> dict:
    return {
        "app": app,
        "question": question,
        "found": result.found,
        "conflict": result.conflict,
        "ghost": result.ghost,
        "answer": result.text,
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

