"""The demo ends in a deterministic file a person can take with them."""

import json

from grave_truth.artifact import build_artifact


def test_eob_letter_links_cited_claims_and_abstains_on_the_rest():
    artifact = build_artifact("eob")
    again = build_artifact("eob")
    assert artifact == again
    assert artifact["kind"] == "dispute-letter"
    assert artifact["live_model"] == "unimplemented"
    assert artifact["filename"] == "grave-truth-dispute-letter.md"
    document = artifact["document"]
    cited = [item for item in artifact["items"] if item["verdict"] == "cited"]
    missing = [item for item in artifact["items"] if item["verdict"] == "not_found"]
    assert len(cited) == 2
    assert len(missing) == 2
    swapped = next(item for item in artifact["items"] if "$180.00" in item["claim"])
    assert swapped["verdict"] == "not_found"
    assert swapped["citations"] == []
    penalty = next(item for item in artifact["items"] if "out-of-network" in item["claim"])
    assert penalty["verdict"] == "not_found"
    assert penalty["citations"] == []
    for item in cited:
        assert item["citations"]
        for citation in item["citations"]:
            assert document[citation["start"]:citation["end"]] == citation["span"]
            assert citation["span"] in artifact["markdown"]
            assert f'{citation["doc_id"]} [{citation["start"]}:{citation["end"]}]' in artifact["markdown"]
    assert all("$180.00" not in citation["span"] for item in artifact["items"] for citation in item["citations"])
    assert "$50.00" not in " ".join(
        citation["span"] for item in artifact["items"] for citation in item["citations"]
    )
    assert "not found" in artifact["markdown"].lower()
    assert "not a medical device" in artifact["markdown"].lower()
    assert "not legal advice" in artifact["markdown"].lower()


def test_lease_list_is_a_different_file_with_the_same_link_rule():
    artifact = build_artifact("lease")
    assert artifact["kind"] == "clause-issues"
    assert artifact["filename"] == "grave-truth-clause-issues.md"
    document = artifact["document"]
    cited = [item for item in artifact["items"] if item["verdict"] == "cited"]
    missing = [item for item in artifact["items"] if item["verdict"] == "not_found"]
    assert len(cited) == 2
    assert len(missing) == 2
    late = next(item for item in artifact["items"] if item["claim"] == "The late fee is $1,850.00.")
    assert late["verdict"] == "not_found"
    assert late["citations"] == []
    for item in cited:
        for citation in item["citations"]:
            assert document[citation["start"]:citation["end"]] == citation["span"]
            assert "$1,850.00" in citation["span"] or "$75.00" in citation["span"]


def test_naive_copy_has_no_span_links():
    """Without the checker, copying the claim does not attach a source span."""
    artifact = build_artifact("eob")
    linked = sum(len(item["citations"]) for item in artifact["items"])
    naive_linked = 0
    assert linked == 2
    assert naive_linked == 0
    assert linked > naive_linked
