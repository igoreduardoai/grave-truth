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

`python3 demos/haunted/server.py` serves the page on 127.0.0.1 and answers through `DocumentAgent`. Uncited claims are ghosts and fade. Cited answers highlight the source clause. No paid API. `python3 -m http.server` only serves the static files; the answers come from the stdlib server so the page uses the same library as the evals.

Synthetic fixtures only. Not a medical device. Not legal advice.
