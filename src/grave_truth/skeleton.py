"""Citation-grounded document agent skeleton.

Every answer must quote a source span or return not found.
Numbers that do not appear in a supporting span are never invented.
A number counts as support only when it sits in the same clause as the
claim's subject, so a figure from one fact cannot launder a different fact.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
_TOKEN = re.compile(r"[a-z0-9$%./-]+")
_NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")
_IDENT = re.compile(r"\b[A-Za-z]{2,}-\d+\b")
_STOP = {
    "a", "an", "the", "is", "are", "was", "were", "of", "to", "in", "on",
    "for", "and", "or", "my", "our", "your", "their", "this", "that", "what",
    "how", "when", "where", "who", "does", "do", "did", "can", "i", "me",
    "we", "it", "be", "with", "at", "from", "as", "by", "without", "after",
    "before", "about", "into", "over", "than", "each", "not", "no", "if",
    "per", "up", "inside", "there", "been", "has", "had", "have", "any",
    "such", "other", "only", "also", "its", "which", "whose", "whom",
    "much", "many", "left", "used", "using", "issued", "percentage",
}
_WEAK = {
    "fee", "amount", "day", "days", "month", "monthly", "written", "document",
    "visit", "unit", "allowed", "prohibited", "required", "number",
}
_GENERIC = {
    "synthetic", "explanation", "benefit", "benefits", "residential",
    "document", "lease",
}
_PLURALS = {
    "pets": "pet",
    "doctors": "doctor",
    "physicians": "physician",
    "renters": "renter",
    "residents": "resident",
    "days": "day",
    "notices": "notice",
    "fees": "fee",
    "amounts": "amount",
    "benefits": "benefit",
    "deposits": "deposit",
    "guests": "guest",
    "providers": "provider",
    "begins": "begin",
    "ends": "end",
    "months": "month",
}
# Same word, different inflection. Applied to the document and the question.
_LEMMAS = {
    "pay": "paid",
    "pays": "paid",
}
# Query-side paraphrases only. The answer text is still a source span.
_QUERY_ALIASES = {
    "doctor": "provider",
    "physician": "provider",
    "clinician": "provider",
    "renter": "resident",
    "tenant": "resident",
    "termination": "terminate",
    "terminating": "terminate",
}
_MIN_SCORE = 0.22
_NEAR_TIE = 0.55
_SUBJECT_WINDOW = 60
_NEGATION = re.compile(r"\b(?:not|never|no|without)\b", re.IGNORECASE)


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
    conflict: bool = False

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
        self._chunks = [chunk for chunk in self._chunks if chunk.doc_id != doc_id]
        for sentence, start, end in _split_spans(text):
            self._chunks.append(_Chunk(doc_id, sentence, start, end))

    def retrieve(self, question: str, limit: int = 4) -> list[_Chunk]:
        query_tokens, query_bigrams = _analyze_query(question)
        if not query_tokens and not _norm_numbers(question):
            return []
        idf = _idf_map(self._chunks)
        if _asks_for_absent_subject(query_tokens, idf):
            return []
        query_numbers = _norm_numbers(question)
        q_content = _content(query_tokens)
        known = {tok for tok in query_tokens if tok in idf}
        ranked: list[tuple[float, _Chunk]] = []
        for chunk in self._chunks:
            score = _score_chunk(
                query_tokens,
                query_bigrams,
                q_content,
                known,
                query_numbers,
                chunk.text,
                idf,
                len(self._chunks),
            )
            if score >= _MIN_SCORE:
                ranked.append((score, chunk))
        ranked.sort(key=lambda item: (-item[0], item[1].start))
        if not ranked:
            return []
        return _select_spans(ranked, q_content, limit)

    def answer(self, question: str) -> GroundedAnswer:
        conflict = _contradictory_chunks(self._chunks, question)
        if conflict:
            return self._quote(conflict, conflict=True)
        hits = self.retrieve(question, limit=2)
        if not hits:
            return _not_found()
        negated = _primary_chunks(self._chunks, question, negated=True)
        if negated:
            positive = _primary_chunks(self._chunks, question, negated=False)
            if positive:
                neg_keys = {(chunk.doc_id, chunk.start, chunk.end) for chunk in negated}
                kept = [hit for hit in hits if (hit.doc_id, hit.start, hit.end) not in neg_keys]
                hits = kept or positive[:2]
        return self._quote(hits, conflict=False)

    def _quote(self, chunks: list[_Chunk], *, conflict: bool) -> GroundedAnswer:
        citations = [
            Citation(doc_id=chunk.doc_id, span=chunk.text, start=chunk.start, end=chunk.end)
            for chunk in sorted(chunks, key=lambda chunk: (chunk.doc_id, chunk.start))
        ]
        for citation in citations:
            source = self._docs.get(citation.doc_id, "")
            if source[citation.start:citation.end] != citation.span:
                return _not_found()
        text = " ".join(citation.span for citation in citations).strip()
        if not text or not _numbers_covered(text, [citation.span for citation in citations]):
            return _not_found()
        return GroundedAnswer(text=text, citations=citations, found=True, conflict=conflict)

    def reject_ungrounded_claim(self, claim: str) -> bool:
        """Return True when a proposed claim has no unique supporting span.

        A number is supported only when that same value appears in a span
        and the words just before it match the claim's subject. A dollar
        amount that belongs to a different clause does not count. Two
        different figures for the same subject are not a unique support.
        """
        if _contradictory_chunks(self._chunks, claim):
            return True
        if not self._chunks:
            return True
        numbers = _norm_numbers(claim)
        idents = _idents(claim)
        if not numbers and not idents:
            return not self.retrieve(claim)
        for number in numbers:
            if not any(_number_supported(claim, chunk.text, number) for chunk in self._chunks):
                return True
        for ident in idents:
            if not any(_ident_supported(claim, chunk.text, ident) for chunk in self._chunks):
                return True
        return False


def _not_found() -> GroundedAnswer:
    return GroundedAnswer(text="not found", citations=[], found=False)


def _split_spans(text: str) -> list[tuple[str, int, int]]:
    spans: list[tuple[str, int, int]] = []
    offset = 0
    for raw in _SENTENCE_SPLIT.split(text.strip()):
        sentence = raw.strip()
        if len(sentence) < 2:
            continue
        start = text.find(sentence, offset)
        if start < 0:
            start = text.find(sentence)
        if start < 0:
            continue
        end = start + len(sentence)
        if text[start:end] != sentence:
            continue
        spans.append((sentence, start, end))
        offset = end
    return spans


def _token_list(text: str) -> list[str]:
    tokens: list[str] = []
    for tok in _TOKEN.findall(text.lower()):
        # The pattern keeps decimal points inside $42.15. A sentence-final
        # period would otherwise glue onto the last word ("notice.").
        tok = tok.strip(".")
        if len(tok) <= 1 or tok in _STOP:
            continue
        tok = _PLURALS.get(tok, tok)
        tok = _LEMMAS.get(tok, tok)
        if len(tok) <= 1 or tok in _STOP:
            continue
        tokens.append(tok)
    return tokens


def _analyze_query(text: str) -> tuple[list[str], set[tuple[str, str]]]:
    base = _token_list(text)
    bigrams = _meaningful_bigrams(base)
    expanded = list(base)
    for tok in base:
        alias = _QUERY_ALIASES.get(tok)
        if alias and alias not in expanded:
            expanded.append(alias)
    return expanded, bigrams


def _meaningful_bigrams(tokens: list[str]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for left, right in zip(tokens, tokens[1:]):
        if left in _GENERIC or right in _GENERIC:
            continue
        if left in _WEAK and right in _WEAK:
            continue
        pairs.add((left, right))
    return pairs


def _asks_for_absent_subject(query_tokens: list[str], idf: dict[str, float]) -> bool:
    """Abstain when the question names a subject the corpus does not contain.

    Alias sources such as "doctor" are allowed when the alias itself is in
    the corpus. Filler words never reach this check because they are not
    content tokens.
    """
    for tok in _content(query_tokens):
        if tok in idf:
            continue
        alias = _QUERY_ALIASES.get(tok)
        if alias and alias in idf:
            continue
        return True
    return False


def _content(tokens: list[str]) -> set[str]:
    return {
        tok
        for tok in tokens
        if tok not in _WEAK and tok not in _GENERIC and not _is_number_token(tok)
    }


def _is_number_token(tok: str) -> bool:
    return _NUMBER.fullmatch(tok) is not None


def _idf_map(chunks: list[_Chunk]) -> dict[str, float]:
    df: dict[str, int] = {}
    for chunk in chunks:
        for tok in set(_token_list(chunk.text)):
            df[tok] = df.get(tok, 0) + 1
    n = max(len(chunks), 1)
    return {tok: math.log((1 + n) / (1 + freq)) + 1.0 for tok, freq in df.items()}


def _idf_value(tok: str, idf: dict[str, float], n_chunks: int) -> float:
    if tok in idf:
        return idf[tok]
    return math.log(1 + max(n_chunks, 1)) + 1.0


def _score_chunk(
    query_tokens: list[str],
    query_bigrams: set[tuple[str, str]],
    q_content: set[str],
    known_query_tokens: set[str],
    query_numbers: set[str],
    text: str,
    idf: dict[str, float],
    n_chunks: int,
) -> float:
    chunk_tokens = _token_list(text)
    chunk_set = set(chunk_tokens)
    q_set = set(query_tokens)
    overlap = q_set & chunk_set
    content_overlap = q_content & _content(chunk_tokens)
    bigrams = query_bigrams & _meaningful_bigrams(chunk_tokens)
    number_hit = bool(query_numbers & _norm_numbers(text))
    if not content_overlap and not bigrams and not number_hit:
        return 0.0
    denominator_terms = known_query_tokens or (q_set & chunk_set)
    if not denominator_terms and not (query_numbers & _norm_numbers(text)):
        return 0.0
    weight = sum(_idf_value(tok, idf, n_chunks) for tok in overlap)
    denom = sum(_idf_value(tok, idf, n_chunks) for tok in denominator_terms) or 1.0
    score = weight / denom
    score += 0.4 * len(bigrams)
    if q_content and content_overlap == q_content:
        score += 0.3
    focus_pool = [tok for tok in q_content if tok in idf]
    if focus_pool:
        focus = max(focus_pool, key=lambda tok: (_idf_value(tok, idf, n_chunks), len(tok)))
        if focus in chunk_set:
            score += 0.35
        else:
            score -= 0.05
    chunk_numbers = _norm_numbers(text)
    if query_numbers and (query_numbers & chunk_numbers):
        score += 0.45
    elif query_numbers:
        score -= 0.2
    if score <= 0:
        return 0.0
    return score


def _select_spans(
    ranked: list[tuple[float, _Chunk]],
    q_content: set[str],
    limit: int,
) -> list[_Chunk]:
    if limit <= 0:
        return []
    best = ranked[0][0]
    selected: list[_Chunk] = []
    covered: set[str] = set()
    for score, chunk in ranked:
        chunk_content = _content(_token_list(chunk.text))
        fresh = (q_content & chunk_content) - covered
        if not selected:
            selected.append(chunk)
            covered |= q_content & chunk_content
            continue
        if len(selected) >= limit or score < best * _NEAR_TIE:
            continue
        if not q_content:
            # A shared amount with no subject is ambiguous: keep each near-tie span.
            selected.append(chunk)
            continue
        if not fresh:
            continue
        selected.append(chunk)
        covered |= fresh
    selected.sort(key=lambda chunk: (chunk.doc_id, chunk.start))
    return selected


def _norm_number(raw: str) -> str | None:
    text = raw.strip().lower().replace(",", "")
    kind = "pct" if text.endswith("%") else "num"
    if text.endswith("%"):
        text = text[:-1]
    if text.startswith("$"):
        text = text[1:]
    if not text:
        return None
    try:
        value = Decimal(text)
    except InvalidOperation:
        return None
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return f"{kind}:{rendered or '0'}"


def _norm_numbers(text: str) -> set[str]:
    found: set[str] = set()
    for raw in _NUMBER.findall(text):
        norm = _norm_number(raw)
        if norm:
            found.add(norm)
    return found


def _idents(text: str) -> set[str]:
    return {match.group(0).upper() for match in _IDENT.finditer(text)}


def _numbers_covered(text: str, spans: list[str]) -> bool:
    allowed: set[str] = set()
    for span in spans:
        allowed.update(_NUMBER.findall(span))
    return all(number in allowed for number in _NUMBER.findall(text))


def _subject_hits(text: str) -> list[tuple[str, set[str], bool]]:
    """Numbers, the subject words in front of them, and whether that prefix negates them.

    The prefix stops at the previous number, so a later figure in the same
    sentence is not given the earlier subject for free.
    """
    matches = list(_NUMBER.finditer(text))
    hits: list[tuple[str, set[str], bool]] = []
    for index, match in enumerate(matches):
        norm = _norm_number(match.group(0))
        if norm is None:
            continue
        left = match.start() - _SUBJECT_WINDOW
        if index:
            left = max(left, matches[index - 1].end())
        prefix = text[max(0, left):match.start()]
        window = {tok for tok in _token_list(prefix) if not _is_number_token(tok)}
        if window:
            hits.append((norm, window, bool(_NEGATION.search(prefix))))
    return hits


def _positive_subject_hits(text: str) -> list[tuple[str, set[str]]]:
    return [(norm, window) for norm, window, negated in _subject_hits(text) if not negated]


def _contradictory_chunks(chunks: list[_Chunk], question: str) -> list[_Chunk]:
    """Spans that state different figures for one subject the question names.

    Each figure is assigned to the rarest question word in its own prefix.
    Two subjects in one question stay apart. The same normalized figure
    written as $240 and $240.00 is one figure. A negated prefix is ignored.
    """
    query_tokens, _bigrams = _analyze_query(question)
    q_terms = {tok for tok in query_tokens if not _is_number_token(tok)}
    if not q_terms or not chunks:
        return []
    idf = _idf_map(chunks)
    n_chunks = len(chunks)
    primary = max(q_terms, key=lambda tok: (_idf_value(tok, idf, n_chunks), len(tok)))
    by_norm: dict[str, list[_Chunk]] = {}
    for chunk in chunks:
        seen_norm: set[str] = set()
        for norm, window in _positive_subject_hits(chunk.text):
            overlap = window & q_terms
            if primary not in overlap:
                continue
            focus = max(overlap, key=lambda tok: (_idf_value(tok, idf, n_chunks), len(tok)))
            if focus != primary or norm in seen_norm:
                continue
            seen_norm.add(norm)
            by_norm.setdefault(norm, []).append(chunk)
    if len(by_norm) < 2:
        return []
    chosen: list[_Chunk] = []
    seen: set[tuple[str, int, int]] = set()
    for group in by_norm.values():
        for chunk in group:
            key = (chunk.doc_id, chunk.start, chunk.end)
            if key in seen:
                continue
            seen.add(key)
            chosen.append(chunk)
    chosen.sort(key=lambda chunk: (chunk.doc_id, chunk.start))
    return chosen


def _primary_chunks(chunks: list[_Chunk], question: str, *, negated: bool) -> list[_Chunk]:
    """Chunks whose figure for the question's rarest subject word is negated or not."""
    query_tokens, _bigrams = _analyze_query(question)
    q_terms = {tok for tok in query_tokens if not _is_number_token(tok)}
    if not q_terms or not chunks:
        return []
    idf = _idf_map(chunks)
    n_chunks = len(chunks)
    primary = max(q_terms, key=lambda tok: (_idf_value(tok, idf, n_chunks), len(tok)))
    chosen: list[_Chunk] = []
    seen: set[tuple[str, int, int]] = set()
    for chunk in chunks:
        for _norm, window, is_negated in _subject_hits(chunk.text):
            if is_negated != negated:
                continue
            overlap = window & q_terms
            if primary not in overlap:
                continue
            focus = max(overlap, key=lambda tok: (_idf_value(tok, idf, n_chunks), len(tok)))
            if focus != primary:
                continue
            key = (chunk.doc_id, chunk.start, chunk.end)
            if key not in seen:
                seen.add(key)
                chosen.append(chunk)
            break
    return chosen


def _number_supported(claim: str, span: str, norm: str) -> bool:
    subjects: set[str] = set()
    for match in _NUMBER.finditer(span):
        if _norm_number(match.group(0)) != norm:
            continue
        prefix = span[max(0, match.start() - _SUBJECT_WINDOW):match.start()]
        subjects.update(_token_list(prefix))
    if not subjects:
        return False
    claim_tokens = [tok for tok in _analyze_query(claim)[0] if not _is_number_token(tok)]
    overlap = set(claim_tokens) & subjects
    if not overlap:
        return False
    claim_content = _content(claim_tokens)
    if claim_content:
        return bool(claim_content & overlap)
    return True


def _ident_supported(claim: str, span: str, ident: str) -> bool:
    if ident not in _idents(span):
        return False
    claim_tokens = [tok for tok in _analyze_query(claim)[0] if not _is_number_token(tok)]
    claim_content = _content(claim_tokens)
    if not claim_content:
        return True
    return bool(claim_content & _content(_token_list(span)))
