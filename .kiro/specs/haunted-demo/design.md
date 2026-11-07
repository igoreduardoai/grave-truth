# Design

## Page

`demos/haunted/index.html`, `app.js`, and `style.css` are static. The browser posts to `/api/ask` on the same origin. A ghost claim uses the `ghost-claim` class, which fades. A cited result renders the fixture and wraps each returned span in `mark.clause` only when the offsets slice that exact text.

## Server

`demos/haunted/server.py` is a stdlib `ThreadingHTTPServer` bound to `127.0.0.1`. It loads `grave_truth.apps.eob` or `grave_truth.apps.lease`. Those loaders ingest `fixtures/sample_eob.txt` and `fixtures/sample_lease.txt`. The process does not open an outbound socket.

`python3 -m http.server` can serve the static files and will not answer `/api/ask`. The supported command is `python3 demos/haunted/server.py`.

## Walkthrough

`scripts/demo_walkthrough.py` reads `evals/gold_cases.json` and scores each case with `grave_truth.grading.evaluate_case`. The printed answer is the library output. Pass/fail is the grader. Rejected and accepted claims print `Quote: none` because the rejection check does not invent a supporting span for a claim it refuses.

## Hook

`.kiro/hooks/walkthrough-before-demo.json` reminds the agent to run the walkthrough after the demo or the script changes, before claiming the demo works.
