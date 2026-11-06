from pathlib import Path

from grave_truth.skeleton import DocumentAgent

ROOT = Path(__file__).resolve().parents[1]


def _both() -> DocumentAgent:
    agent = DocumentAgent()
    agent.ingest("eob", (ROOT / "fixtures" / "sample_eob.txt").read_text(encoding="utf-8"))
    agent.ingest("lease", (ROOT / "fixtures" / "sample_lease.txt").read_text(encoding="utf-8"))
    return agent


def test_citations_are_exact_source_slices():
    agent = _both()
    for question in (
        "What is the patient responsibility?",
        "What is the security deposit?",
        "How much did the plan pay?",
    ):
        result = agent.answer(question)
        assert result.found, question
        for citation in result.citations:
            source = {
                "eob": (ROOT / "fixtures" / "sample_eob.txt").read_text(encoding="utf-8"),
                "lease": (ROOT / "fixtures" / "sample_lease.txt").read_text(encoding="utf-8"),
            }[citation.doc_id]
            assert source[citation.start:citation.end] == citation.span


def test_shared_dollar_amount_stays_with_its_subject():
    agent = _both()
    deposit = agent.answer("What is the security deposit?")
    assert deposit.found
    assert len(deposit.citations) == 1
    assert "security deposit" in deposit.citations[0].span
    assert "Monthly rent" not in deposit.citations[0].span
    assert agent.reject_ungrounded_claim("The security deposit is $75.00.") is True
    assert agent.reject_ungrounded_claim("Monthly rent is $75.00.") is True
    assert agent.reject_ungrounded_claim("The security deposit is $1,850.00.") is False


def test_swapped_eob_figures_are_rejected():
    agent = _both()
    assert agent.reject_ungrounded_claim("The billed amount is $180.00.") is True
    assert agent.reject_ungrounded_claim("The plan paid $240.00.") is True
    assert agent.reject_ungrounded_claim("The patient coinsurance is 80%.") is True
    assert agent.reject_ungrounded_claim("The plan allowed amount is $180.00.") is False


def test_documents_do_not_bleed_across_ids():
    agent = _both()
    result = agent.answer("What is the patient responsibility?")
    assert {citation.doc_id for citation in result.citations} == {"eob"}
    assert agent.answer("What is the reserved parking fee?").found is False


def test_reingest_replaces_previous_spans():
    agent = DocumentAgent()
    agent.ingest("gen", "The alpha total is $10.00.")
    agent.ingest("gen", "The alpha total is $12.00.")
    result = agent.answer("What is the alpha total?")
    assert "$12.00" in result.text
    assert "$10.00" not in result.text
    assert agent.reject_ungrounded_claim("The alpha total is $10.00.") is True


def test_blank_question_is_not_found():
    agent = DocumentAgent()
    agent.ingest("gen", "The alpha total is $10.00.")
    result = agent.answer("   ")
    assert result.found is False
    assert result.text == "not found"
    assert result.citations == []
