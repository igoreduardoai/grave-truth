import random
import re

from grave_truth.skeleton import DocumentAgent

_NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")
_TOPICS = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"]


def test_generated_documents_keep_numbers_inside_citations():
    rng = random.Random(20261106)
    for _ in range(25):
        topic, other = rng.sample(_TOPICS, 2)
        amount = f"${rng.randint(10, 99)}.{rng.randint(0, 99):02d}"
        other_amount = f"${rng.randint(100, 199)}.{rng.randint(0, 99):02d}"
        invented = f"${rng.randint(500, 900)}.{rng.randint(0, 99):02d}"
        doc = f"The {topic} total is {amount}. The {other} note is {other_amount}."
        agent = DocumentAgent()
        agent.ingest("gen", doc)
        result = agent.answer(f"What is the {topic} total?")
        assert result.found
        assert amount in result.text
        assert other_amount not in result.text
        assert result.citations
        for citation in result.citations:
            assert doc[citation.start:citation.end] == citation.span
            assert topic in citation.span
        for number in _NUMBER.findall(result.text):
            assert any(number in citation.span for citation in result.citations)
        assert agent.reject_ungrounded_claim(f"The {topic} total is {invented}.") is True
        assert agent.reject_ungrounded_claim(f"The {topic} total is {amount}.") is False
        missing = agent.answer(f"What is the {topic} zebra quota?")
        assert missing.found is False
        assert missing.text == "not found"


def test_absent_vocabulary_does_not_borrow_a_span():
    agent = DocumentAgent()
    agent.ingest("gen", "The alpha total is $10.00. The bravo note is $20.00.")
    result = agent.answer("What is the satellite dish fee?")
    assert result.found is False
    assert result.citations == []
