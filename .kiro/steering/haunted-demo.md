---
inclusion: fileMatch
fileMatchPattern: ["demos/haunted/**", "scripts/demo_walkthrough.py"]
---

# Haunted demo

Before claiming the demo works, run:

```bash
python3 scripts/demo_walkthrough.py
```

The process must exit 0. The transcript is the evidence: question, answer, quote span, and pass or fail, for both `eob-explainer` and `lease-checker`.

`python3 demos/haunted/server.py` is the judge quickstart. It serves the page on 127.0.0.1. The judge picks the sample EOB, the sample lease, or pastes a synthetic document, then sends a question, a proposed answer, or both. The process calls `DocumentAgent` in `src/grave_truth`. It does not reimplement retrieval. A proposed answer is split into sentences and each sentence is checked with that library. Cited claims return span offsets. Uncited claims are ghosts and fade, with a text badge that still says Ghost. No paid API. `python3 -m http.server` only serves the static files.

Empty question-and-answer text, a blank pasted document, and oversized bodies return HTTP 400. Do not invent an answer for those requests. Do not add a deployment, a credential, or a network call. Synthetic text only. Not a medical device. Not legal advice.
