"""Caption numbers have to be copied from measurement text. No browser here."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _recorder():
    path = ROOT / "scripts" / "record_demo.py"
    spec = importlib.util.spec_from_file_location("record_demo_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_caption_numbers_must_occur_as_their_own_tokens():
    recorder = _recorder()
    source = "90/90 passed\ncontrast checker cited 0 of 17\n"
    recorder.assert_caption_numbers("Gold eval 90/90 passed.", source)
    recorder.assert_caption_numbers("contrast checker cited 0 of 17.", source)
    with pytest.raises(SystemExit):
        recorder.assert_caption_numbers("Lighthouse 100.", source)
    with pytest.raises(SystemExit):
        recorder.assert_caption_numbers("cited 1 of 17.", source)


def test_contrast_count_matches_the_capability_test():
    recorder = _recorder()
    counts = recorder.measure_contrast()
    assert counts["checker"] == 0
    assert counts["cases"] == 17
    assert counts["first_sentence"] == 17
    assert counts["export_spans"] == 4
    assert counts["copy_spans"] == 0


def test_caption_builder_rejects_a_number_that_was_not_measured():
    recorder = _recorder()
    source = "\n".join(
        [
            "90/90 passed",
            "accept_grounded 22, cited 33, not_found 17, reject_ungrounded 18",
            "holdout 7/7",
            "contrast checker cited 0 of 17",
            "contrast first sentence cited 17 of 17",
            "contrast export spans 4",
            "contrast copy spans 0",
            "axe violations 0",
            "axe pages 8",
            "axe incomplete 0",
            "104 passed in 3.00s",
        ]
    )
    texts = recorder.caption_texts(source + "\n")
    assert texts[0].startswith("Synthetic fixtures only")
    assert "90/90 passed" in texts[1]
    blob = "\n".join(texts)
    assert "100" not in blob
    recorder.assert_caption_numbers(blob, source)
