"""Citation-grounded document agent skeleton.

Every answer must quote a source span or return not found.
Numbers that do not appear in retrieved spans are never invented.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
_TOKEN = re.compile(r"[a-z0-9$%./-]+")
_NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")
_STOP = {
    "a", "an", "the", "is", "are", "was", "were", "of", "to", "in", "on",
    "for", "and", "or", "my", "our", "your", "their", "this", "that", "what",
    "how", "when", "where", "who", "does", "do", "did", "can", "i", "me",
    "we", "it", "be", "with", "at", "from", "as", "by",
}
_WEAK = {"fee", "amount", "day", "days", "month", "monthly", "written", "document", "visit", "unit"}


@dataclass(frozen=True)
class Citation:
    doc_id: str
    span: str
    start: int
    end: int


@dataclass
class GroundedAnswer:
    text: str
    citations: list[Citation] = field(default_factory=list)
    found: bool = False

    @property
    def ghost(self) -> bool:
        """Uncited claims are ghosts: they must not survive as answers."""
        return not self.found or not self.citations


@dataclass
class _Chunk:
    doc_id: str
    text: str
    start: int
    end: int


class DocumentAgent:
    def __init__(self) -> None:
        self._docs: dict[str, str] = {}
        self._chunks: list[_Chunk] = []

    def ingest(self, doc_id: str, text: str) -> None:
        if not doc_id or not text.strip():
            raise ValueError("doc_id and text are required")
        self._docs[doc_id] = text
        offset = 0
        for raw in _SENTENCE_SPLIT.split(text.strip()):
            sentence = raw.strip()
            if not sentence:
                continue
            start = text.find(sentence, offset)
            if start < 0:
                start = offset
            end = start + len(sentence)
            offset = end
            self._chunks.append(_Chunk(doc_id, sentence, start, end))

    def retrieve(self, question: str, limit: int = 4) -> list[_Chunk]:
        q_tokens = _tokens(question)
        if not q_tokens:
            return []
        scored: list[tuple[float, _Chunk]] = []
        distinctive = {tok for tok in q_tokens if tok not in _WEAK}
        for chunk in self._chunks:
            c_tokens = _tokens(chunk.text)
            overlap = q_tokens & c_tokens
            if not overlap:
                continue
            if distinctive and not (distinctive & c_tokens):
                continue
            score = len(overlap) / len(q_tokens)
            scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:limit]]

    def answer(self, question: str) -> GroundedAnswer:
        hits = self.retrieve(question)
        if not hits:
            return GroundedAnswer(text="not found", citations=[], found=False)

        citations = [
            Citation(doc_id=h.doc_id, span=h.text, start=h.start, end=h.end)
            for h in hits
        ]
        allowed_numbers = set()
        for hit in hits:
            allowed_numbers.update(_NUMBER.findall(hit.text))

        composed = " ".join(hit.text for hit in hits)
        cleaned_parts = []
        for token in composed.split():
            numbers = _NUMBER.findall(token)
            if numbers and any(n not in allowed_numbers for n in numbers):
                continue
            cleaned_parts.append(token)
        text = " ".join(cleaned_parts).strip() or "not found"
        if text == "not found":
            return GroundedAnswer(text="not found", citations=[], found=False)
        return GroundedAnswer(text=text, citations=citations, found=True)

    def reject_ungrounded_claim(self, claim: str) -> bool:
        """Return True when a proposed claim has no supporting span."""
        result = self.answer(claim)
        if not result.found:
            return True
        claim_numbers = set(_NUMBER.findall(claim))
        span_numbers = set()
        for citation in result.citations:
            span_numbers.update(_NUMBER.findall(citation.span))
        invented = claim_numbers - span_numbers
        return bool(invented)


def _tokens(text: str) -> set[str]:
    return {tok for tok in _TOKEN.findall(text.lower()) if tok not in _STOP and len(tok) > 1}
