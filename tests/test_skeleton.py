from grave_truth.apps import eob, lease
from grave_truth.skeleton import DocumentAgent


def test_answer_cites_span_and_keeps_source_number():
    agent = eob.load_agent()
    result = agent.answer("What is the patient responsibility?")
    assert result.found
    assert result.citations
    assert "$42.15" in result.text
    assert any("$42.15" in c.span for c in result.citations)
    assert result.ghost is False


def test_missing_fact_is_not_found():
    agent = eob.load_agent()
    result = agent.answer("What is the out-of-network penalty?")
    assert result.found is False
    assert result.text == "not found"
    assert result.citations == []
    assert result.ghost is True


def test_invented_number_is_rejected():
    agent = eob.load_agent()
    assert agent.reject_ungrounded_claim("The patient responsibility is $99999.00") is True


def test_lease_late_fee_is_grounded():
    agent = lease.load_agent()
    result = agent.answer("What late fee applies after the fifth day?")
    assert result.found
    assert "$75.00" in result.text
    assert any("late fee" in c.span.lower() for c in result.citations)


def test_ingest_requires_content():
    agent = DocumentAgent()
    try:
        agent.ingest("empty", "   ")
    except ValueError:
        return
    raise AssertionError("expected ValueError")
